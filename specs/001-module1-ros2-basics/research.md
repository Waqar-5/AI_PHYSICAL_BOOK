# Research & Decisions for Module 1

This document records the key architectural and structural decisions for the AI Book project, as of Module 1.

## Docusaurus Structure

- **Decision**: The book will be a Docusaurus project. The main content will reside in the `docusaurus/docs` directory.
- **Rationale**: Docusaurus is excellent for documentation-heavy sites, provides a good structure for versioning, and is based on React, which allows for customization like the RAG chatbot integration.
- **Sidebar Organization**: The `sidebars.js` file will be configured to organize the book by modules, with each module containing its chapters. This will provide a clear, hierarchical navigation for the reader.
- **Folder Layout**: Each module will have its own subdirectory within `docusaurus/docs`. For example, `docusaurus/docs/module1`, `docusaurus/docs/module2`, etc.

## Module to Chapter Mapping

- **Decision**: Each module will consist of 2-3 chapters.
- **Rationale**: This keeps modules focused and digestible. It allows for a logical progression of topics within each module. For Module 1, the chapters will be:
    1.  ROS 2 Nodes and Topics
    2.  ROS 2 Services
    3.  Understanding Basic Humanoid URDFs

## Code Example Format and Testing

- **Decision**: Code examples will be written in Python using `rclpy` for ROS 2 Humble. They will be placed in a separate `examples/` directory at the root of the project, organized by module.
- **Rationale**: Separating code from documentation makes it easier to maintain and test the code. Readers can browse or download the examples easily.
- **Testing**: Code examples will be manually tested for correctness and reproducibility. Each example will include a `README.md` with instructions on how to run it.

## Chatbot Placement

- **Decision**: The RAG chatbot will be integrated as a floating action button or a dedicated component on the Docusaurus site.
- **Rationale**: This provides an unobtrusive way for readers to ask questions at any point while reading the book. The chatbot will be a React component, making it easy to integrate into Docusaurus.
- **UI/UX**: The chatbot interface will be simple: a text input for questions and a display area for answers. The answers will cite the source chapter in the book.

## Hosting

- **Decision**: The Docusaurus site will be built and deployed to GitHub Pages. The backend for the RAG chatbot will be hosted on a free-tier provider like Heroku or Vercel.
- **Rationale**: GitHub Pages is free and integrates seamlessly with GitHub repositories. A free-tier hosting for the backend is sufficient for the initial version of the chatbot.
