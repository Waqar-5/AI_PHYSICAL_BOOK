# Tasks: Module 1: ROS 2 Robotic Nervous System

**Input**: Design documents from `specs/001-module1-ros2-basics/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Per the constitution's principles of Technical Accuracy and Reproducibility, creating tests is strongly encouraged. Tasks for tests should be created for each user story.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Paths are relative to the project root unless specified.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for Docusaurus and examples.

- [X] T001 Create `docusaurus/` directory.
- [X] T002 Initialize Docusaurus project within `docusaurus/`.
- [X] T003 Create `docusaurus/docs/module1/` directory.
- [X] T004 Configure `docusaurus/sidebars.js` for Module 1 chapters.
- [X] T005 Configure `docusaurus/docusaurus.config.js` with basic settings.
- [X] T006 Create `examples/` directory.
- [X] T007 Create `examples/module1/` directory.

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No specific foundational tasks beyond initial setup for this module.

## Phase 3: User Story 1 - Learn ROS 2 Nodes and Topics (Priority: P1) 🎯 MVP

**Goal**: Students can understand and run basic ROS 2 node and topic examples.

**Independent Test**: The student can run the provided publisher and subscriber examples and see the messages being passed.

### Implementation for User Story 1

- [X] T008 [US1] Create `docusaurus/docs/module1/chapter1-nodes-topics.md`.
- [X] T009 [US1] Write explanation of ROS 2 nodes and topics in `docusaurus/docs/module1/chapter1-nodes-topics.md`.
- [X] T010 [US1] Create `examples/module1/nodes_topics/` directory.
- [X] T011 [US1] Create `examples/module1/nodes_topics/publisher.py`.
- [X] T012 [US1] Write Python code for publisher node in `examples/module1/nodes_topics/publisher.py`.
- [X] T013 [US1] Create `examples/module1/nodes_topics/subscriber.py`.
- [X] T014 [US1] Write Python code for subscriber node in `examples/module1/nodes_topics/subscriber.py`.
- [X] T015 [US1] Add a task for the reader in `docusaurus/docs/module1/chapter1-nodes-topics.md`.
- [X] T016 [US1] Create `examples/module1/nodes_topics/README.md` with instructions.
- [ ] T017 [US1] Test runnable examples for nodes and topics (`examples/module1/nodes_topics/publisher.py`, `examples/module1/nodes_topics/subscriber.py`).

## Phase 4: User Story 2 - Learn ROS 2 Services (Priority: P2)

**Goal**: Students can understand and run basic ROS 2 service examples.

**Independent Test**: The student can run the provided service server and client examples and see the client receive a response from the server.

### Implementation for User Story 2

- [X] T018 [US2] Create `docusaurus/docs/module1/chapter2-services.md`.
- [X] T019 [US2] Write explanation of ROS 2 services in `docusaurus/docs/module1/chapter2-services.md`.
- [X] T020 [US2] Create `examples/module1/services/` directory.
- [X] T021 [US2] Create `examples/module1/services/server.py`.
- [X] T022 [US2] Write Python code for service server in `examples/module1/services/server.py`.
- [X] T023 [US2] Create `examples/module1/services/client.py`.
- [X] T024 [US2] Write Python code for service client in `examples/module1/services/client.py`.
- [X] T025 [US2] Add a task for the reader in `docusaurus/docs/module1/chapter2-services.md`.
- [X] T026 [US2] Create `examples/module1/services/README.md` with instructions.
- [ ] T027 [US2] Test runnable examples for services (`examples/module1/services/server.py`, `examples/module1/services/client.py`).

## Phase 5: User Story 3 - Understand Basic Humanoid URDF (Priority: P3)

**Goal**: Students can understand the structure of a basic humanoid URDF file and visualize it.

**Independent Test**: The student can view the provided basic humanoid URDF in a viewer like RViz2 and identify the links and joints.

### Implementation for User Story 3

- [X] T028 [US3] Create `docusaurus/docs/module1/chapter3-urdf-basics.md`.
- [X] T029 [US3] Write explanation of basic humanoid URDF in `docusaurus/docs/module1/chapter3-urdf-basics.md`.
- [X] T030 [US3] Create `examples/module1/urdf_basics/` directory.
- [X] T031 [US3] Create `examples/module1/urdf_basics/simple_humanoid.urdf`.
- [X] T032 [US3] Write XML for a simple humanoid URDF in `examples/module1/urdf_basics/simple_humanoid.urdf`.
- [X] T033 [US3] Add a task for the reader in `docusaurus/docs/module1/chapter3-urdf-basics.md`.
- [X] T034 [US3] Create `examples/module1/urdf_basics/README.md` with instructions.
- [ ] T035 [US3] Test URDF visualization in RViz2 (`examples/module1/urdf_basics/simple_humanoid.urdf`).

## Phase 6: Documentation & Examples

**Purpose**: Ensure the feature aligns with the principles of Clarity and Reproducibility.

- [ ] T036 [US_ALL] Review all chapters in `docusaurus/docs/module1/` for clarity, technical accuracy, and Docusaurus compatibility.
- [X] T037 [US_ALL] Ensure all code examples have clear `README.md` files for setup and execution.
- [ ] T038 [US_ALL] Verify all tasks are well-defined within the chapters.

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final review and build verification.

- [X] T039 Perform a local Docusaurus build within `docusaurus/` and check for errors.
- [ ] T040 Verify Docusaurus build output visually.
- [ ] T041 Check for consistency between book content and RAG ingestion requirements (manual check).
- [X] T042 Ensure all files are correctly placed and named according to the project structure defined in plan.md.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: No specific tasks for this module.
- **User Stories (Phase 3+)**: All depend on Setup phase completion.
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Documentation & Examples (Phase 6)**: Depends on all User Story phases completion.
- **Polish (Phase 7)**: Depends on Documentation & Examples phase completion.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Setup (Phase 1) - No dependencies on other stories.
- **User Story 2 (P2)**: Can start after Setup (Phase 1) - May integrate with US1 but should be independently testable.
- **User Story 3 (P3)**: Can start after Setup (Phase 1) - May integrate with US1/US2 but should be independently testable.

### Within Each User Story

- Implementation tasks should be completed before testing.

### Parallel Opportunities

- Many tasks within each User Story phase can be run in parallel, especially file creation and initial content drafting. Code implementation and testing for different examples can also run in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 3: User Story 1
3. **STOP and VALIDATE**: Test User Story 1 independently (publisher/subscriber examples and chapter content).
4. Deploy/demo if ready.

### Incremental Delivery

1. Complete Setup → Foundation ready.
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!).
3. Add User Story 2 → Test independently → Deploy/Demo.
4. Add User Story 3 → Test independently → Deploy/Demo.
5. Complete Documentation & Examples.
6. Complete Polish & Cross-Cutting Concerns.
7. Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup together.
2. Once Setup is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently.
4. Team then collaborates on Documentation & Examples and Polish phases.

---

## Notes

- Tasks are designed to be immediately executable by an LLM.
- Each user story is independently completable and testable.
- Verify examples work after implementation.
- Commit after each task or logical group.
- Stop at any checkpoint to validate story independently.
