# Data Model for Module 1

This document outlines the key data entities for Module 1 of the AI Book.

## Entity: Chapter

- **Description**: A single chapter in the book. It is a standalone document that explains a specific concept.
- **Attributes**:
    - `title`: The title of the chapter.
    - `content`: The main body of the chapter in Markdown format.
    - `code_example`: A reference to a runnable code example.
    - `task`: A small assignment for the reader to complete.
- **Relationships**: A `Module` contains multiple `Chapters`.

## Entity: ROS 2 Node

- **Description**: A Python script that functions as a ROS 2 node.
- **Attributes**:
    - `name`: The name of the node.
    - `source_code`: The Python source code.
    - `dependencies`: A list of required ROS 2 packages and Python libraries.
- **Relationships**: A `Chapter` may have one or more `ROS 2 Nodes` as examples.

## Entity: URDF File

- **Description**: An XML file that describes the structure of a robot.
- **Attributes**:
    - `name`: The name of the robot model.
    - `xml_content`: The XML content of the URDF file.
- **Relationships**: A `Chapter` may reference a `URDF File` as an example.
