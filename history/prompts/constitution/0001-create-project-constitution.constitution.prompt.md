---
id: 0001
title: Create Project Constitution and Propagate Changes
stage: constitution
date: 2025-12-10
surface: agent
model: gemini
feature: none
branch: unknown
user: unknown
command: /sp.constitution
labels: ["constitution", "templates", "documentation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests:
  - none
---

## Prompt

/sp.constitution

Project: AI Book + RAG Chatbot on Physical AI & Humanoid Robotics

Core Principles:
- Technical accuracy (ROS 2, Gazebo, Unity, NVIDIA Isaac, VLA)
- Clear, intermediate-level explanations (Panaversity AI-201/202)
- Spec-driven development using Spec-Kit Plus + Claude Code
- Reproducible code, simulations, and chatbot behavior

Standards:
- Verify all robotics content with official docs
- Include runnable examples (ROS 2 rclpy, Gazebo worlds, Isaac scripts, FastAPI APIs)
- RAG chatbot must follow OpenAI Agents/ChatKit SDK schemas
- Neon + Qdrant must be used for storage + vector search
- Docusaurus formatting consistency across all modules

Constraints:
- Book: 40+ sections across 8–12 modules
- Each section: concept summary, code, diagram (text-described), assignment
- RAG chatbot: answers only from book or selected text; must be embedded in site
- Deployment: Docusaurus on GitHub Pages; backend on free-tier host

Success Criteria:
- Complete book generated and deployed
- RAG chatbot functional and accurate to book content
- All modules include runnable instructions
- Final “Autonomous Humanoid” capstone documented end-to-end

## Response snapshot

I have successfully created the project constitution and propagated the necessary changes to the project's templates.

## Outcome

- ✅ Impact: Created the initial project constitution (v1.0.0) and updated dependent templates to align with the new principles. This establishes the governance and standards for the project.
- 🧪 Tests: none
- 📁 Files: 
  - `.specify/memory/constitution.md` (Created)
  - `.specify/templates/plan-template.md` (Modified)
  - `.specify/templates/spec-template.md` (Modified)
  - `.specify/templates/tasks-template.md` (Modified)
- 🔁 Next prompts: The next logical step would be to start defining a feature using `/sp.specify`.
- 🧠 Reflection: The process demonstrated the importance of propagating constitutional changes to all dependent artifacts to ensure consistency. The inability to get git user/branch information without explicit approval highlights a security constraint.

## Evaluation notes (flywheel)

- Failure modes observed: The `git` command to retrieve user and branch name was not approved, requiring placeholders.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
