"""
=========================================================
Research Navigator

Knowledge Planner

Version : 3.0

=========================================================

Transforms a resolved Intent into an educational
knowledge plan.

This module decides

• What knowledge should be retrieved

• In what order

• Which sections deserve emphasis

• Which curiosity hooks to introduce

• Which visual elements should be shown

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

from core.constants import *

import core.database as db

from agents.intent_resolver import (
    Intent,
    Entity
)

# =========================================================
# LEARNING PROFILES
# =========================================================

PROFILE_BEGINNER = "beginner"

PROFILE_INTERMEDIATE = "intermediate"

PROFILE_RESEARCHER = "researcher"


# =========================================================
# TEACHING STRATEGIES
# =========================================================

STRATEGY_CONCEPT_FIRST = "concept_first"

STRATEGY_GUIDED = "guided_learning"

STRATEGY_HISTORICAL = "historical_journey"

STRATEGY_RESEARCH = "research_driven"

STRATEGY_EXAMPLE = "example_driven"

# =========================================================
# KNOWLEDGE BLOCK
# =========================================================

@dataclass(slots=True)
class KnowledgeBlock:
    """
    One educational retrieval unit.
    """

    title: str

    section: str

    priority: int

    purpose: str = ""

    source: str = SOURCE_DATABASE

    estimated_time: int = 2

    required: bool = True

    visual: bool = False

    curiosity: bool = False

    llm_required: bool = False

    database_required: bool = True

    depends_on: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

# =========================================================
# PLANNER RESULT
# =========================================================

@dataclass(slots=True)
class PlannerResult:
    """
    Final educational retrieval plan.
    """

    entity: Optional[Entity]

    learning_profile: str = ""

    teaching_strategy: str = ""

    confidence: float = 0.0

    difficulty: str = DIFFICULTY_MEDIUM

    blocks: List[KnowledgeBlock] = field(
        default_factory=list
    )

    context: Dict[str, Any] = field(
        default_factory=dict
    )

    retrieval_order: List[str] = field(
        default_factory=list
    )

    learning_objectives: List[str] = field(
        default_factory=list
    )

    suggested_questions: List[str] = field(
        default_factory=list
    )

    next_topics: List[str] = field(
        default_factory=list
    )

    visual_components: List[str] = field(
        default_factory=list
    )

    planner_notes: List[str] = field(
        default_factory=list
    )

    estimated_reading_time: int = 0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

# =========================================================
# KNOWLEDGE PLANNER
# =========================================================

class KnowledgePlanner:
    """
    Builds educational plans.
    """

    def __init__(self):
        """
        Initialize the knowledge planner.
        """
    
        pass
    
    # =====================================================
    # BLOCK FACTORY
    # =====================================================

    def make_block(
        self,
        title: str,
        section: str,
        priority: int,
        *,
        required: bool = True,
        visual: bool = False,
        curiosity: bool = False,
        purpose: str = ""
    ) -> KnowledgeBlock:
        """
        Create a standardized knowledge block.
        """

        return KnowledgeBlock(

            title=title,

            section=section,

            priority=priority,

            purpose=purpose,

            estimated_time=2,

            required=required,

            visual=visual,

            curiosity=curiosity,

            metadata={

                "generated_by":
            
                self.__class__.__name__
            
            }

        )

    # =====================================================
    # DEFAULT PLAN
    # =====================================================

    def build_default_blocks(
        self,
        intent: Intent
    ) -> List[KnowledgeBlock]:
        """
        Build the initial retrieval plan from
        the resolved intent.
        """

        blocks = []

        priority = 1

        for section in intent.sections:

            # -----------------------------------------

            if section == SECTION_IDENTITY:

                blocks.append(

                    self.make_block(

                        title="Topic Overview",

                        section=SECTION_IDENTITY,

                        priority=priority,

                        purpose="Core Understanding"

                    )

                )

            # -----------------------------------------

            elif section == SECTION_LEARNING:

                blocks.append(

                    self.make_block(

                        title="Learning Concepts",

                        section= SECTION_LEARNING,

                        priority=priority,

                        purpose="Core Understanding"

                    )

                )

            # -----------------------------------------

            elif section == SECTION_HISTORY:

                blocks.append(

                    self.make_block(

                        title="Historical Background",

                        section=SECTION_HISTORY,

                        priority=priority,

                        purpose="Historical Context"

                    )

                )

            # -----------------------------------------

            elif section == SECTION_TIMELINE:

                blocks.append(

                    self.make_block(

                        title="Evolution Timeline",

                        section=SECTION_TIMELINE,

                        priority=priority,

                        visual=True,

                        purpose="Historical Context"

                    )

                )

            # -----------------------------------------

            elif section == SECTION_RESEARCHERS:

                blocks.append(

                    self.make_block(

                        title="Important Researchers",

                        section=SECTION_RESEARCHERS,

                        priority=priority,

                        purpose="Research Foundation"

                    )

                )

            # -----------------------------------------

            elif section == SECTION_PAPERS:

                blocks.append(

                    self.make_block(

                        title="Landmark Papers",

                        section=SECTION_PAPERS,

                        priority=priority,

                        purpose="Research Foundation"

                    )

                )

            # -----------------------------------------

            elif section == SECTION_APPLICATIONS:

                blocks.append(

                    self.make_block(

                        title="Applications",

                        section= SECTION_APPLICATIONS,

                        priority=priority,

                        purpose="Real World"

                    )

                )

            # -----------------------------------------

            elif section == SECTION_FUTURE:

                blocks.append(

                    self.make_block(

                        title="Future Directions",

                        section=SECTION_FUTURE,

                        priority=priority,

                        curiosity=True,

                        purpose="Future Research"

                    )

                )

            # -----------------------------------------

            elif section == SECTION_RELATIONSHIPS:

                blocks.append(

                    self.make_block(

                        title="Related Topics",

                        section=SECTION_RELATIONSHIPS,

                        priority=priority,

                        curiosity=True,

                        purpose="Knowledge Expansion"

                    )

                )

            priority += 1

        return blocks
    # =====================================================
    # EDUCATIONAL ENRICHMENT
    # =====================================================

    def enrich_blocks(
        self,
        intent: Intent,
        blocks: List[KnowledgeBlock]
    ) -> List[KnowledgeBlock]:
        """
        Improve the learning experience by
        automatically adding useful educational
        blocks.
        """

        existing_sections = {

            block.section

            for block in blocks

        }

        next_priority = len(blocks) + 1

        hints = intent.planner_hints

        # ---------------------------------------------
        # Visual Timeline
        # ---------------------------------------------

        if hints.get(

            "show_visual_timeline",

            False

        ):

            if SECTION_TIMELINE not in existing_sections:

                blocks.append(

                    self.make_block(

                        title="Evolution Timeline",

                        section=SECTION_TIMELINE,

                        priority=next_priority,

                        visual=True,

                        purpose="Historical Context"

                    )

                )

                next_priority += 1

        # ---------------------------------------------
        # Key Researchers
        # ---------------------------------------------

        if hints.get(

            "show_key_researchers",

            False

        ):

            if SECTION_RESEARCHERS not in existing_sections:

                blocks.append(

                    self.make_block(

                        title="Important Researchers",

                        section=SECTION_RESEARCHERS,

                        priority=next_priority,

                        purpose="Research Foundation"

                    )

                )

                next_priority += 1

        # ---------------------------------------------
        # Landmark Papers
        # ---------------------------------------------

        if hints.get(

            "show_landmark_papers",

            False

        ):

            if SECTION_PAPERS not in existing_sections:

                blocks.append(

                    self.make_block(

                        title="Landmark Papers",

                        section=SECTION_PAPERS,

                        priority=next_priority,

                        purpose="Research Foundation"

                    )

                )

                next_priority += 1

        # ---------------------------------------------
        # Related Topics
        # ---------------------------------------------

        if hints.get(

            "show_related_topics",

            True

        ):

            if SECTION_RELATIONSHIPS not in existing_sections:

                blocks.append(

                    self.make_block(

                        title="Related Topics",

                        section=SECTION_RELATIONSHIPS,

                        priority=next_priority,

                        curiosity=True,

                        purpose="Knowledge Expansion"

                    )

                )

                next_priority += 1

        # ---------------------------------------------
        # Future Directions
        # ---------------------------------------------

        if SECTION_FUTURE not in existing_sections:

            blocks.append(

                self.make_block(

                    title="Future Research",

                    section= SECTION_FUTURE,

                    priority=next_priority,

                    curiosity=True,

                    purpose="Curiosity Trigger"

                )

            )

        return sorted(

            blocks,

            key=lambda block: block.priority

        )


    # =====================================================
    # RETRIEVAL ORDER
    # =====================================================

    def build_retrieval_order(
        self,
        blocks: List[KnowledgeBlock]
    ) -> List[str]:
        """
        Return retrieval order.
        """

        return [

            block.section

            for block in sorted(

                blocks,

                key=lambda block: block.priority

            )

        ]
    # =====================================================
    # LEARNING PROFILE
    # =====================================================

    def determine_learning_profile(
        self,
        intent: Intent
    ) -> str:
        """
        Determine the learner profile.
        """
    
        if intent.intent == RESEARCH:
    
            return PROFILE_RESEARCHER
    
        if intent.intent == LEARN:
    
            return PROFILE_BEGINNER
    
        return PROFILE_INTERMEDIATE

    # =====================================================
    # PROFILE ENRICHMENT
    # =====================================================

    def apply_learning_profile(
        self,
        profile: str,
        blocks: List[KnowledgeBlock]
    ) -> List[KnowledgeBlock]:
        """
        Adjust retrieval priorities based on
        learning profile.
        """

        for block in blocks:

            # --------------------------

            if profile == PROFILE_BEGINNER:

                if block.section in [

                    SECTION_IDENTITY,

                    SECTION_LEARNING

                ]:

                    block.priority -= 2

                elif block.section == SECTION_TIMELINE:

                    block.priority -= 1

                elif block.section == SECTION_RESEARCHERS:

                    block.priority += 1

                elif block.section == SECTION_PAPERS:

                    block.priority += 2

            # --------------------------

            elif profile == PROFILE_INTERMEDIATE:

                if block.section == SECTION_APPLICATIONS:

                    block.priority -= 1

            # --------------------------

            elif profile == PROFILE_RESEARCHER:

                if block.section in [

                    SECTION_RESEARCHERS,

                    SECTION_PAPERS,

                    SECTION_FUTURE

                ]:

                    block.priority -= 3

                elif block.section in [

                    SECTION_IDENTITY,

                    SECTION_LEARNING

                ]:

                    block.priority += 2

        blocks.sort(

            key=lambda block: block.priority

        )

        return blocks

    # =====================================================
    # VISUAL COMPONENTS
    # =====================================================
    
    def determine_visual_components(
        self,
        blocks: List[KnowledgeBlock]
    ) -> List[str]:
        """
        Determine which visual components should be
        generated for the current learning plan.
    
        Duplicate visualizations are automatically
        removed while preserving order.
        """
    
        visuals = []
    
        seen = set()
    
        def add_visual(name: str):
            if name not in seen:
                visuals.append(name)
                seen.add(name)
    
            for block in blocks:
        
                section = block.section.lower()
        
                # -----------------------------------------
                # History
                # -----------------------------------------
        
                if section == SECTION_HISTORY:
        
                    add_visual(VISUAL_HISTORY)
        
                # -----------------------------------------
                # Timeline
                # -----------------------------------------
        
                elif section == SECTION_TIMELINE:
        
                    add_visual(VISUAL_TIMELINE)
        
                    add_visual(VISUAL_CHRONOLOGY)
        
                # -----------------------------------------
                # Researchers
                # -----------------------------------------
        
                elif section == SECTION_RESEARCHERS:
        
                    add_visual(VISUAL_RESEARCH_NETWORK)
        
                # -----------------------------------------
                # Papers
                # -----------------------------------------
        
                elif section == SECTION_PAPERS:
        
                    add_visual(VISUAL_CITATION_GRAPH)
        
                # -----------------------------------------
                # Relationships
                # -----------------------------------------
        
                elif section == SECTION_RELATIONSHIPS:
        
                    add_visual(VISUAL_KNOWLEDGE_GRAPH)
        
                # -----------------------------------------
                # Applications
                # -----------------------------------------
        
                elif section == SECTION_APPLICATIONS:
        
                    add_visual(VISUAL_APPLICATION_MAP)
        
                # -----------------------------------------
                # Comparison
                # -----------------------------------------
        
                elif section == SECTION_COMPARISON:
        
                    add_visual(VISUAL_COMPARISON_TABLE)
        
                # -----------------------------------------
                # Learning Path
                # -----------------------------------------
        
                elif section == SECTION_LEARNING:
        
                    add_visual(VISUAL_LEARNING_PATH)
        
                # -----------------------------------------
                # Future
                # -----------------------------------------
        
                elif section == SECTION_FUTURE:
        
                    add_visual(VISUAL_FUTURE_ROADMAP)
        
                # -----------------------------------------
                # Concepts
                # -----------------------------------------
        
                elif section == STRATEGY_CONCEPT_FIRST:
        
                    add_visual(VISUAL_CONCEPT_MAP)
        
            return visuals
   
    # =====================================================
    # TEACHING STRATEGY
    # =====================================================

    def determine_teaching_strategy(
        self,
        intent: Intent,
        profile: str
    ) -> str:
        """
        Decide how the topic should be taught.
        """

        if SECTION_HISTORY in intent.sections:

            return "historical_journey"

        if intent.intent == RESEARCH:

            return STRATEGY_RESEARCH

        if SECTION_APPLICATIONS in intent.sections:

            return STRATEGY_EXAMPLE

        if profile == PROFILE_BEGINNER:

            return STRATEGY_CONCEPT_FIRST

        if profile == PROFILE_RESEARCHER:

            return STRATEGY_RESEARCH

        return STRATEGY_GUIDED

    # =====================================================
    # CURIOUSITY PROMPTS
    # =====================================================

    def build_curiosity_prompts(
        self,
        entity: Entity
    ) -> List[str]:
        """
        Generate follow-up questions.
        """

        if entity is None:

            return []

        return [

            f"What is the history of {entity.name}?",

            f"Who are the important researchers in {entity.name}?",

            f"What are the major applications of {entity.name}?",

            f"What are the future directions of {entity.name}?",

            f"Which topics should I study after {entity.name}?"

        ]


    # =====================================================
    # BUILD COMPLETE PLAN
    # =====================================================

    def build_plan(
        self,
        intent: Intent
    ) -> PlannerResult:
        """
        Build the educational retrieval plan.
        """
    
        entity = (
    
            intent.entities[0]
    
            if intent.entities
    
            else None
    
        )
    
        profile = self.determine_learning_profile(

            intent
        
        )
        
        blocks = self.build_default_blocks(
        
            intent
        
        )
        
        blocks = self.enrich_blocks(
        
            intent,
        
            blocks
        
        )
        
        blocks = self.apply_learning_profile(
        
            profile,
        
            blocks
        
        )
        
        difficulty = self.determine_difficulty(
        
            blocks
        
        )
        
        strategy = self.determine_teaching_strategy(
        
            intent,
        
            profile
        
        )
        
        visuals = self.determine_visual_components(
        
            blocks
        
        )
    
        retrieval_order = [
    
            block.section
    
            for block
    
            in sorted(
    
                blocks,
    
                key=lambda b: b.priority
    
            )
    
        ]
    
        context = {}
    
        result = PlannerResult(
    
            entity=entity,
    
            learning_profile=profile,
    
            teaching_strategy=strategy,
    
            confidence=intent.confidence,
    
            difficulty=difficulty,
    
            blocks=blocks,
    
            context=context,
    
            retrieval_order=retrieval_order,
    
            visual_components=visuals
    
        )
    
        return result
        
    # =====================================================
    # LEARNING OBJECTIVES
    # =====================================================

    def build_learning_objectives(
        self,
        intent: Intent
    ) -> List[str]:
        """
        Build learning objectives.
        """

        objectives = []

        if intent.intent == LEARN:

            objectives.extend([

                "Understand the fundamental concepts.",

                "Develop intuitive understanding.",

                "Identify where the topic is used."

            ])

        if SECTION_HISTORY in intent.sections:

            objectives.extend([

                "Understand how the field evolved.",

                "Identify important milestones.",

                "Recognize major contributors."

            ])

        elif intent.intent == RESEARCH:

            objectives.extend([

                "Study landmark publications.",

                "Identify active research areas.",

                "Understand current challenges."

            ])

        else:

            objectives.append(

                "Develop a deeper understanding."

            )

        return objectives


    # =====================================================
    # ESTIMATED STUDY TIME
    # =====================================================

    def estimate_reading_time(
        self,
        blocks: List[KnowledgeBlock]
    ) -> int:
        """
        Estimate total reading time in minutes.
        """
    
        return sum(
    
            block.estimated_time
    
            for block
    
            in blocks
    
        )
    def determine_difficulty(
        self,
        blocks: List[KnowledgeBlock]
    ) -> str:
        """
        Estimate learning difficulty.
        """
    
        if len(blocks) <= 4:
    
            return DIFFICULTY_EASY
    
        if len(blocks) <= 8:
    
            return DIFFICULTY_MEDIUM
    
        return DIFFICULTY_HARD

    # =====================================================
    # CONFIDENCE
    # =====================================================

    def planner_confidence(
        self,
        intent: Intent
    ) -> float:
        """
        Estimate planner confidence.
        """

        if not intent.entities:

            return 0.4

        return min(

            1.0,

            intent.confidence

        )


    # =====================================================
    # NEXT TOPICS
    # =====================================================

    def recommend_next_topics(
        self,
        entity: Optional[Entity]
    ) -> List[str]:
        """
        Recommend next topics.

        Uses relationship graph.
        """

        if entity is None:

            return []

        if entity.entity_type != ENTITY_TOPIC:

            return []

        related = db.get_related_topics(

            entity.name

        )

        children = db.get_child_topics(

            entity.name

        )

        recommendations = []

        seen = set()

        recommendations.extend(

            related

        )

        recommendations.extend(

            children

        )

        # remove duplicates
        
        unique = []

        for topic in recommendations:

            if not topic:

                continue

            normalized = topic.strip()

            if normalized in seen:

                continue

            unique.append(

                normalized

            )

            seen.add(

                normalized

            )

        return unique

    # =====================================================
    # ENRICH RESULT
    # =====================================================

    def finalize_plan(
        self,
        plan: PlannerResult
    ) -> PlannerResult:
        """
        Finalize the retrieval plan.
        """
    
        #
        # Estimated reading time
        #
    
        plan.estimated_reading_time = self.estimate_reading_time(

            plan.blocks
        
        )
    
        #
        # Retrieval order
        #
    
        plan.retrieval_order = [
    
            block.section
    
            for block
    
            in sorted(
    
                plan.blocks,
    
                key=lambda block: block.priority
    
            )
    
        ]
    
        #
        # Planner metadata
        #
    
        plan.metadata.update(
    
            {
    
                "planner":
    
                    self.__class__.__name__,
    
                "block_count":
    
                    len(plan.blocks)
    
            }
    
        )
    
        return plan

    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(
        self,
        intent: Intent
    ) -> PlannerResult:
        """
        Execute the complete planning pipeline.
        """
    
        plan = self.build_plan(
    
            intent
    
        )
    
        plan = self.finalize_plan(
    
            plan
    
        )
    
        return plan
    
# =========================================================
# PUBLIC API
# =========================================================

__all__ = [

    "KnowledgeBlock",

    "PlannerResult",

    "KnowledgePlanner"

]