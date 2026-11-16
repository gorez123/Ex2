import os
from typing import List
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .services import (
    AIServices,
    AttendanceManager,
    GeminiVisionCounter,
    PollAndFeedbackService,
    SpreadsheetExporter,
)

app = FastAPI(title="SmartClass — LLM-Ready Classroom Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OOP Services
vision_counter = GeminiVisionCounter()
attendance_mgr = AttendanceManager(vision_counter=vision_counter)
poll_feedback_svc = PollAndFeedbackService()
ai_svc = AIServices()

# Auto-load course roster from project root or samples/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
loaded_count = attendance_mgr.load_roster_from_folder([
    BASE_DIR,
    os.path.join(BASE_DIR, "samples"),
])
print(f"[SmartClass] Loaded {loaded_count} students into roster.")


# --- Request Schemas ---
class SessionCreateReq(BaseModel):
    title: str


class CheckInReq(BaseModel):
    identifier: str


class PollCreateReq(BaseModel):
    question: str
    options: List[str]


class VoteReq(BaseModel):
    student_id: str
    option_index: int


class FeedbackReq(BaseModel):
    author: str = ""
    content: str
    is_anonymous: bool = False


class SummarizeReq(BaseModel):
    content: str


class HomeworkReviewReq(BaseModel):
    submission: str
    rubric: str


# --- API Endpoints ---
@app.get("/api/state")
def get_state():
    session = attendance_mgr.get_active_session()
    poll = poll_feedback_svc.active_poll
    return {
        "roster_size": len(attendance_mgr.roster),
        "session": {
            "session_id": session.session_id,
            "title": session.title,
            "created_at": session.created_at,
            "digital_count": len(session.records),
            "photo_headcount": session.photo_headcount,
            "photo_note": session.photo_note,
            "discrepancy": session.get_discrepancy(),
            "recent_checkins": list(session.records.values())[-10:],
        },
        "poll": {
            "poll_id": poll.poll_id,
            "question": poll.question,
            "is_open": poll.is_open,
            "total_votes": len(poll.votes),
            "results": poll.results(),
        } if poll else None,
        "feedback": poll_feedback_svc.messages[:20],
    }


@app.post("/api/sessions")
def create_session(req: SessionCreateReq):
    session = attendance_mgr.create_session(req.title)
    return {"session_id": session.session_id, "title": session.title}


@app.post("/api/checkin")
def student_checkin(req: CheckInReq):
    try:
        rec = attendance_mgr.check_in(req.identifier)
        return {"status": "checked_in", "record": rec}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/api/attendance/photo")
async def upload_classroom_photo(file: UploadFile = File(...)):
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image file.")
    return attendance_mgr.verify_with_photo(image_bytes)


@app.get("/api/attendance/export")
def export_attendance_xlsx():
    session = attendance_mgr.get_active_session()
    roster_list = list(attendance_mgr.roster.values())
    xlsx_bytes = SpreadsheetExporter.export_xlsx(session, roster_list)
    filename = f"attendance_{session.session_id}.xlsx"
    return Response(
        content=xlsx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.post("/api/polls")
def launch_poll(req: PollCreateReq):
    if len([o for o in req.options if o.strip()]) < 2:
        raise HTTPException(status_code=400, detail="Provide at least 2 poll options.")
    poll = poll_feedback_svc.launch_poll(req.question, req.options)
    return {"poll_id": poll.poll_id, "question": poll.question}


@app.post("/api/polls/vote")
def vote_poll(req: VoteReq):
    try:
        poll = poll_feedback_svc.vote(req.student_id, req.option_index)
        return {"total_votes": len(poll.votes), "results": poll.results()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/polls/close")
def close_poll():
    poll_feedback_svc.close_poll()
    return {"status": "closed"}


@app.post("/api/feedback")
def post_feedback(req: FeedbackReq):
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="Feedback cannot be empty.")
    msg = poll_feedback_svc.add_feedback(req.author, req.content, req.is_anonymous)
    return msg


@app.post("/api/ai/summarize")
def summarize_lecture(req: SummarizeReq):
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="Transcript or notes required.")
    return {"summary": ai_svc.summarize_lecture(req.content)}


@app.post("/api/ai/review-homework")
def review_homework(req: HomeworkReviewReq):
    if not req.submission.strip():
        raise HTTPException(status_code=400, detail="Code or repository details required.")
    return {"review": ai_svc.review_homework(req.submission, req.rubric)}


# Serve static frontend
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def serve_home():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))