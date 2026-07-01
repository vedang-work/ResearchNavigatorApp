"""
=========================================================
Research Navigator

Context Builder

Version : 3.0

=========================================================

Retrieves knowledge required by the planner.

This module knows

• where information comes from

• how to merge it

• how to validate it

It does NOT

• detect intent

• build prompts

• call the LLM

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

import core.database as db

from agents.intent_resolver import (

    Entity

)

from agents.knowledge_planner import (

    PlannerResult,

    KnowledgeBlock

)


# =========================================================
# CONTEXT ITEM
# =========================================================

@dataclass(slots=True)
class ContextItem:
    """
    One retrieved knowledge item.
    """

    entity: Entity

    section: str

    data: Any

    source: str = "database"

    confidence: float = 1.0

    retrieved: bool = True

    metadata: Dict[str, Any] = field(

        default_factory=dict

    )

# =========================================================
# CONTEXT RESULT
# =========================================================

@dataclass(slots=True)
class RetrievalStatistics:
    """
    Statistics produced during retrieval.
    """

    total_blocks: int = 0

    retrieved_blocks: int = 0

    failed_blocks: int = 0

    retrieval_rate: float = 0.0

    valid: bool = False

    missing_sections: List[str] = field(
        default_factory=list
    )

    summary: Dict[str, Dict[str, Any]] = field(
        default_factory=dict
    )


# =========================================================

@dataclass(slots=True)
class ContextResult:
    """
    Complete retrieved context.
    """

    entity: Optional[Entity]

    items: List[ContextItem] = field(
        default_factory=list
    )

    merged_context: Dict[str, Any] = field(
        default_factory=dict
    )

    statistics: RetrievalStatistics = field(
        default_factory=RetrievalStatistics
    )

    warnings: List[str] = field(
        default_factory=list
    )

# =====================================================
# DATABASE RETRIEVER
# =====================================================

class BaseRetriever:
    """
    Base class for every retriever.
    """

    def retrieve(
        self,
        entity: Entity,
        section: str
    ) -> Any:
        """
        Retrieve one section.
        """
    
        raise NotImplementedError

class DatabaseRetriever(
    BaseRetriever
):
    """
    Retrieves knowledge from the local
    Research Navigator database.
    """

    def retrieve(
        self,
        entity: Entity,
        section: str
    ) -> Any:
        """
        Retrieve one section from the database.
        """
    
        result = db.get_entity_section(
        
            entity.entity_type,
        
            entity.name,
        
            section,
        
            {}
        
        )
        
        return result

# =====================================================
# CONTEXT BUILDER
# =====================================================

class ContextBuilder:
    """
    Retrieves educational context from one
    or more retrievers.
    """

    def __init__(self):
        """
        Initialize retrievers.
        """
    
        self.database = DatabaseRetriever()

    # -------------------------------------------------

    def retrieve_block(
        self,
        entity: Entity,
        block: KnowledgeBlock
    ) -> ContextItem:
        """
        Retrieve one knowledge block.
        """

        data = self.database.retrieve(

            entity,

            block.section

        )

        retrieved = data not in (

            None,

            {},

            []

        )

        return ContextItem(

            entity=entity,

            section=block.section,

            data=data,

            source=block.source,

            confidence=1.0 if retrieved else 0.0,

            retrieved=retrieved,

            metadata={

                "priority":

                    block.priority,

                "purpose":

                    block.purpose,

                "visual":

                    block.visual,

                "curiosity":

                    block.curiosity

            }

        )

    # =====================================================
    # SAFE RETRIEVAL
    # =====================================================

    def safe_retrieve(
        self,
        entity: Entity,
        block: KnowledgeBlock
    ) -> ContextItem:
        """
        Retrieve a knowledge block safely.
        """
    
        try:
    
            return self.retrieve_block(
    
                entity,
    
                block
    
            )
    
        except Exception as error:
    
            return ContextItem(
    
                entity=entity,
    
                section=block.section,
    
                data={},
    
                source=block.source,
    
                confidence=0.0,
    
                retrieved=False,
    
                metadata={
    
                    "error": str(error),
    
                    "priority": block.priority,
    
                    "purpose": block.purpose,
    
                    "exception": error.__class__.__name__
    
                }
    
            )

    # =====================================================
    # SAFE BLOCK RETRIEVAL
    # =====================================================

    def retrieve_blocks_safe(
        self,
        planner: PlannerResult
    ) -> List[ContextItem]:
        """
        Retrieve every block while tolerating
        retrieval failures.
        """

        if planner.entity is None:

            return []

        items = []

        for block in planner.blocks:

            items.append(

                self.safe_retrieve(

                    planner.entity,

                    block

                )

            )

        return items


    # =====================================================
    # MERGE CONTEXT
    # =====================================================

    def merge_context(
        self,
        items: List[ContextItem]
    ) -> Dict[str, Any]:
        """
        Merge retrieved items into one context
        dictionary.
        """

        merged = {}

        for item in items:

            if not item.retrieved:

                continue

            merged[

                item.section

            ] = item.data

        return merged


    # =====================================================
    # CONTEXT WARNINGS
    # =====================================================

    def collect_warnings(
        self,
        items: List[ContextItem]
    ) -> List[str]:
        """
        Collect retrieval warnings.
        """
    
        warnings = []
    
        seen = set()
    
        for item in items:
    
            if item.retrieved:
    
                continue
    
            error = item.metadata.get(
    
                "error",
    
                "Unknown retrieval error"
    
            )
    
            message = (
    
                f"{item.section}: {error}"
    
            )
    
            if message in seen:
    
                continue
    
            seen.add(
    
                message
    
            )
    
            warnings.append(
    
                message
    
            )
    
        return warnings
    
    # =====================================================
    # CONTEXT VALIDATION
    # =====================================================

    def validate_context(
        self,
        items: List[ContextItem]
    ) -> bool:
        """
        Validate retrieved context.
        """
    
        return any(
    
            item.retrieved
    
            for item
    
            in items
    
        )

    # =====================================================
    # RETRIEVAL STATISTICS
    # =====================================================

    def build_statistics(
        self,
        items: List[ContextItem]
    ) -> RetrievalStatistics:
        """
        Build retrieval statistics.
        """
    
        total = len(items)
    
        successful = sum(
    
            item.retrieved
    
            for item
    
            in items
    
        )
    
        failed = total - successful
    
        return RetrievalStatistics(
    
            total_blocks=total,
    
            retrieved_blocks=successful,
    
            failed_blocks=failed,
    
            retrieval_rate=(
    
                successful / total
    
                if total
    
                else 0.0
    
            )
    
        )

    # =====================================================
    # MISSING SECTIONS
    # =====================================================

    def missing_sections(
        self,
        items: List[ContextItem]
    ) -> List[str]:
        """
        Return sections that could not
        be retrieved.
        """

        return [

            item.section

            for item in items

            if not item.retrieved

        ]


    # =====================================================
    # CONTEXT SUMMARY
    # =====================================================

    def summarize_context(
        self,
        items: List[ContextItem]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Produce a lightweight summary
        of retrieved context.
        """
    
        summary = {}
    
        for item in items:
    
            summary[item.section] = {
    
                "retrieved":
    
                    item.retrieved,
    
                "source":
    
                    item.source,
    
                "confidence":
    
                    item.confidence
    
            }
    
        return summary
    
    # =====================================================
    # BUILD CONTEXT
    # =====================================================

    def build(
        self,
        planner: PlannerResult
    ) -> ContextResult:
        """
        Main retrieval pipeline.
        """

        # -----------------------------------------
        # No entity available
        # -----------------------------------------

        if planner.entity is None:

            return ContextResult(

                entity=None,

                warnings=[

                    "No entity available for retrieval."

                ]

            )

        # -----------------------------------------
        # Retrieve all blocks
        # -----------------------------------------

        items = self.retrieve_blocks_safe(

            planner

        )

        # -----------------------------------------
        # Merge context
        # -----------------------------------------

        merged = self.merge_context(

            items

        )

        # -----------------------------------------
        # Warnings
        # -----------------------------------------

        warnings = self.collect_warnings(

            items

        )

        # -----------------------------------------
        # Statistics
        # -----------------------------------------

        statistics = self.build_statistics(

            items

        )

        statistics.missing_sections = (

            self.missing_sections(

                items

            )

        )

        statistics.summary = (

            self.summarize_context(

                items

            )

        )

        statistics.valid = (

            self.validate_context(

                items

            )

        )

        # -----------------------------------------
        # Required block validation
        # -----------------------------------------

        for block in planner.blocks:

            if not block.required:

                continue

            found = any(

                item.section == block.section

                and item.retrieved

                for item in items

            )

            if not found:

                warnings.append(

                    f"Required section '{block.section}' could not be retrieved."

                )

        # -----------------------------------------
        # Build result
        # -----------------------------------------

        result = ContextResult(

            entity=planner.entity,

            items=items,

            merged_context=merged,

            statistics=statistics,

            warnings=warnings

        )

        return result

# =========================================================
# PUBLIC API
# =========================================================

__all__ = [

    "ContextItem",

    "ContextResult",

    "RetrievalStatistics",

    "DatabaseRetriever",

    "ContextBuilder"

]