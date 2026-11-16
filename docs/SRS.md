# Software Requirements Specification (SRS)
**System Name:** SmartClass  
**Version:** 1.0  
**Standard:** IEEE 830 Adapted (KISS & Design-First Focus)  

---

## 1. Introduction
### 1.1 Purpose
This document specifies the functional and non-functional requirements for **SmartClass**, a web-based teaching assistant designed for live university lectures[cite: 1].

### 1.2 User Roles (Actors)
* **Lecturer:** Creates lecture sessions, captures/uploads classroom photos for automated headcount, launches instant polls, exports attendance spreadsheets, generates ML video summaries, and runs LLM homework reviews[cite: 1].
* **Student:** Accesses the web app via smartphone browser (no installation), marks attendance, submits real-time comments/suggestions, votes in live polls, and requests LLM feedback on homework[cite: 1].

---

## 2. Functional Requirements (FR)

### FR-1: Automated Attendance & Headcount (Core Priority)
* **FR-1.1:** The system shall allow students to check in to an active lecture session via a simple mobile web form (selecting or entering their email/name from the course roster)[cite: 1].
* **FR-1.2:** The system shall allow the lecturer to upload or capture a classroom photo and automatically estimate the physical headcount using AI/CV[cite: 1].
* **FR-1.3:** The system shall cross-reference digital check-ins against the physical photo headcount to flag discrepancies[cite: 1].
* **FR-1.4:** The lecturer shall be able to export the complete attendance report (present, absent, timestamp, photo count) as an offline `.xlsx` or `.csv` spreadsheet[cite: 1].

### FR-2: Real-Time & Offline Student Feedback
* **FR-2.1:** Students shall be able to post comments, questions, or suggestions during or after a lecture[cite: 1].
* **FR-2.2:** The lecturer dashboard shall display incoming student comments in near real-time with optional anonymity[cite: 1].

### FR-3: On-the-Spot (KISS) Polls
* **FR-3.1:** The lecturer shall be able to create and publish a multiple-choice poll within seconds during a lecture[cite: 1].
* **FR-3.2:** Students shall be able to submit a single vote from their mobile browser and view live aggregated results once closed[cite: 1].

### FR-4: ML Lecture Video Summarizer
* **FR-4.1:** The lecturer shall be able to upload a lecture recording (e.g., `.mp4` from Zoom/Meet) or transcript[cite: 1].
* **FR-4.2:** The system shall generate a structured summary highlighting key topics, technical explanations, and Q&A points[cite: 1].

### FR-5: LLM Deep Homework & Peer-Comparison Reviewer
* **FR-5.1:** Students and lecturers shall be able to submit a GitHub repository URL or code archive for automated LLM review[cite: 1].
* **FR-5.2:** The system shall evaluate the submission against assignment requirements and compare its structure/approach against a cohort of peer repositories[cite: 1].

---

## 3. Non-Functional Requirements (NFR)
* **NFR-1 (Usability / KISS):** Student workflows must require zero app installation and at most 2 taps on a mobile web browser[cite: 1].
* **NFR-2 (Isolation):** The system must operate completely standalone without external dependencies on Moodle, Zoom APIs, or university portals[cite: 1].
* **NFR-3 (Performance):** Mobile check-in and poll submissions must respond within `< 500ms` under typical classroom load (~100 concurrent students)[cite: 1].
* **NFR-4 (Portability & Maintainability):** Built using modular Object-Oriented Python (FastAPI) and standard web technologies (HTML/JS) so third-party AI/ML tools can be swapped cleanly[cite: 1].