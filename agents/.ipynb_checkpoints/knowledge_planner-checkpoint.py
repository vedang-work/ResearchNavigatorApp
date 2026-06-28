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
from core.constants import *

from __future__ import annotations

from dataclasses import dataclass, field

from typing import (

    Dict,

    List,

    Optional

)

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

@dataclass
class KnowledgeBlock:
    """
    One educational unit planned by the
    Knowledge Planner.
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

    metadata: Dict = field(
        default_factory=dict
    )
# =========================================================
# PLANNER RESULT
# =========================================================

@dataclass
class PlannerResult:
    """
    Final educational plan.
    """

    entity: Optional[Entity]

    learning_profile: str = ""

    teaching_strategy: str = ""

    confidence: float = 0.0

    difficulty: str = "Medium"

    blocks: List[KnowledgeBlock] = field(
        default_factory=list
    )

    context: Dict = field(
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

    metadata: Dict = field(
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

                "KnowledgePlanner"

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

            if section == "identity":

                blocks.append(

                    self.make_block(

                        title="Topic Overview",

                        section="identity",

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

            elif section == "relationships":

                blocks.append(

                    self.make_block(

                        title="Related Topics",

                        section="relationships",

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

            if "relationships" not in existing_sections:

                blocks.append(

                    self.make_block(

                        title="Related Topics",

                        section="relationships",

                        priority=next_priority,

                        curiosity=True,

                        purpose="Knowledge Expansion"

                    )

                )

                next_priority += 1

        # ---------------------------------------------
        # Future Directions
        # ---------------------------------------------

        if intent.intent != SECTION_FUTURE:

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
        Infer the user's learning profile.

        Profiles
        --------
        beginner
        intermediate
        researcher
        """

        question = intent.normalized_question

        # -------------------------------
        # Research profile
        # -------------------------------

        research_keywords = [

            "research",

            "paper",

            "survey",

            "state of the art",

            "sota",

            "benchmark",

            "novel",

            "limitation",

            "future",

            "open problem"

        ]

        if any(

            keyword in question

            for keyword in research_keywords

        ):

            return "researcher"

        # -------------------------------
        # Beginner profile
        # -------------------------------

        beginner_keywords = [

            "what is",

            "meaning",

            "explain",

            "introduce",

            "overview",

            PROFILE_BEGINNER

        ]

        if any(

            keyword in question

            for keyword in beginner_keywords

        ):

            return PROFILE_BEGINNER

        # -------------------------------
        # Intermediate

        return "intermediate"


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

                    "identity",

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

            elif profile == "intermediate":

                if block.section == SECTION_APPLICATIONS:

                    block.priority -= 1

            # --------------------------

            elif profile == "researcher":

                if block.section in [

                    SECTION_RESEARCHERS,

                    SECTION_PAPERS,

                    SECTION_FUTURE

                ]:

                    block.priority -= 3

                elif block.section in [

                    "identity",

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
    
                add_visual("historical_timeline")
    
            # -----------------------------------------
            # Timeline
            # -----------------------------------------
    
            elif section == SECTION_TIMELINE:
    
                add_visual(SECTION_TIMELINE)
    
                add_visual("chronology")
    
            # -----------------------------------------
            # Researchers
            # -----------------------------------------
    
            elif section == SECTION_RESEARCHERS:
    
                add_visual("research_network")
    
            # -----------------------------------------
            # Papers
            # -----------------------------------------
    
            elif section == SECTION_PAPERS:
    
                add_visual("citation_graph")
    
            # -----------------------------------------
            # Relationships
            # -----------------------------------------
    
            elif section == "relationships":
    
                add_visual("knowledge_graph")
    
            # -----------------------------------------
            # Applications
            # -----------------------------------------
    
            elif section == SECTION_APPLICATIONS:
    
                add_visual("application_map")
    
            # -----------------------------------------
            # Comparison
            # -----------------------------------------
    
            elif section == SECTION_COMPARISON:
    
                add_visual("comparison_table")
    
            # -----------------------------------------
            # Learning Path
            # -----------------------------------------
    
            elif section == SECTION_LEARNING:
    
                add_visual("learning_path")
    
            # -----------------------------------------
            # Future
            # -----------------------------------------
    
            elif section == SECTION_FUTURE:
    
                add_visual("future_roadmap")
    
            # -----------------------------------------
            # Concepts
            # -----------------------------------------
    
            elif section == STRATEGY_CONCEPT_FIRST:
    
                add_visual("concept_map")
    
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

        if intent.intent == SECTION_HISTORY:

            return "historical_journey"

        if intent.intent == "research":

            return STRATEGY_RESEARCH

        if intent.intent == SECTION_APPLICATIONS:

            return "example_driven"

        if profile == "PROFILE_BEGINNER":

            return "concept_first"

        if profile == "researcher":

            return STRATEGY_RESEARCH

        return "guided_learning"

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
        Main planning pipeline.
        """

        entity = None

        if intent.entities:

            entity = intent.entities[0]

        blocks = self.build_default_blocks(

            intent

        )

        blocks = self.enrich_blocks(

            intent,

            blocks

        )

        profile = self.determine_learning_profile(

            intent

        )

        blocks = self.apply_learning_profile(

            profile,

            blocks

        )

        visuals = self.determine_visual_components(

            blocks

        )

        strategy = self.determine_teaching_strategy(

            intent,

            profile

        )

        questions = self.build_curiosity_prompts(

            entity

        )

        result = PlannerResult(

            entity=entity,

            blocks=blocks,

            context=context,

            retrieval_order=self.build_retrieval_order(

                blocks

            ),

            suggested_questions=questions,

            visual_components=visuals,

            result = PlannerResult(

                entity=entity,

                learning_profile=profile,

                teaching_strategy=strategy,

                blocks=blocks,

                context=context,

                retrieval_order=self.build_retrieval_order(

                    blocks

                ),

                suggested_questions=questions,

                visual_components=visuals,

                planner_notes=[

                    "Knowledge plan generated successfully."

                ]
            )
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

        if intent.intent == "learn":

            objectives.extend([

                "Understand the fundamental concepts.",

                "Develop intuitive understanding.",

                "Identify where the topic is used."

            ])

        elif intent.intent == SECTION_HISTORY:

            objectives.extend([

                "Understand how the field evolved.",

                "Identify important milestones.",

                "Recognize major contributors."

            ])

        elif intent.intent == "research":

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
        Estimate reading time in minutes.
        """

        return max(

            5,

            len(blocks) * 4

        )
    def estimate_difficulty(
        self,
        blocks: List[KnowledgeBlock]
    ) -> str:
        """
        Estimate difficulty based on the plan.
        """

        if len(blocks) <= 4:

            return "Easy"

        if len(blocks) <= 8:

            return "Medium"

        return "Hard"


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

        if entity.entity_type != "topic":

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
        result: PlannerResult,
        intent: Intent
    ) -> PlannerResult:
        """
        Add educational metadata.
        """

        result.learning_objectives = (

            self.build_learning_objectives(

                intent

            )

        )

        result.estimated_reading_time = (

            self.estimate_reading_time(

                result.blocks

            )

        )

        result.difficulty = (

            self.estimate_difficulty(

                result.blocks

            )

        )

        result.metadata = {

            "planner_version":

            "3.0",

            "generated":

                True

        }

        result.confidence = (

            self.planner_confidence(

                intent

            )

        )

        result.next_topics = (

            self.recommend_next_topics(

                result.entity

            )

        )

        return result


    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(
        self,
        intent: Intent
    ) -> PlannerResult:
        """
        Public execution API.
        """

        plan = self.build_plan(

            intent

        )

        return self.finalize_plan(

            plan,

            intent

        )

# =========================================================
# PUBLIC API
# =========================================================

__all__ = [

    "KnowledgeBlock",

    "PlannerResult",

    "KnowledgePlanner"

]