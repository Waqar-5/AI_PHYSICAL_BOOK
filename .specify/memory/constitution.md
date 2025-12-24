<!--
---
Sync Impact Report
---
- **Version change**: None → 1.0.0
- **Reason**: Initial creation of the project constitution.
- **Added Sections**:
  - Core Principles
  - Standards
  - Constraints
  - Success Criteria
- **Templates requiring review**:
  - `⚠ .specify/templates/plan-template.md`
  - `⚠ .specify/templates/spec-template.md`
  - `⚠ .specify/templates/tasks-template.md`
- **Follow-up TODOs**: None
-->
# AI Book + RAG Chatbot on Physical AI & Humanoid Robotics Constitution

## Core Principles

### I. Technical Accuracy
All robotics content, including concepts and code involving ROS 2, Gazebo, Unity, NVIDIA Isaac, and Vision-Language-Action (VLA) models, MUST be verified against official documentation and established best practices to ensure correctness.

### II. Clear, Intermediate-Level Explanations
Explanations MUST be tailored to an intermediate-level audience, comparable to Panaversity's AI-201/202 courses. Complex topics should be broken down into understandable segments without sacrificing essential technical depth.

### III. Spec-Driven Development
All development MUST follow the Spec-Kit Plus methodology. Features and modules will be formally specified before implementation begins, using Claude Code as the primary implementation assistant.

### IV. Reproducible Code and Simulations
All code examples, simulations, and chatbot behaviors MUST be reproducible. This includes providing runnable ROS 2 `rclpy` scripts, Gazebo worlds, NVIDIA Isaac Sim scripts, and FastAPI APIs, complete with versioned dependencies and setup instructions.

## Standards

- **Verification**: All technical content related to robotics MUST be cross-referenced with official documentation or primary sources.
- **Examples**: Runnable examples MUST be provided for all key concepts, including ROS 2 nodes, Gazebo worlds, Isaac Sim scripts, and FastAPI endpoints.
- **SDK Adherence**: The RAG chatbot implementation MUST adhere to the schemas and protocols defined by the OpenAI Agents/ChatKit SDK.
- **Tech Stack**: The backend MUST use Neon for storage and Qdrant for vector search.
- **Formatting**: All documentation and book content MUST maintain consistent formatting according to Docusaurus standards.

## Constraints

- **Scope**: The book MUST contain at least 40 sections distributed across 8 to 12 modules.
- **Content Structure**: Each section MUST include a conceptual summary, a corresponding code example, a text-described diagram, and a concluding assignment.
- **Chatbot Behavior**: The RAG chatbot MUST only source answers from the book's content or explicitly selected supplementary texts. It MUST be embedded within the Docusaurus-generated site.
- **Deployment**: The final book/site MUST be deployed on GitHub Pages, with the backend API running on a free-tier hosting provider.

## Success Criteria

- **Book Completion**: The full book is generated, formatted, and successfully deployed.
- **Chatbot Functionality**: The RAG chatbot is functional, accurate, and adheres to its content sourcing constraints.
- **Reproducibility**: All provided examples and simulations are runnable by following the documented instructions.
- **Capstone Project**: A final "Autonomous Humanoid" capstone project is documented end-to-end, integrating the concepts from the book.

## Governance

This constitution is the definitive guide for the project. All development activities, including documentation, code, and reviews, must align with its principles. Any deviation requires a formal amendment to this document, which must include a justification and be approved by the project lead.

**Version**: 1.0.0 | **Ratified**: 2025-12-10 | **Last Amended**: 2025-12-10