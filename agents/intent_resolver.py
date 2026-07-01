"""
=========================================================
Research Navigator

Intent Resolver

Version : 3.0

=========================================================

This module understands what the user wants.

It DOES NOT retrieve knowledge.

It DOES NOT call the LLM.

It only converts natural language into
a structured Intent object.

=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from typing import (

    Any,

    Dict,

    List,

    Optional

)

import re

import core.database as db


# =========================================================
# INTENT TYPES
# =========================================================

LEARN = "learn"

HISTORY = "history"

RESEARCH = "research"

APPLICATIONS = "applications"

FUTURE = "future"

COMPARE = "compare"

SEARCH = "search"

UNKNOWN = "unknown"


# =========================================================
# DETAIL LEVELS
# =========================================================

SUMMARY = "summary"

NORMAL = "normal"

DETAILED = "detailed"


# =========================================================
# INTENT OBJECT
# =========================================================

@dataclass(slots=True)
class Entity:
    """
    Entity identified inside a question.
    """

    name: str

    entity_type: str

    confidence: float = 1.0

    matched_by: str = "exact"

@dataclass(slots=True)
class Intent:
    """
    Structured output of the intent resolver.
    """

    raw_question: str

    normalized_question: str

    intent: str = UNKNOWN

    entities: List[Entity] = field(
        default_factory=list
    )

    sections: List[str] = field(
        default_factory=list
    )

    planner_hints: Dict[str, Any] = field(
        default_factory=dict
    )

    detail_level: str = NORMAL

    confidence: float = 0.0

    follow_up: bool = False

# =========================================================
# CONVERSATION STATE
# =========================================================

@dataclass(slots=True)
class ConversationState:
    """
    Tracks conversation context across turns.
    """

    current_entity: Optional[Entity] = None

    previous_entity: Optional[Entity] = None

    last_intent: Optional[str] = None

    mentioned_entities: List[Entity] = field(
        default_factory=list
    )

# =========================================================
# INTENT RESOLVER
# =========================================================

class IntentResolver:
    """
    Convert natural language into Intent.
    """

    def __init__(self):
        """
        Initialize the resolver and preload searchable entities.
        """
    
        self.state = ConversationState()
    
        self.topic_names = db.get_all_topic_names()
    
        self.researcher_names = db.get_all_researcher_names()
    
        self.paper_titles = db.get_all_paper_titles()
        
    # -----------------------------------------------------

    @staticmethod
    def normalize(
        question: str
    ) -> str:
        """
        Normalize text.
        """

        question = question.lower()

        question = re.sub(

            r"\s+",

            " ",

            question

        )

        return question.strip()
    # =====================================================
    # KEYWORD MAPS
    # =====================================================

    INTENT_KEYWORDS = {

        LEARN: [

            "what",
            "what is",
            "define",
            "meaning",
            "explain",
            "tell me",
            "introduce",
            "overview"

        ],

        HISTORY: [

            "history",
            "historical",
            "origin",
            "invent",
            "invented",
            "developed",
            "evolution",
            "timeline",
            "started"

        ],

        RESEARCH: [

            "research",
            "paper",
            "papers",
            "publication",
            "researcher",
            "scientist",
            "author"

        ],

        APPLICATIONS: [

            "application",
            "applications",
            "use",
            "uses",
            "real world",
            "industry",
            "where used"

        ],

        FUTURE: [

            "future",
            "next",
            "open problem",
            "research direction",
            "challenge",
            "limitation"

        ],

        COMPARE: [

            "compare",
            "difference",
            "vs",
            "versus",
            "better",
            "contrast"

        ]

    }

    # =====================================================
    # ENTITY DETECTION
    # =====================================================

    def detect_entities(
        self,
        question: str
    ) -> List[str]:
        """
        Detect entities mentioned in a question.

        Longest names are matched first.
        """

        text = self.normalize(question)

        entities = []

        # ---------------- Topics ----------------

        for topic in sorted(

            self.topic_names,

            key=len,

            reverse=True

        ):

            if topic.lower() in text:

                entities.append(topic)

        # ---------------- Researchers ----------------

        for researcher in sorted(

            self.researcher_names,

            key=len,

            reverse=True

        ):

            if researcher.lower() in text:

                entities.append(researcher)

        # ---------------- Papers ----------------

        for paper in sorted(

            self.paper_titles,

            key=len,

            reverse=True

        ):

            if paper.lower() in text:

                entities.append(paper)

        # Remove duplicates while preserving order

        unique = []

        seen = set()

        for entity in entities:

            if entity not in seen:

                unique.append(entity)

                seen.add(entity)

        return unique

    # =====================================================
    # FOLLOW-UP DETECTION
    # =====================================================

    FOLLOW_UP_WORDS = {

        "it",
        "its",
        "they",
        "them",
        "that",
        "those",
        "this",
        "these",
        "he",
        "she",
        "his",
        "her",
        "more"
    }

    def is_follow_up(
        self,
        question: str
    ) -> bool:
        """
        Determine whether this is likely
        a follow-up question.
        """

        words = set(

            self.normalize(question).split()

        )

        return any(

            word in words

            for word in self.FOLLOW_UP_WORDS

        )
    
    # =====================================================
    # INTENT DETECTION
    # =====================================================

    def detect_intent(
        self,
        question: str
    ) -> str:
        """
        Determine the user's primary intent.
        """
    
        text = self.normalize(question)
    
        best_intent = LEARN
    
        best_score = 0
    
        for intent, keywords in self.INTENT_KEYWORDS.items():
    
            score = sum(
    
                keyword in text
    
                for keyword in keywords
    
            )
    
            if score > best_score:
    
                best_score = score
    
                best_intent = intent
    
        return best_intent
        
    # =====================================================
    # SECTION DETECTION
    # =====================================================

    SECTION_KEYWORDS = {

        "overview": [

            "overview",
            "summary",
            "introduction",
            "intro",
            "about",
            "what is"

        ],

        "learning": [

            "learn",
            "concept",
            "intuition",
            "understand"

        ],

        "history": [

            "history",
            "historical",
            "origin",
            "invent",
            "invented",
            "developed"

        ],

        "timeline": [

            "timeline",
            "evolution",
            "chronology"

        ],

        "researchers": [

            "researcher",
            "scientist",
            "author",
            "who"

        ],

        "papers": [

            "paper",
            "publication",
            "journal",
            "article"

        ],

        "applications": [

            "application",
            "applications",
            "use",
            "uses",
            "industry",
            "real world"

        ],

        "future": [

            "future",
            "challenge",
            "limitation",
            "research direction"

        ],

        "faq": [

            "question",
            "faq"

        ],

        "relationships": [

            "related",
            "dependency",
            "prerequisite",
            "parent",
            "child"

        ]

    }


    # =====================================================
    # SECTION RESOLUTION
    # =====================================================

    def detect_sections(
        self,
        question: str,
        intent: str
    ) -> List[str]:
        """
        Determine which knowledge sections
        are required.
        """

        text = self.normalize(question)

        sections = []

        for section, keywords in self.SECTION_KEYWORDS.items():

            for keyword in keywords:

                if keyword in text:

                    sections.append(section)

                    break

        # -----------------------------------------
        # Intent defaults
        # -----------------------------------------

        if not sections:

            if intent == LEARN:

                sections.extend([

                    "identity",

                    "learning"

                ])

            elif intent == HISTORY:

                sections.extend([

                    "history",

                    "timeline"

                ])

            elif intent == RESEARCH:

                sections.extend([

                    "researchers",

                    "papers"

                ])

            elif intent == APPLICATIONS:

                sections.append(

                    "applications"

                )

            elif intent == FUTURE:

                sections.append(

                    "future"

                )

        # -----------------------------------------
        # Intelligent enrichment
        # -----------------------------------------

        if "history" in sections:

            if "timeline" not in sections:

                sections.append(

                    "timeline"

                )

        if "researchers" in sections:

            if "papers" not in sections:

                sections.append(

                    "papers"

                )

        if "applications" in sections:

            if "future" not in sections:

                sections.append(

                    "future"

                )

        # Remove duplicates

        unique = []

        seen = set()

        for section in sections:

            if section not in seen:

                unique.append(section)

                seen.add(section)

        return unique


    # =====================================================
    # DETAIL LEVEL
    # =====================================================

    def detect_detail_level(
        self,
        question: str
    ) -> str:
        """
        Estimate desired answer length.
        """

        text = self.normalize(question)

        if any(

            phrase in text

            for phrase in [

                "brief",

                "short",

                "quick",

                "summary"

            ]

        ):

            return SUMMARY

        if any(

            phrase in text

            for phrase in [

                "detailed",

                "deep",

                "complete",

                "everything",

                "comprehensive"

            ]

        ):

            return DETAILED

        return NORMAL

    # =====================================================
    # PLANNER HINTS
    # =====================================================

    def build_planner_hints(
        self,
        intent: str,
        sections: List[str]
    ) -> Dict[str, bool]:
        """
        Build planner hints.
        """
    
        hints = {
    
            "show_visual_timeline": False,
    
            "show_related_topics": True,
    
            "show_key_researchers": False,
    
            "show_landmark_papers": False,
    
            "encourage_follow_up": True
    
        }
    
        if "history" in sections:
    
            hints["show_visual_timeline"] = True
    
            hints["show_key_researchers"] = True
    
        if "timeline" in sections:
    
            hints["show_visual_timeline"] = True
    
        if "researchers" in sections:
    
            hints["show_key_researchers"] = True
    
        if "papers" in sections:
    
            hints["show_landmark_papers"] = True
    
        if intent != LEARN:
    
            hints["show_related_topics"] = False
    
        return hints
    
    # =====================================================
    # SMART ENTITY RESOLUTION
    # =====================================================

    def resolve_best_entity(
        self,
        question: str
    ) -> Optional[Entity]:
        """
        Resolve the best matching entity.

        Priority
        --------
        1. Exact match
        2. Topic search
        3. Researcher search
        4. Paper search
        5. Conversation memory
        """

        # -------------------------------------------------
        # Exact entity detection
        # -------------------------------------------------

        entities = self.detect_entities(question)

        name: Optional[str] = None
        
        if entities:
        
            name = entities[0]
        
        if name is not None:
        
            if db.topic_exists(name):
        
                return Entity(
                    name=name,
                    entity_type="topic",
                    confidence=1.0,
                    matched_by="exact"
                )
        
            if db.researcher_exists(name):
        
                return Entity(
                    name=name,
                    entity_type="researcher",
                    confidence=1.0,
                    matched_by="exact"
                )
        
            if db.paper_exists(name):
        
                return Entity(
                    name=name,
                    entity_type="paper",
                    confidence=1.0,
                    matched_by="exact"
                )
        
        # -------------------------------------------------
        # Topic search
        # -------------------------------------------------

        topics = db.search_topics(
            question,
            limit=1
        )

        if topics:

            return Entity(
                name=topics[0],
                entity_type="topic",
                confidence=0.85,
                matched_by="search"
            )

        # -------------------------------------------------
        # Researcher search
        # -------------------------------------------------

        researchers = db.search_researchers(
            question,
            limit=1
        )

        if researchers:

            return Entity(
                name=researchers[0],
                entity_type="researcher",
                confidence=0.80,
                matched_by="search"
            )

        # -------------------------------------------------
        # Paper search
        # -------------------------------------------------

        papers = db.search_papers(
            question,
            limit=1
        )

        if papers:

            return Entity(
                name=papers[0],
                entity_type="paper",
                confidence=0.80,
                matched_by="search"
            )

        # -------------------------------------------------
        # Follow-up resolution
        # -------------------------------------------------

        if self.is_follow_up(question):

            return self.state.current_entity

        return None

    # =====================================================
    # CONVERSATION MEMORY
    # =====================================================

    def update_state(
        self,
        intent: Intent
    ) -> None:
        """
        Update conversation memory.
        """
    
        self.state.last_intent = intent.intent
    
        if not intent.entities:
    
            return
    
        entity = intent.entities[0]
    
        self.state.previous_entity = self.state.current_entity
    
        self.state.current_entity = entity
    
        already_exists = any(
    
            e.name == entity.name
    
            and
    
            e.entity_type == entity.entity_type
    
            for e
    
            in self.state.mentioned_entities
    
        )
    
        if not already_exists:
    
            self.state.mentioned_entities.append(
    
                entity
    
            )
    
    # =====================================================
    # MAIN RESOLUTION PIPELINE
    # =====================================================

    def resolve(
        self,
        question: str
    ) -> Intent:
        """
        Resolve natural language into
        an Intent object.
        """
    
        normalized = self.normalize(
    
            question
    
        )
    
        intent_type = self.detect_intent(
    
            normalized
    
        )
    
        entity = self.resolve_best_entity(
    
            normalized
    
        )
    
        entities: List[Entity] = []
    
        confidence = 0.25
    
        if entity is not None:
    
            entities.append(
    
                entity
    
            )
    
            confidence = max(
    
                confidence,
    
                entity.confidence
    
            )
    
        sections = self.detect_sections(
    
            normalized,
    
            intent_type
    
        )
    
        detail = self.detect_detail_level(
    
            normalized
    
        )
    
        planner_hints = self.build_planner_hints(
    
            intent_type,
    
            sections
    
        )
    
        if len(sections) > 2:
    
            confidence += 0.05
    
        if detail == DETAILED:
    
            confidence += 0.05
    
        confidence = min(
    
            confidence,
    
            1.0
    
        )
    
        result = Intent(
    
            raw_question=question,
    
            normalized_question=normalized,
    
            intent=intent_type,
    
            entities=entities,
    
            sections=sections,
    
            planner_hints=planner_hints,
    
            detail_level=detail,
    
            confidence=confidence,
    
            follow_up=self.is_follow_up(
    
                normalized
    
            )
    
        )
    
        self.update_state(
    
            result
    
        )
    
        return result
    
    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        intent: Intent
    ) -> bool:
        """
        Validate resolved intent.
        """
    
        if not intent.intent:
    
            return False
    
        if intent.intent == UNKNOWN:
    
            return False
    
        if not intent.entities:
    
            return False
    
        return True

    # =====================================================
    # EXPLANATION
    # =====================================================

    def explain(
        self,
        intent: Intent
    ) -> Dict[str, Any]:
        """
        Return a human-readable explanation of
        how the resolver interpreted the query.
        """

        return {

            "question":

                intent.raw_question,

            "normalized":

                intent.normalized_question,

            "intent":

                intent.intent,

            "entities": [

                {

                    "name": entity.name,

                    "type": entity.entity_type,

                    "confidence": entity.confidence,

                    "matched_by": entity.matched_by

                }

                for entity in intent.entities

            ],

            "sections":

                intent.sections,

            "planner_hints":

                intent.planner_hints,

            "detail_level":

                intent.detail_level,

            "confidence":

                intent.confidence,

            "follow_up":

                intent.follow_up

        }

    # =====================================================
    # DEBUG
    # =====================================================

    def debug(
        self,
        question: str
    ) -> Dict[str, Any]:
        """
        Useful during notebook development.
        """

        result = self.resolve(question)

        return {

            "normalized":

                result.normalized_question,

            "intent":

                result.intent,

            "entities":

                [

                    (

                        entity.name,

                        entity.entity_type

                    )

                    for entity in result.entities

                ],
            "sections":

                result.sections,

            "planner_hints":

                result.planner_hints,

            "detail":

                result.detail_level,

            "confidence":

                result.confidence,

            "follow_up":

                result.follow_up,

            "valid":

                self.validate(result)

        }


    # =====================================================
    # RESET
    # =====================================================

    def reset(
        self
    ) -> None:
        """
        Reset conversation state.
        """
    
        self.state = ConversationState()

    # =====================================================
    # STATE
    # =====================================================

    def get_state(
        self
    ) -> ConversationState:
        """
        Return conversation state.
        """
    
        return self.state
    
# =========================================================
# PUBLIC API
# =========================================================

__all__ = [

    "Intent",

    "Entity",

    "ConversationState",

    "IntentResolver",

    "LEARN",

    "HISTORY",

    "RESEARCH",

    "APPLICATIONS",

    "FUTURE",

    "COMPARE",

    "SEARCH",

    "UNKNOWN",

    "SUMMARY",

    "NORMAL",

    "DETAILED"

]