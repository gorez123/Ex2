# SmartClass - LLM-Ready Classroom Assistant (Ex2)

## 📌 Problem Statement
Current online teaching platforms (such as Moodle and Zoom) are bloated, clunky, and lack native AI/LLM capabilities[cite: 1]. During live lectures, attendance tracking wastes valuable teaching time, real-time student feedback is fragmented, and reviewing recordings or student code repositories requires heavy manual effort. We need a lightweight, KISS-compliant (Keep It Simple, Stupid), mobile-first web tool that bridges these gaps[cite: 1].

## 🎯 Project Scope
This project focuses on the **system design, software architecture, and rapid prototyping (Vibe Coding)** of an end-to-end web application tailored for university lectures[cite: 1, 2].

### In-Scope (Core Features)
1. **Automated Attendance & Headcount (Core Feature):** Simple student check-in paired with computer-vision crowd counting from a classroom photo, exporting directly to an online/offline spreadsheet[cite: 1].
2. **Real-Time Student Feedback:** Live/offline comment and suggestion board for students during lectures[cite: 1].
3. **On-the-Spot Polls:** Instant, low-friction polls created by the lecturer during class[cite: 1].
4. **ML Lecture Summarizer:** Automated, structured summaries generated from class video/transcripts (improving upon standard Zoom summaries)[cite: 1, 2].
5. **LLM Homework Reviewer:** Deep automated code/assignment review for both students and lecturers, including cross-referencing against peer repositories[cite: 1].

### Out-of-Scope (Constraints & Guidelines)
* **No External LMS/University Integrations:** No API integrations with Moodle, Zoom, or Ariel University's personal portal ("מידע אישי")[cite: 1].
* **Design-First Approach:** Production-grade hardening, enterprise security, and heavy custom backend infrastructure are out of scope; existing open-source tools, APIs, and AI-composed code are prioritized to deliver a working classroom demo[cite: 1].

## 📂 Repository Structure
* `/docs` - SoW, SRS, Technical Tools Report, UML Diagrams (Class & Sequence), and Testing Strategy.
* `/demo` - KISS Web Application prototype[cite: 2].
* `/samples` - Test runs on provided class photos, student lists, and sample repositories[cite: 2].
