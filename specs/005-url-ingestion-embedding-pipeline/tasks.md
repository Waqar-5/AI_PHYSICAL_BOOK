# Tasks: URL Ingestion & Embedding Pipeline

## Feature Overview
A backend pipeline that fetches URLs, processes the content, generates embeddings, and stores them in Qdrant Cloud for retrieval and search capabilities.

## Implementation Strategy
MVP approach: Implement core functionality first (URL fetching, text processing, embedding, storage), then add error handling, security, and additional features.

## Dependencies
- Python 3.8+
- uv package manager
- Cohere API access
- Qdrant Cloud access

---

## Phase 1: Setup

- [X] T001 Create backend directory structure per implementation plan
- [X] T002 Initialize Python project with uv in backend directory
- [X] T003 Create requirements.txt with dependencies: requests, beautifulsoup4, cohere, qdrant-client, python-dotenv
- [X] T004 Create project configuration file config.py with constants
- [X] T005 Set up environment variables for Cohere and Qdrant credentials

## Phase 2: Foundational Components

- [X] T006 [P] Create URL fetcher module fetcher.py with basic HTTP request functionality
- [X] T007 [P] Create text processor module processor.py with basic text cleaning functionality
- [X] T008 [P] Create embedder module embedder.py with basic Cohere integration
- [X] T009 [P] Create storage module storage.py with basic Qdrant integration
- [X] T010 [P] Create data models for DocumentChunk and ProcessingJob in models.py

## Phase 3: [US1] URL Fetching with Security

- [X] T011 [US1] Implement URL validation in fetcher.py (scheme, format, private IP blocking)
- [X] T012 [US1] Add security checks to prevent SSRF in fetcher.py
- [X] T013 [US1] Implement timeout and retry logic in fetcher.py
- [X] T014 [US1] Add content type validation to fetcher.py
- [X] T015 [US1] Test URL fetching with various content types

## Phase 4: [US2] Text Cleaning and Chunking

- [X] T016 [US2] Implement HTML parsing and cleaning with BeautifulSoup in processor.py
- [X] T017 [US2] Add metadata extraction (title, description) to processor.py
- [X] T018 [US2] Implement text chunking algorithm with configurable size and overlap in processor.py
- [X] T019 [US2] Add chunk validation (min/max size) to processor.py
- [X] T020 [US2] Test text processing with sample HTML content

## Phase 5: [US3] Embedding Generation

- [X] T021 [US3] Configure Cohere client with API key from environment
- [X] T022 [US3] Implement embedding generation using embed-english-v3.0 model
- [X] T023 [US3] Add embedding validation and error handling
- [X] T024 [US3] Implement batch embedding generation for efficiency
- [X] T025 [US3] Test embedding generation with sample text chunks

## Phase 6: [US4] Storage in Qdrant Cloud

- [X] T026 [US4] Configure Qdrant client with cloud URL and API key
- [X] T027 [US4] Create document_chunks collection in Qdrant with 1024-dimensional vectors
- [X] T028 [US4] Implement chunk storage functionality in storage.py
- [X] T029 [US4] Add metadata storage (URL, chunk_index, source_domain) to storage.py
- [X] T030 [US4] Test data storage and retrieval from Qdrant Cloud

## Phase 7: [US5] End-to-End Pipeline

- [X] T031 [US5] Implement main() function in main.py to orchestrate the pipeline
- [X] T032 [US5] Connect URL fetcher → text processor → embedder → storage in main.py
- [X] T033 [US5] Add job tracking with ProcessingJob model
- [X] T034 [US5] Implement error handling and logging in main.py
- [X] T035 [US5] Test complete pipeline with sample URLs

## Phase 8: Polish & Cross-Cutting Concerns

- [X] T036 Add comprehensive error handling and logging throughout all modules
- [X] T037 Add input validation and sanitization to all components
- [ ] T038 Implement rate limiting and cost monitoring for API calls
- [ ] T039 Add unit tests for all core components
- [ ] T040 Document the code and add usage examples

---

## Dependencies Between User Stories
- US2 (Text Processing) depends on US1 (URL Fetching) - needs fetched content to process
- US3 (Embedding) depends on US2 (Text Processing) - needs cleaned text to embed
- US4 (Storage) depends on US3 (Embedding) - needs embeddings to store
- US5 (End-to-End) depends on US1, US2, US3, US4 - orchestrates all components

## Parallel Execution Examples
- T006-T009 can run in parallel (different modules: fetcher.py, processor.py, embedder.py, storage.py)
- T021-T025 can run in parallel after foundational components are complete (all in embedder.py)
- T026-T030 can run in parallel after foundational components are complete (all in storage.py)

## Independent Test Criteria
- US1: URL fetching works with various content types and security checks pass
- US2: Text cleaning removes HTML tags and chunking splits content appropriately
- US3: Embeddings are generated successfully and match expected dimensions
- US4: Data is stored in Qdrant Cloud and can be retrieved correctly
- US5: Complete pipeline executes without errors and stores results in Qdrant

## MVP Scope
Core functionality: Basic URL fetching → text cleaning → embedding generation → Qdrant storage with main() orchestrator (tasks T001-T035)