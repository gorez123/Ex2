# Software Architecture & Main Components

## 1. Architectural Pattern
**SmartClass** follows a **Modular Layered Monolith (KISS-oriented)** architecture built around Object-Oriented Design (OOD) principles[cite: 1]:
* **Presentation Layer (Mobile & Desktop Web UI):** Responsive HTML5/JS/Tailwind client served directly by the backend—zero app installation or frontend build toolchain required[cite: 1].
* **API & Controller Layer (FastAPI):** Exposes clean REST endpoints for student actions, lecturer controls, and file uploads.
* **Domain & Service Layer (OOP Core):** Encapsulates business logic into decoupled service classes with clean interfaces (enabling easy swapping between local OpenCV, Gemini Vision API, Whisper, etc.)[cite: 1].
* **Persistence & Export Layer:** Lightweight SQLite database for session state, paired with `OpenPyXL` / `Pandas` for offline Excel/CSV spreadsheet generation[cite: 1].

---

## 2. Component Diagram (Mermaid)

```mermaid
flowchart TB
    subgraph Clients["Client Layer (Zero-Install Web)"]
        StudentUI["Student Mobile Browser\n(Check-in, Polls, Feedback, HW)"]
        LecturerUI["Lecturer Dashboard\n(Photo Upload, Live Feed, Export, ML)"]
    end

    subgraph Backend["SmartClass FastAPI Server"]
        Router["REST API Controllers\n(/attendance, /polls, /feedback, /ai)"]
        
        subgraph Services["Core OOP Domain Services"]
            AttSvc["AttendanceManager\n(Roster matching & reconciliation)"]
            VisionSvc["VisionCounterService\n(Classroom photo headcount)"]
            PollSvc["PollAndFeedbackService\n(Live polls & student comments)"]
            VideoSvc["VideoSummarizerService\n(Transcription + LLM summary)"]
            HWSvc["HomeworkReviewerService\n(Repo parser + Peer LLM diff)"]
        end
    end

    subgraph Storage_External["Data & External AI Adapters"]
        DB[("SQLite DB\n(Sessions, Votes, Logs)")]
        Excel["Spreadsheet Exporter\n(.xlsx / .csv)"]
        AI["External AI / ML Engines\n(Vision-LLM / OpenCV / Whisper)"]
    end

    StudentUI <-->|HTTP / JSON| Router
    LecturerUI <-->|HTTP / JSON| Router
    Router --> AttSvc & PollSvc & VideoSvc & HWSvc
    AttSvc --> VisionSvc
    AttSvc & PollSvc --> DB
    AttSvc --> Excel
    VisionSvc & VideoSvc & HWSvc <--> AI