# Main Use Cases & Client Stories

## 1. Use Case Overview
This document defines the primary interaction flows between the two system actors (**Lecturer** and **Student**) and **SmartClass**.

---

## 2. Detailed Use Cases

### UC-1: Hybrid Classroom Attendance & Spreadsheet Export (Core Feature)
* **Primary Actor:** Lecturer & Student
* **Preconditions:** A lecture session is active; the course roster (`courseid_130158_participants`) is loaded.
* **Main Flow:**
  1. The lecturer starts a new lecture session and displays the session URL/QR code on the classroom projector.
  2. Students open the link on their mobile browsers, select/enter their name or email, and tap **"Check In"**[cite: 1].
  3. The lecturer takes a photo of the classroom (using a smartphone or webcam) and uploads it to the dashboard[cite: 1].
  4. The `VisionCounterService` analyzes the photo and returns an estimated physical headcount (e.g., `26` students)[cite: 1, 3].
  5. The system compares digital check-ins (`N_digital`) against the physical headcount (`N_photo`) and flags any discrepancy[cite: 1].
  6. The lecturer clicks **"Export Attendance"**, downloading an `.xlsx` / `.csv` spreadsheet with timestamps, student statuses, and photo verification metrics[cite: 1].
* **Alternative Flow (Offline / Network Drop):** If classroom Wi-Fi fails, the lecturer can still upload the classroom photo later for offline headcount logging and manual reconciliation[cite: 1].

---

### UC-2: Real-Time & Offline Student Feedback
* **Primary Actor:** Student (Poster), Lecturer (Reader)[cite: 1]
* **Main Flow:**
  1. During or after class, a student opens the **"Feedback / Q&A"** tab on their phone[cite: 1].
  2. The student types a question or suggestion (e.g., *"Can you slow down on the Sequence Diagram explanation?"*) and optionally toggles **"Post Anonymously"**.
  3. The comment immediately appears on the lecturer's live feed[cite: 1].
  4. The lecturer reviews and marks comments as *"Addressed"*.

---

### UC-3: On-the-Spot (KISS) Classroom Poll
* **Primary Actor:** Lecturer (Creator), Student (Voter)[cite: 1]
* **Main Flow:**
  1. The lecturer clicks **"Quick Poll"**, enters a short question and 2–4 options (e.g., *"Did you understand the SOLID Dependency Inversion example?"* -> `Yes` / `Partially` / `No`), and clicks **Launch**[cite: 1].
  2. Connected student mobile screens automatically display the active poll[cite: 1].
  3. Students tap their answer (one vote per student)[cite: 1].
  4. The lecturer views live vote distribution and closes the poll.

---

### UC-4: ML Lecture Recording Summarization
* **Primary Actor:** Lecturer[cite: 1]
* **Main Flow:**
  1. After class, the lecturer uploads a recorded class video (e.g., `m21.mp4` from Zoom/Meet) or raw transcript.
  2. The `VideoSummarizerService` extracts audio, transcribes speech, and prompts an LLM to generate a structured study guide (Key Concepts, Code Examples Discussed, Student Questions, Action Items)[cite: 1].
  3. The lecturer reviews and shares the Markdown/PDF summary with the class.

---

### UC-5: LLM Homework & Peer-Comparison Review
* **Primary Actor:** Student & Lecturer[cite: 1]
* **Main Flow:**
  1. A student or lecturer submits a GitHub repository link (or `.zip` archive) along with the assignment rubric.
  2. The `HomeworkReviewerService` fetches the source code files and compares them against both the assignment requirements and peer submissions in the cohort[cite: 1, 2].
  3. The system outputs a structured review covering: requirement coverage, OOP design quality, potential bugs, and similarity/approach comparison against peer repositories[cite: 1].