# Data Model for Module 4 - Vision-Language-Action (VLA)

This module focuses on conceptual explanations of integrated systems and workflows rather than defining new data entities in a traditional software development sense. The "entities" here represent the key conceptual components involved in a Vision-Language-Action (VLA) system.

## Conceptual Entities

-   **Large Language Models (LLMs)**:
    -   **Description**: AI models capable of processing and generating human-like text. In VLA, used for natural language understanding, cognitive planning, and translating high-level commands into robot-executable actions.
    -   **Key Aspects**: Natural Language Understanding (NLU), reasoning, task decomposition, knowledge grounding.

-   **Humanoid Robot**:
    -   **Description**: The autonomous physical platform that receives and executes commands, interacts with the environment, and provides sensor feedback.
    -   **Key Aspects**: Actuators (manipulators, locomotion), sensors (cameras, microphones, proprioceptors), onboard computing.

-   **OpenAI Whisper**:
    -   **Description**: An automatic speech recognition (ASR) system. Used in VLA for converting spoken natural language commands into text.
    -   **Key Aspects**: High accuracy, multi-language support, robust to noise.

-   **ROS 2 Actions/Commands**:
    -   **Description**: The standard framework within ROS 2 for sending goals to an action server (e.g., a navigation stack or a manipulation controller) and receiving feedback and results.
    -   **Key Aspects**: Goal-oriented communication, feedback mechanisms, cancellation.

-   **Natural Language Commands**:
    -   **Description**: User input provided to the VLA system in human language (e.g., "Robot, go to the kitchen and get me a coffee").
    -   **Key Aspects**: Ambiguity, context-dependency, varied phrasing.

-   **Cognitive Planning**:
    -   **Description**: The process by which the LLM reasons about a high-level natural language command, breaks it down into sub-tasks, and generates a sequence of robot-executable actions.
    -   **Key Aspects**: Task decomposition, sequence generation, error handling (e.g., asking for clarification).

## Relationships

-   **Natural Language Commands** are transcribed by **OpenAI Whisper** into text.
-   **LLMs** process the text from **OpenAI Whisper**, perform **Cognitive Planning**, and translate it into a sequence of **ROS 2 Actions/Commands**.
-   **Humanoid Robot** executes **ROS 2 Actions/Commands**, performing tasks like navigation and manipulation.
-   The **Humanoid Robot** provides sensory feedback, which can inform subsequent **Cognitive Planning** by the **LLMs**.

## No Traditional Data Model

This `data-model.md` describes conceptual entities for understanding the module's subject matter. It does not define a database schema or API data structures.
