# Technical-Related Tools Report & Real-Life Benchmarks

## 1. Objective
In accordance with the KISS (Keep It Simple, Stupid) and "compose rather than build from scratch" guidelines, we evaluated and benchmarked existing libraries, models, and tools against the actual course datasets provided for Ex2:
* **Class Photos:** Multi-angle classroom images (ground truth: 26 present students in the primary front-view frame).
* **Participants Roster:** `courseid_130158_participants` (102 enrolled students + lecturer metadata).
* **Classroom Video:** `m21.mp4` sample recording and reference Zoom summary.
* **Sample Repositories:** Student assignment repositories for automated LLM code review.

---

## 2. Feature-by-Feature Tool Evaluation & Benchmarks

### Feature 1: Automated Attendance & Classroom Headcount (Core Feature)
We tested two computer vision approaches on the classroom photo (`26` actual students) alongside a lightweight web check-in mechanism:

1. **Classical Computer Vision — OpenCV Haar Cascade (`haarcascade_frontalface_default.xml`)**
   * **Real-Life Test Result:** Detected only **6 out of 26 students** (~23% recall).
   * **Failure Analysis:** Classical feature-based detectors fail heavily in lecture halls due to desk occlusions, side/downward head angles (students looking at laptops), distance in back rows, and overhead fluorescent lighting.
   * **Artifact:** Saved output bounding-box image in `/samples/haar_result.jpg`.
2. **Multimodal Vision-LLM — Gemini 2.5 Flash (`google-genai` SDK)**
   * **Real-Life Test Result:** Accurately identifies classroom context, handles partial occlusion behind desks/laptops, and estimates **26/26 students** across multiple angles without requiring custom model training or heavy GPU dependencies.
3. **Student Self Check-In & Spreadsheet Export — FastAPI + Pandas/OpenPyXL**
   * **Real-Life Test Result:** Tested parsing `courseid_130158_participants` (102 records) and generating a clean `.xlsx` / `.csv` attendance sheet cross-referencing self-check-ins against the photo headcount.
* **Verdict:** **Selected** — Hybrid approach combining a mobile QR web check-in (matching against the 102-student roster) + Vision-LLM photo verification + `openpyxl` spreadsheet export.

---

### Feature 2 & 3: Real-Time Student Feedback & On-the-Spot Polls
* **Candidates Evaluated:**
  1. **Custom WebSockets / Django Channels:** Too heavy for a KISS prototype; violates minimal-code guidelines.
  2. **FastAPI + Lightweight REST Polling / SSE (Server-Sent Events) + SQLite:** Zero external broker required, runs locally or on any free tier, handles 100+ concurrent mobile browser clients effortlessly.
* **Verdict:** **Selected** — FastAPI + SQLite + Vanilla HTML/JS (Tailwind CSS via CDN) for instant mobile access via QR code with zero app installation.

---

### Feature 4: ML Lecture Video Summarizer
* **Candidates Evaluated:**
  1. **Default Zoom AI Summary (Baseline):** Produces generic, high-level bullet points that miss technical nuances, code discussions, and student questions ("nothing to write home about").
  2. **OpenAI Whisper (`faster-whisper`) + Structured LLM Prompting:** Tested pipeline architecture on `m21.mp4` audio track extraction -> timestamped transcript -> structured Markdown summary (Key Concepts, Action Items, Q&A Highlights).
* **Verdict:** **Selected** — Whisper transcription paired with structured LLM summarization.

---

### Feature 5: LLM Homework & Repository Reviewer
* **Candidates Evaluated:**
  1. **Static Linters (`pylint` / `flake8`):** Only catch syntax and PEP8 style issues; cannot evaluate OOP design, architectural choices, or cross-student similarity.
  2. **GitHub API / `git clone` Ingestion + LLM Context Review:** Fetches student repository source trees, evaluates adherence to assignment requirements, and compares structural patterns across peer submissions.
* **Verdict:** **Selected** — Automated repository file aggregator + LLM rubric-based reviewer.

---

## 3. Summary Architecture Stack (Final Selection)

| Layer | Chosen Tool / Technology | Justification |
| :--- | :--- | :--- |
| **Backend & API** | Python 3.12 + FastAPI | Fast, lightweight, native async support, easy REST endpoints. |
| **Database & Export** | SQLite + `openpyxl` / `pandas` | Zero-config persistence; direct `.xlsx`/`.csv` export for the lecturer. |
| **Frontend (KISS)** | HTML5 + Vanilla JS + Tailwind CDN | Mobile-first responsive UI, zero build step required. |
| **AI / Vision / NLP** | Gemini API (`google-genai`) + Whisper | Solves classroom occlusion counting, video summarization, and repo comparison out-of-the-box. |