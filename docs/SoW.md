# Statement of Work (SoW)
**Project:** SmartClass — LLM-Ready Classroom Assistant (Ex2)  
**Course:** Introduction to Software Engineering (OOP / OOD), Ariel University  
**Author:** Guy Gersner  
**Target Delivery Date:** 25/11/2026  

---

## 1. Project Background & Purpose
Traditional classroom management and online learning platforms (such as Moodle and Zoom) suffer from cluttered user interfaces, manual overhead, and a lack of native AI capabilities[cite: 1]. The purpose of this project is to design and prototype an end-to-end, lightweight, KISS-compliant web application that streamlines live classroom attendance, real-time student engagement, lecture summarization, and automated LLM-assisted homework evaluation[cite: 1].

## 2. Scope of Work
This engagement prioritizes **software architecture, object-oriented design (OOD), and rapid AI-assisted prototyping (Vibe Coding)** over heavy custom infrastructure[cite: 1, 2].

### 2.1 In-Scope Deliverables
1. **Documentation & Architecture (`/docs`):**
   * Technical-Related Tools Report with real-life benchmarks on course datasets.
   * Statement of Work (SoW) and Software Requirements Specification (SRS)[cite: 2].
   * Primary Use Cases (Client Stories)[cite: 2].
   * High-level Component Architecture, Low-Level UML Class Diagrams, and Sequence Diagrams[cite: 2].
   * Class-mapped Testing Strategy[cite: 2].
2. **Working KISS Web Prototype (`/demo`):**
   * Mobile-friendly student web interface (no installation required)[cite: 1].
   * Lecturer dashboard supporting hybrid attendance tracking (QR/web check-in + classroom photo headcount) and `.xlsx`/`.csv` spreadsheet export[cite: 1].
   * Real-time student comments/suggestions feed and instant classroom polls[cite: 1].
   * ML/LLM modules for lecture recording summarization and peer-comparative homework repository review[cite: 1].
3. **Live Classroom Demonstration & Final Report:**
   * Live demo executed using the provided Ariel University course dataset (`courseid_130158_participants`, classroom photos, sample video, and student repositories)[cite: 2].
   * Final results summary in `README.md`[cite: 2].

### 2.2 Out-of-Scope (Exclusions)
* Direct API integration with Ariel University's Moodle, Zoom, or Personal Portal ("מידע אישי")[cite: 1].
* Enterprise authentication (SSO/LDAP), production cloud scaling, or custom deep-learning model training from scratch[cite: 1].

## 3. Milestones & Schedule

| Milestone | Deliverable | Target Date |
| :--- | :--- | :--- |
| **M1** | Repository initialization, `README.md` scope definition, and form submission[cite: 2] | 16/11/2026 |
| **M2** | Technical Tools Report & local benchmarks (`OpenCV` vs. Vision-LLM)[cite: 2] | 16/11/2026 |
| **M3** | SoW, SRS, Use Cases, and UML Diagrams (Class & Sequence)[cite: 2] | 19/11/2026 |
| **M4** | Testing Strategy & KISS Web Application prototype implementation[cite: 2] | 23/11/2026 |
| **M5** | Final verification, classroom demo readiness, and final conclusions[cite: 2] | 25/11/2026 |

## 4. Acceptance Criteria
* All design artifacts are cleanly documented and version-controlled in the public GitHub repository[cite: 2].
* The demo web application runs smoothly on mobile and desktop browsers without requiring external university system logins[cite: 1].
* Attendance export accurately maps check-ins to the 102-student course roster and reconciles with classroom photo headcounts[cite: 1, 2].