# Research Navigator

# System Design Document

Version: 1.0

---

# 1. Project Vision

Research Navigator is an AI-powered Knowledge Navigation System designed to help researchers understand a domain from its foundations to its latest advancements.

Instead of simply retrieving research papers or answering questions, the platform reconstructs the complete evolution of knowledge by connecting concepts, researchers, landmark papers, datasets, models, and historical events into an interactive research ecosystem.

The objective is to transform research from information retrieval into structured knowledge exploration.

---

# 2. Design Philosophy

The platform is built around five principles.

## 1. Knowledge before Answers

The system should help users understand a field rather than only answering isolated questions.

---

## 2. Historical Evolution

Every important concept has a history.

Researchers should understand:

- Why did this idea emerge?
- What problem existed before it?
- Who solved it?
- How did the field evolve?

---

## 3. Guided Exploration

Users should never feel lost.

Every topic should naturally suggest where to go next.

Learning becomes navigation rather than searching.

---

## 4. Modular Architecture

Each module performs one responsibility only.

Knowledge Engine

↓

Database Engine

↓

Knowledge Base

↓

Research Assistant

↓

User Interface

---

## 5. Local First AI

The platform is designed to work completely offline using locally hosted language models.

Current Models

- llama3.2:3b
- qwen3:4b

Future models may be added without changing the architecture.

---

# 3. System Architecture

```

                User

                  │

                  ▼

        Streamlit User Interface

                  │

                  ▼

         Research Assistant

          (Local Ollama LLM)

                  │

                  ▼

          Knowledge Engine

                  │

                  ▼

          Database Engine

                  │

                  ▼

        JSON Knowledge Objects

```

Each layer depends only on the layer beneath it.

---

# 4. Core Modules

## Knowledge Engine

Responsibilities

- Create knowledge objects
- Validate objects
- Save JSON
- Load JSON
- Search knowledge
- Update knowledge
- Delete knowledge

File

core/knowledge.py

Status

Completed

---

## Database Engine

Responsibilities

- SQLite database
- Object indexing
- Fast retrieval
- Relationship storage
- Synchronization

File

core/database.py

Status

In Development

---

## Knowledge Base

Contains structured JSON files representing the knowledge of the platform.

Current categories

- Topics
- Researchers
- Papers

Future categories

- Datasets
- Models
- Frameworks
- Companies
- Universities
- Conferences
- Journals
- Tools

---

## Research Assistant

Uses local language models to explain knowledge already stored inside the platform.

The assistant should retrieve structured knowledge before generating natural language explanations.

Retrieval First

↓

Generation Second

---

# 5. Knowledge Object Philosophy

Every knowledge object should answer the following questions.

What is it?

↓

Why was it created?

↓

What problem did it solve?

↓

Who contributed?

↓

Which papers changed the field?

↓

How did it evolve?

↓

Where can future researchers contribute?

---

# 6. Knowledge Navigation

Research Navigator supports multiple exploration paths.

## Topic Driven

Topic

↓

Timeline

↓

Researchers

↓

Papers

↓

Applications

↓

Open Problems

---

## Researcher Driven

Researcher

↓

Biography

↓

Timeline

↓

Contributions

↓

Papers

↓

Influenced Fields

---

## Paper Driven

Paper

↓

Historical Context

↓

Methodology

↓

Results

↓

Impact

↓

Future Work

---

## Timeline Driven

Timeline

↓

Historical Events

↓

Researchers

↓

Concepts

↓

Modern Research

---

# 7. Knowledge Tree

Knowledge is organized hierarchically.

Example

Mathematics

↓

Statistics

↓

Machine Learning

↓

Neural Networks

↓

Deep Learning

↓

Attention

↓

Transformers

↓

Large Language Models

Each node can be expanded independently.

Every node may contain unlimited depth.

---

# 8. Timeline Philosophy

Time provides context.

Every topic contains important milestones.

Each milestone connects

Year

↓

Researcher

↓

Paper

↓

Contribution

↓

Impact

Users should understand not only *what* happened but *why* it mattered.

---

# 9. Researcher Philosophy

Researchers are treated as first-class knowledge objects.

Each researcher contains

- Biography
- Timeline
- Contributions
- Papers
- Collaborators
- Awards
- Research Areas
- Influence

---

# 10. Paper Philosophy

Research papers are not stored as PDFs.

Instead, they are transformed into structured knowledge.

Each paper contains

- Motivation
- Problem Statement
- Methodology
- Key Contributions
- Results
- Limitations
- Future Work
- Related Papers

---

# 11. Database Design

SQLite acts as the indexing engine.

JSON remains the source of truth.

Workflow

JSON

↓

SQLite Index

↓

Fast Search

↓

Knowledge Retrieval

↓

Natural Language Explanation

---

# 12. Coding Principles

The project follows strict engineering practices.

- One responsibility per module.
- No duplicate business logic.
- Test before freeze.
- Freeze modules after validation.
- Backward-compatible improvements only.
- Clear documentation.
- Consistent naming conventions.

---

# 13. Development Workflow

Every feature follows the same lifecycle.

Idea

↓

Implementation

↓

Testing

↓

Freeze

↓

Next Sprint

Modules are only modified when necessary.

---

# 14. Current Progress

Completed

- Folder Structure
- Knowledge Engine
- JSON Storage
- Database Foundation

In Progress

- JSON Synchronization
- Knowledge Population

Upcoming

- Mathematics
- Statistics
- Machine Learning
- Researchers
- Papers
- Knowledge Graph
- Timeline Explorer
- Research Assistant
- Streamlit Interface

---

# 15. Long-Term Vision

Research Navigator aims to become a complete AI-powered research ecosystem capable of helping researchers

- understand unfamiliar domains,
- explore historical developments,
- discover landmark research,
- navigate knowledge hierarchies,
- identify research gaps,
- build structured learning paths,
- generate new research ideas.

The platform should function as an intelligent research mentor rather than a conventional search engine.

---

# Version History

Version 1.0

Initial system architecture established.