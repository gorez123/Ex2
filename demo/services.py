from abc import ABC, abstractmethod
import csv
import io
import os
import re
import time
from typing import Dict, List, Optional, Tuple
import uuid

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError
import openpyxl
from PIL import Image

from .models import AttendanceRecord, FeedbackMessage, LectureSession, Poll, Student

load_dotenv()


# --- Strategy Pattern for Classroom Vision Headcount ---
class IVisionCounter(ABC):
    @abstractmethod
    def count_students(self, image_bytes: bytes) -> Tuple[int, str]:
        pass


class GeminiVisionCounter(IVisionCounter):
    def __init__(self):
        self.client = genai.Client() if os.getenv("GEMINI_API_KEY") else None
        self.models = ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3.8-pro"]

    def count_students(self, image_bytes: bytes) -> Tuple[int, str]:
        if not self.client:
            return 0, "GEMINI_API_KEY missing in .env"

        pil_img = Image.open(io.BytesIO(image_bytes))
        prompt = (
            "Count the exact number of students sitting in this university classroom. "
            "Ignore the lecturer if standing at the front. Return ONLY the integer number first, "
            "followed by a short 1-sentence explanation."
        )

        for model_name in self.models:
            try:
                res = self.client.models.generate_content(
                    model=model_name,
                    contents=[pil_img, prompt],
                )
                text = res.text.strip()
                match = re.search(r"\d+", text)
                count = int(match.group(0)) if match else 0
                return count, f"[{model_name}] {text}"
            except APIError:
                time.sleep(0.5)
                continue

        return 0, "All Gemini vision models temporarily overloaded (503)."


# --- Spreadsheet Exporter (.xlsx) ---
class SpreadsheetExporter:
    @staticmethod
    def export_xlsx(session: LectureSession, roster: List[Student]) -> bytes:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"Attendance_{session.session_id}"

        ws.append(["Session ID", session.session_id, "Title", session.title, "Created", session.created_at])
        ws.append([
            "Digital Check-Ins", len(session.records),
            "Photo Headcount", session.photo_headcount if session.photo_headcount is not None else "N/A",
            "Discrepancy", session.get_discrepancy() if session.get_discrepancy() is not None else "N/A",
        ])
        ws.append([])
        ws.append(["Student ID", "Full Name", "Email", "Group", "Status", "Check-In Time"])

        for student in roster:
            rec = session.records.get(student.email.lower())
            status = rec.status if rec else "Absent"
            ts = rec.timestamp if rec else "-"
            ws.append([student.id, student.full_name, student.email, student.group, status, ts])

        stream = io.BytesIO()
        wb.save(stream)
        stream.seek(0)
        return stream.read()


# --- Core Attendance Manager ---
class AttendanceManager:
    def __init__(self, vision_counter: IVisionCounter):
        self.vision_counter = vision_counter
        self.roster: Dict[str, Student] = {}
        self.sessions: Dict[str, LectureSession] = {}
        self.active_session_id: Optional[str] = None

    def load_roster_from_folder(self, search_dirs: List[str]) -> int:
        for folder in search_dirs:
            if not os.path.isdir(folder):
                continue
            for fname in os.listdir(folder):
                if "participants" in fname.lower() and fname.endswith((".csv", ".xlsx")):
                    path = os.path.join(folder, fname)
                    return self._parse_roster_file(path)

        # Fallback sample students if roster file is not placed yet
        fallback = [
            Student(id=1001, full_name="Guy Gersner", email="guy@ariel.ac.il", group="A"),
            Student(id=1002, full_name="Noa Levi", email="noa@ariel.ac.il", group="A"),
            Student(id=1003, full_name="Dan Cohen", email="dan@ariel.ac.il", group="B"),
        ]
        for s in fallback:
            self.roster[s.email.lower()] = s
        return len(self.roster)

    def _parse_roster_file(self, path: str) -> int:
        self.roster.clear()
        rows = []
        if path.endswith(".csv"):
            with open(path, encoding="utf-8-sig") as f:
                rows = list(csv.DictReader(f))
        elif path.endswith(".xlsx"):
            wb = openpyxl.load_workbook(path, data_only=True)
            ws = wb.active
            headers = [str(c.value or "").strip() for c in next(ws.iter_rows(min_row=1, max_row=1))]
            for r in ws.iter_rows(min_row=2, values_only=True):
                if any(r):
                    rows.append(dict(zip(headers, r)))

        for idx, row in enumerate(rows, start=1):
            norm = {str(k).lower(): str(v or "").strip() for k, v in row.items()}
            # תופס כל עמודה שיש בה @ (עובד גם כשהכותרת בעברית כמו 'כתובת דוא"ל')
            email = next((v for v in norm.values() if "@" in v), f"student{idx}@ariel.ac.il")
            first = next((v for k, v in norm.items() if "first" in k or "פרטי" in k), "")
            last = next((v for k, v in norm.items() if "last" in k or "משפחה" in k), "")
            full = f"{first} {last}".strip() or next((v for k, v in norm.items() if "name" in k or "שם" in k), f"Student {idx}")
            sid_raw = next((v for k, v in norm.items() if ("id" in k or "זהות" in k) and v.isdigit()), str(1000 + idx))
            group = next((v for k, v in norm.items() if "group" in k or "קבוצה" in k), "Course 130158")
            self.roster[email.lower()] = Student(id=int(sid_raw), full_name=full, email=email, group=group)
        return len(self.roster)

    def create_session(self, title: str) -> LectureSession:
        sid = f"LEC-{uuid.uuid4().hex[:4].upper()}"
        session = LectureSession(session_id=sid, title=title)
        self.sessions[sid] = session
        self.active_session_id = sid
        return session

    def get_active_session(self) -> LectureSession:
        if not self.active_session_id or self.active_session_id not in self.sessions:
            return self.create_session("OOP & Software Engineering - Live Lecture")
        return self.sessions[self.active_session_id]

    def check_in(self, identifier: str) -> AttendanceRecord:
        session = self.get_active_session()
        ident = identifier.strip().lower()
        student = self.roster.get(ident)
        if not student:
            # Allow partial match by name or ID for smooth live classroom UX
            for s in self.roster.values():
                if ident in s.full_name.lower() or ident == str(s.id):
                    student = s
                    break
        if not student:
            raise ValueError(f"Student '{identifier}' not found in course roster ({len(self.roster)} enrolled).")
        return session.add_check_in(student)

    def verify_with_photo(self, image_bytes: bytes) -> dict:
        session = self.get_active_session()
        count, note = self.vision_counter.count_students(image_bytes)
        session.photo_headcount = count
        session.photo_note = note
        return {
            "session_id": session.session_id,
            "digital_check_ins": len(session.records),
            "photo_headcount": count,
            "discrepancy": session.get_discrepancy(),
            "vision_note": note,
        }


# --- Polls & Student Feedback Service ---
class PollAndFeedbackService:
    def __init__(self):
        self.active_poll: Optional[Poll] = None
        self.messages: List[FeedbackMessage] = []

    def launch_poll(self, question: str, options: List[str]) -> Poll:
        self.active_poll = Poll(
            poll_id=uuid.uuid4().hex[:6],
            question=question,
            options=[o.strip() for o in options if o.strip()],
        )
        return self.active_poll

    def vote(self, student_id: str, option_index: int) -> Poll:
        if not self.active_poll or not self.active_poll.is_open:
            raise ValueError("No open poll right now.")
        if not self.active_poll.cast_vote(student_id, option_index):
            raise ValueError("Invalid option selected.")
        return self.active_poll

    def close_poll(self) -> Optional[Poll]:
        if self.active_poll:
            self.active_poll.is_open = False
        return self.active_poll

    def add_feedback(self, author: str, content: str, is_anonymous: bool) -> FeedbackMessage:
        msg = FeedbackMessage(
            msg_id=uuid.uuid4().hex[:6],
            author="Anonymous Student" if is_anonymous else (author.strip() or "Student"),
            content=content.strip(),
            is_anonymous=is_anonymous,
        )
        self.messages.insert(0, msg)
        return msg


# --- AI Lecture Summarizer & Homework Reviewer ---
class AIServices:
    def __init__(self):
        self.client = genai.Client() if os.getenv("GEMINI_API_KEY") else None
        self.models = ["gemini-3.8-flash", "gemini-3.5-flash"]

    def _generate(self, contents) -> str:
        if not self.client:
            return "GEMINI_API_KEY missing in .env."
        for m in self.models:
            try:
                res = self.client.models.generate_content(model=m, contents=contents)
                return res.text.strip()
            except APIError:
                time.sleep(0.5)
        return "AI model temporarily unavailable."

    def summarize_lecture(self, transcript_or_notes: str) -> str:
        prompt = (
            "You are an expert university Teaching Assistant. Summarize this lecture recording/transcript "
            "into clear, structured Markdown with: 1) Core Concepts, 2) Key Technical Takeaways, "
            "and 3) Likely Exam Questions.\n\nContent:\n" + transcript_or_notes
        )
        return self._generate(prompt)

    def review_homework(self, repo_url_or_code: str, rubric: str) -> str:
        prompt = (
            "You are an OOP & Software Engineering code reviewer. Evaluate the following student submission "
            "against the rubric. Provide: 1) Requirement Coverage, 2) OOP/SOLID Strengths & Issues, "
            "3) Architectural Comparison Notes, and 4) Actionable Improvements.\n\n"
            f"Rubric:\n{rubric}\n\nSubmission:\n{repo_url_or_code}"
        )
        return self._generate(prompt)