"""
=========================================================
Research Navigator
Knowledge Schema
Version : 2.0
=========================================================

This file defines the official schema used throughout the
entire project.

Every module imports constants from here instead of using
hardcoded strings.
"""

# =========================================================
# OBJECT TYPES
# =========================================================

TOPIC = "topic"
RESEARCHER = "researcher"
PAPER = "paper"


# =========================================================
# KNOWLEDGE QUALITY LEVELS
# =========================================================

QUALITY_LEVELS = [
    "Bronze",
    "Silver",
    "Gold",
    "Platinum",
    "Diamond"
]


# =========================================================
# TOPIC ROOT SECTIONS
# =========================================================

TOPIC_SECTIONS = [

    "identity",

    "learning",

    "history",

    "timeline",

    "researchers",

    "papers",

    "applications",

    "future",

    "faq",

    "relationships"

]


# =========================================================
# IDENTITY
# =========================================================

IDENTITY_FIELDS = [

    "name",

    "domain",

    "subdomain",

    "difficulty",

    "importance",

    "estimated_study_time",

    "quality_level",

    "version",

    "tags"

]


# =========================================================
# LEARNING
# =========================================================

LEARNING_FIELDS = [

    "overview",

    "why_it_matters",

    "intuition",

    "key_concepts",

    "prerequisites",

    "key_takeaways"

]


# =========================================================
# HISTORY
# =========================================================

HISTORY_FIELDS = [

    "problem_before",

    "historical_motivation",

    "impact_on_ai"

]


# =========================================================
# TIMELINE EVENT
# =========================================================

TIMELINE_FIELDS = [

    "year",

    "event",

    "researchers",

    "papers",

    "description",

    "impact"

]


# =========================================================
# RESEARCHER ENTRY
# =========================================================

RESEARCHER_FIELDS = [

    "name",

    "contribution",

    "importance"

]


# =========================================================
# PAPER ENTRY
# =========================================================

PAPER_FIELDS = [

    "title",

    "year",

    "authors",

    "summary",

    "importance"

]


# =========================================================
# APPLICATION ENTRY
# =========================================================

APPLICATION_FIELDS = [

    "field",

    "usage",

    "example"

]


# =========================================================
# FUTURE
# =========================================================

FUTURE_FIELDS = [

    "open_problems",

    "future_directions"

]


# =========================================================
# FAQ
# =========================================================

FAQ_FIELDS = [

    "question",

    "answer"

]


# =========================================================
# RELATIONSHIPS
# =========================================================

RELATIONSHIP_FIELDS = [

    "parent_topics",

    "child_topics",

    "related_topics"

]


# =========================================================
# KNOWLEDGE SCORE SECTIONS
# =========================================================

QUALITY_SECTIONS = [

    "Identity",

    "Learning",

    "History",

    "Timeline",

    "Researchers",

    "Papers",

    "Applications",

    "Future",

    "FAQ",

    "Relationships"

]
# =========================================================
# AI KNOWLEDGE ENGINE
# =========================================================

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


# =========================================================
# ENTITY TYPES
# =========================================================

class EntityType(str, Enum):

    TOPIC = "topic"

    RESEARCHER = "researcher"

    PAPER = "paper"

    DATASET = "dataset"

    ALGORITHM = "algorithm"

    LIBRARY = "library"

    FRAMEWORK = "framework"

    MODEL = "model"


# =========================================================
# USER ACTIONS
# =========================================================

class ActionType(str, Enum):

    EXPLAIN = "explain"

    DEFINE = "define"

    COMPARE = "compare"

    HISTORY = "history"

    TIMELINE = "timeline"

    RESEARCHERS = "researchers"

    PAPERS = "papers"

    APPLICATIONS = "applications"

    FUTURE = "future"

    LEARNING_PATH = "learning_path"

    PREREQUISITES = "prerequisites"

    SUMMARY = "summary"

    UNKNOWN = "unknown"


# =========================================================
# DETAIL LEVEL
# =========================================================

class DetailLevel(str, Enum):

    QUICK = "quick"

    BASIC = "basic"

    DETAILED = "detailed"

    RESEARCH = "research"


# =========================================================
# KNOWLEDGE ENTITY
# =========================================================

@dataclass(slots=True)
class Entity:
    """
    Entity identified in a user question.
    """

    entity_type: EntityType

    name: str

    confidence: float = 1.0

    aliases: List[str] = field(
        default_factory=list
    )

# =========================================================
# USER INTENT
# =========================================================

@dataclass(slots=True)
class Intent:
    """
    Result of intent resolution.
    """

    action: ActionType

    entities: List[Entity] = field(
        default_factory=list
    )

    requested_sections: List[str] = field(
        default_factory=list
    )

    detail_level: DetailLevel = DetailLevel.BASIC

    raw_question: str = ""

    confidence: float = 1.0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

# =========================================================
# RETRIEVAL PLAN
# =========================================================

@dataclass(slots=True)
class RetrievalPlan:
    """
    Retrieval instructions for the knowledge layer.
    """

    entities: List[Entity] = field(
        default_factory=list
    )

    sections: List[str] = field(
        default_factory=list
    )

    include_related_topics: bool = True

    include_researchers: bool = True

    include_papers: bool = True

    include_timeline: bool = True

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

# =========================================================
# TIMELINE EVENT
# =========================================================

@dataclass
class TimelineEvent:

    year: str

    title: str

    summary: str

    researchers: List[str] = field(default_factory=list)

    papers: List[str] = field(default_factory=list)

    importance: str = ""

    related_topics: List[str] = field(default_factory=list)

    next_questions: List[str] = field(default_factory=list)


# =========================================================
# KNOWLEDGE RESPONSE
# =========================================================

@dataclass(slots=True)
class KnowledgeResponse:
    """
    Final structured knowledge response.
    """

    answer: str

    timeline: List[TimelineEvent] = field(
        default_factory=list
    )

    researchers: List[Dict[str, Any]] = field(
        default_factory=list
    )

    papers: List[Dict[str, Any]] = field(
        default_factory=list
    )

    related_topics: List[str] = field(
        default_factory=list
    )

    suggested_questions: List[str] = field(
        default_factory=list
    )

    learning_path: List[str] = field(
        default_factory=list
    )

    confidence: float = 1.0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )
# =========================================================
# PUBLIC API
# =========================================================

__all__ = [

    "TOPIC",

    "RESEARCHER",

    "PAPER",

    "QUALITY_LEVELS",

    "TOPIC_SECTIONS",

    "IDENTITY_FIELDS",

    "LEARNING_FIELDS",

    "HISTORY_FIELDS",

    "TIMELINE_FIELDS",

    "RESEARCHER_FIELDS",

    "PAPER_FIELDS",

    "APPLICATION_FIELDS",

    "FUTURE_FIELDS",

    "FAQ_FIELDS",

    "RELATIONSHIP_FIELDS",

    "QUALITY_SECTIONS",

    "EntityType",

    "ActionType",

    "DetailLevel",

    "Entity",

    "Intent",

    "RetrievalPlan",

    "TimelineEvent",

    "KnowledgeResponse"

]