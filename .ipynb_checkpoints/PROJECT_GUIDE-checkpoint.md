# Research Navigator

# Project Development Guide

Version: 1.0

---

# Purpose

This document defines the development workflow, coding standards, project organization, and engineering practices for Research Navigator.

Its objective is to ensure that every future development session follows a consistent methodology regardless of who contributes to the project.

---

# Development Philosophy

Research Navigator is developed using an incremental engineering approach.

Every module follows the same lifecycle:

Idea

↓

Design

↓

Implementation

↓

Testing

↓

Freeze

↓

Next Module

Once a module is frozen, it should only be modified to fix bugs or introduce backward-compatible improvements.

---

# Project Structure

```

research_navigator/

│

├── README.md

├── SYSTEM_DESIGN.md

├── PROJECT_GUIDE.md

├── MASTER_PROMPT.md

├── DEVELOPMENT_ROADMAP.md

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

# Folder Responsibilities

## core/

Contains production Python code.

Current files

knowledge.py

database.py

No notebook should contain production logic.

---

## knowledge/

Stores all structured JSON knowledge.

Subfolders

topics/

researchers/

papers/

Every knowledge object is stored as an individual JSON file.

---

## notebooks/

Notebook files are used for

- Testing
- Experiments
- Debugging
- Demonstrations

Production code should always be moved into the core folder.

---

## data/

Contains

SQLite database

Future cache files

Temporary exports

Backups

---

## assets/

Stores

Images

Icons

Diagrams

Illustrations

Future UI resources

---

## outputs/

Stores generated outputs.

Examples

Reports

Graphs

Exports

Knowledge maps

---

# Coding Standards

Use

snake_case

for

Functions

Variables

File names

---

Use

PascalCase

for

Classes

---

Use

UPPER_CASE

for

Constants

---

Private helper functions begin with

_

Example

_build_path()

_read_json()

_validate_object()

---

# Python Guidelines

Every function should

- have a single responsibility
- contain a docstring
- avoid duplicated logic
- be reusable
- raise meaningful exceptions

Avoid

except:

pass

Instead

Raise informative exceptions whenever possible.

---

# Notebook Guidelines

Notebook responsibilities

Import modules

Run tests

Verify outputs

Prototype ideas

Notebook responsibilities do NOT include

Business logic

Large utility functions

Database implementation

Knowledge engine implementation

---

# Database Guidelines

SQLite is used only for

Fast indexing

Searching

Relationships

JSON files remain the source of truth.

Database should never replace JSON.

---

# Knowledge Object Workflow

Creating a new topic

↓

Create JSON

↓

Validate

↓

Save

↓

Synchronize Database

↓

Verify

↓

Freeze

---

# Testing Workflow

Every module must be tested before freezing.

Recommended order

Create

↓

Validate

↓

Save

↓

Load

↓

Search

↓

Update

↓

Delete

If all tests pass

↓

Freeze Module

---

# Versioning

Major updates

1.0

2.0

3.0

Minor updates

1.1

1.2

1.3

Patch releases

1.0.1

1.0.2

1.0.3

---

# Development Rules

Rule 1

One coding session should produce one completed deliverable.

---

Rule 2

Do not redesign completed modules without a valid technical reason.

---

Rule 3

Avoid duplicate implementations.

---

Rule 4

Every feature should be tested before freezing.

---

Rule 5

JSON remains the source of truth.

---

Rule 6

Database indexes knowledge.

It does not own knowledge.

---

Rule 7

Each module should have one clear responsibility.

---

Rule 8

Keep code readable.

Readability is more important than cleverness.

---

Rule 9

Document important engineering decisions.

Future developers should understand why something exists.

---

Rule 10

Build reusable components instead of writing one-time solutions.

---

# Git Workflow (Future)

Feature

↓

Test

↓

Commit

↓

Push

↓

Release

---

# Recommended Development Order

Phase 1

Knowledge Engine

Database Engine

---

Phase 2

Topics

Researchers

Papers

---

Phase 3

Knowledge Graph

Timeline

Search

---

Phase 4

Research Assistant

Ollama Integration

---

Phase 5

Streamlit Interface

Interactive Navigation

Visual Knowledge Tree

---

# Debugging Checklist

Before reporting a bug

Confirm

- Module imports successfully.
- JSON file exists.
- Database exists.
- Paths are correct.
- Required fields are present.
- Functions are tested independently.

---

# Documentation Policy

Every production module should include

Purpose

Responsibilities

Version

Docstrings

Meaningful comments where necessary

---

# Final Principle

Research Navigator should remain

Simple

Modular

Reusable

Maintainable

Scalable

Every engineering decision should move the project closer to these five goals.

---

Version

1.0