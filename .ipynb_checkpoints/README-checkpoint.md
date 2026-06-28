# 🚀 Research Navigator

> **An AI-powered Research Knowledge Navigation System**

---

# Vision

Research Navigator is an AI-assisted platform designed to help researchers understand a field from its very foundations rather than simply reading isolated research papers.

Instead of only answering questions, the system guides users through the historical evolution of knowledge, the researchers behind major discoveries, landmark papers, prerequisite concepts, and future research directions.

The ultimate goal is to help researchers understand **how knowledge evolved**, **why it evolved**, and **where future opportunities lie**.

---

# Problem Statement

Modern research is difficult because information is scattered across:

- Research papers
- Textbooks
- Documentation
- Blogs
- University courses
- Videos
- GitHub repositories

Researchers often know *what* to study but struggle to understand:

- Where did this idea originate?
- Why was it needed?
- Which problems did it solve?
- Which researchers contributed?
- Which papers changed the field?
- What remains unsolved?

Research Navigator aims to answer these questions through a structured knowledge navigation system.

---

# Objectives

The project aims to:

- Build a structured AI knowledge base.
- Organize concepts into hierarchical knowledge trees.
- Connect concepts using historical timelines.
- Connect researchers to their contributions.
- Connect landmark papers to research topics.
- Build relationships between domains.
- Provide guided learning paths.
- Enable AI-assisted research exploration.

---

# Core Philosophy

Research Navigator is **NOT**

- Wikipedia
- Google Scholar
- ChatGPT
- A Paper Search Engine

Research Navigator **IS**

- A Knowledge Navigation System
- A Research Exploration Platform
- A Historical AI Knowledge Graph
- An AI-powered Research Mentor

---

# Major Components

## Knowledge Engine

Responsible for:

- Creating knowledge objects
- Saving objects
- Loading objects
- Searching objects
- Managing JSON knowledge files

---

## Database Engine

Responsible for:

- SQLite database
- Fast search
- Object indexing
- Relationships
- Query execution

---

## Knowledge Base

Stores:

- Topics
- Researchers
- Papers

Each object is stored as JSON.

---

## Knowledge Tree

Represents prerequisite relationships.

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

Transformers

↓

Large Language Models

---

## Timeline Explorer

Shows the chronological evolution of research.

Example

1654

↓

1763

↓

1959

↓

1986

↓

2012

↓

2017

↓

2022

---

## Researcher Explorer

Shows

- Biography
- Timeline
- Major Contributions
- Landmark Papers
- Influence

---

## Paper Explorer

Shows

- Motivation
- Methodology
- Contributions
- Impact
- Limitations
- Future Work

---

## Research Assistant

Uses local Ollama models to explain the knowledge stored inside the project.

Current local models:

- llama3.2:3b
- qwen3:4b

Future models may be added without changing the project architecture.

---

# Current Technology Stack

Programming Language

- Python

Database

- SQLite

Development Environment

- Jupyter Notebook

Local LLM Runtime

- Ollama

Current Models

- Qwen3 4B
- Llama 3.2 3B

Future UI

- Streamlit

Knowledge Storage

- JSON

Version Control

- Git + GitHub

---

# Folder Structure

```
research_navigator/

│

├── core/

│ ├── knowledge.py

│ └── database.py

│

├── knowledge/

│ ├── topics/

│ ├── researchers/

│ └── papers/

│

├── notebooks/

│

├── data/

│

├── assets/

│

└── outputs/
```

---

# Development Workflow

Every feature follows the same workflow.

Idea

↓

Implementation

↓

Testing

↓

Freeze

↓

Next Sprint

Modules are frozen after successful testing and are only modified for bug fixes or backward-compatible improvements.

---

# Current Project Status

Completed

- Folder Structure
- Knowledge Engine
- Database Engine (Core)
- JSON Storage
- SQLite Integration

In Progress

- JSON → SQLite Synchronization
- Gold Standard Knowledge Nodes

Upcoming

- Mathematics
- Statistics
- Machine Learning
- Researchers
- Papers
- Knowledge Graph
- Timeline Explorer
- Research Assistant
- Streamlit UI

---

# Long-Term Vision

Research Navigator aims to become a complete AI-powered research companion capable of helping researchers:

- Understand unfamiliar domains
- Explore historical developments
- Discover landmark research
- Build structured learning paths
- Generate research ideas
- Identify research gaps
- Navigate entire research ecosystems

---

# License

This project is currently under active development.

Version

**0.1**