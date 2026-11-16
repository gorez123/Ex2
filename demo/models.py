from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class Student(BaseModel):
    id: int
    full_name: str
    email: str
    group: str = "General"


class AttendanceRecord(BaseModel):
    student_id: int
    student_name: str
    email: str
    timestamp: str = Field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))
    status: str = "Present"


class LectureSession(BaseModel):
    session_id: str
    title: str
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))
    is_active: bool = True
    photo_headcount: Optional[int] = None
    photo_note: str = ""
    records: Dict[str, AttendanceRecord] = Field(default_factory=dict)

    def add_check_in(self, student: Student) -> AttendanceRecord:
        key = student.email.lower()
        if key in self.records:
            return self.records[key]
        record = AttendanceRecord(
            student_id=student.id,
            student_name=student.full_name,
            email=student.email,
        )
        self.records[key] = record
        return record

    def get_discrepancy(self) -> Optional[int]:
        if self.photo_headcount is None:
            return None
        return self.photo_headcount - len(self.records)


class Poll(BaseModel):
    poll_id: str
    question: str
    options: List[str]
    votes: Dict[str, int] = Field(default_factory=dict)  # student_id -> option_index
    is_open: bool = True

    def cast_vote(self, student_id: str, option_index: int) -> bool:
        if not self.is_open or option_index < 0 or option_index >= len(self.options):
            return False
        self.votes[student_id.strip().lower()] = option_index
        return True

    def results(self) -> List[Dict]:
        counts = [0] * len(self.options)
        for idx in self.votes.values():
            if 0 <= idx < len(counts):
                counts[idx] += 1
        return [
            {"option": opt, "count": counts[i]}
            for i, opt in enumerate(self.options)
        ]


class FeedbackMessage(BaseModel):
    msg_id: str
    author: str
    content: str
    is_anonymous: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%H:%M"))
    resolved: bool = False