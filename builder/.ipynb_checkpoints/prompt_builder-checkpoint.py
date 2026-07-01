"""
=========================================================
Research Navigator

Prompt Builder

Version : 3.0

=========================================================

Builds prompts for the local LLM.

Responsibilities

• Format retrieved context

• Build educational instructions

• Build system prompt

• Build user prompt

• Assemble the final prompt

The Prompt Builder never

• retrieves knowledge

• plans knowledge

• calls the LLM

• parses responses

=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from typing import (
    Any,
    Dict,
    List
)

from agents.knowledge_planner import (
    PlannerResult
)

from builder.context_builder import (
    ContextResult,
    ContextItem
)

from core.constants import (
    STRATEGY_CONCEPT_FIRST,
    STRATEGY_GUIDED,
    STRATEGY_HISTORY,
    STRATEGY_RESEARCH,
)


# =========================================================
# PROMPT RESULT
# =========================================================

@dataclass(slots=True)
class PromptResult:
    """
    Complete prompt package.
    """

    system_prompt: str = ""

    instruction_prompt: str = ""

    context_prompt: str = ""

    user_prompt: str = ""

    full_prompt: str = ""

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

# =========================================================
# PROMPT BUILDER
# =========================================================

class PromptBuilder:
    """
    Builds prompts for local LLMs.
    """

    def __init__(self):
        """
        PromptBuilder is intentionally stateless.
        """

        pass
    # =====================================================
    # PROMPT TEMPLATES
    # =====================================================

    SYSTEM_TEMPLATE = """
You are Research Navigator, an educational AI research mentor.

Your primary objective is to help users understand concepts rather than merely providing answers.

Core Principles

• Teach before concluding.

• Explain historical motivation whenever possible.

• Connect ideas together.

• Build intuition before technical details.

• Prefer educational clarity over brevity.

• If context is incomplete, clearly state the limitation instead of inventing information.

• Never fabricate researchers, papers, datasets or historical events.

• If multiple viewpoints exist, explain them objectively.

Always produce structured markdown with meaningful headings.
""".strip()


    EDUCATIONAL_TEMPLATE = """
Teaching Strategy:
{strategy}

Difficulty:
{difficulty}

Learning Profile:
{profile}

Learning Objectives

{objectives}

Suggested Visualizations

{visuals}

Suggested Curiosity Prompts

{questions}
""".strip()


    CONTEXT_TEMPLATE = """
Retrieved Knowledge

{context}
""".strip()


    USER_TEMPLATE = """
User Question

{question}
""".strip()


    FULL_PROMPT_TEMPLATE = """
{system_prompt}

------------------------------------------------------------

{instruction_prompt}

------------------------------------------------------------

{context_prompt}

------------------------------------------------------------

{user_prompt}
""".strip()


    # =====================================================
    # DEFAULTS
    # =====================================================

    DEFAULT_SYSTEM_NAME = "Research Navigator"

    DEFAULT_STRATEGY = STRATEGY_CONCEPT_FIRST

    DEFAULT_PROFILE = "Intermediate"

    DEFAULT_DIFFICULTY = "Medium"
    # =====================================================
    # FORMAT LIST
    # =====================================================

    @staticmethod
    def format_list(
        values: List[str]
    ) -> str:
        """
        Format a list as bullet points.
        """

        if not values:

            return "- None"

        return "\n".join(

            f"- {item}"

            for item in values

        )


    # =====================================================
    # FORMAT VALUE
    # =====================================================

    @staticmethod
    def format_value(
        value: Any
    ) -> str:
        """
        Format any Python value into a
        readable prompt representation.
        """

        if value is None:

            return "None"

        if isinstance(value, bool):

            return "Yes" if value else "No"

        if isinstance(value, list):

            if not value:

                return "None"

            return "\n".join(

                f"- {item}"

                for item in value

            )

        if isinstance(value, dict):

            if not value:

                return "None"

            lines = []

            for key, val in sorted(

                value.items()
            
            ):
                lines.append(

                    f"{key}: {PromptBuilder.format_value(val)}"

                )

            return "\n".join(lines)

        return str(value)


    # =====================================================
    # FORMAT CONTEXT ITEM
    # =====================================================

    def format_context_item(
        self,
        item: ContextItem
    ) -> str:
        """
        Convert one ContextItem into text.
        """

        lines = [

            f"## {item.section.title()}"

        ]

        if not item.retrieved:

            lines.append(
        
                "No information available."
        
            )
        
            return "\n".join(lines)
        
        if isinstance(item.data, dict):

            for key, value in item.data.items():

                lines.append(

                    f"{key}:"

                )

                lines.append(

                    self.format_value(value)

                )

                lines.append("")

        else:

            lines.append(

                self.format_value(

                    item.data

                )

            )

            lines.append("")

        return "\n".join(lines).strip()


    # =====================================================
    # FORMAT COMPLETE CONTEXT
    # =====================================================

    def format_context(
        self,
        context: ContextResult
    ) -> str:
        """
        Format all retrieved context.
        """

        if not context.items:

            return "No context available."

        sections = []

        for item in context.items:

            sections.append(

                self.format_context_item(

                    item

                )

            )

        return "\n\n".join(

            sections

        )
    # =====================================================
    # HUMAN READABLE LABEL
    # =====================================================

    @staticmethod
    def humanize(text: str) -> str:
        """
        Convert snake_case into a readable label.
        """

        return text.replace(

            "_",

            " "

        ).title()


    # =====================================================
    # FORMAT OBJECTIVES
    # =====================================================

    def format_learning_objectives(
        self,
        planner: PlannerResult
    ) -> str:
        """
        Format learning objectives.
        """
    
        objectives = planner.learning_objectives
    
        if not objectives:
    
            objectives = [
    
                "Understand the requested topic."
    
            ]
    
        return self.format_list(
    
            objectives
    
        )


    # =====================================================
    # FORMAT VISUALS
    # =====================================================

    def format_visual_components(
        self,
        planner: PlannerResult
    ) -> str:
        """
        Format suggested visualizations.
        """
    
        visuals = [
    
            self.humanize(
    
                visual
    
            )
    
            for visual
    
            in planner.visual_components
    
        ]
    
        if not visuals:
    
            visuals = [
    
                "None"
    
            ]
    
        return self.format_list(
    
            visuals
    
        )

    # =====================================================
    # FORMAT CURIOSITY
    # =====================================================

    def format_curiosity_prompts(
        self,
        planner: PlannerResult
    ) -> str:
        """
        Format curiosity prompts.
        """
    
        prompts = planner.suggested_questions
    
        if not prompts:
    
            prompts = [
    
                "None"
    
            ]
    
        return self.format_list(
    
            prompts
    
        )

    # =====================================================
    # BUILD EDUCATIONAL INSTRUCTIONS
    # =====================================================

    def build_instruction_prompt(
        self,
        planner: PlannerResult
    ) -> str:
        """
        Build the educational instruction block.
        """

        strategy = (

            planner.teaching_strategy

            or

            self.DEFAULT_STRATEGY

        )

        profile = (

            planner.learning_profile

            or

            self.DEFAULT_PROFILE

        )

        difficulty = (

            planner.difficulty

            or

            self.DEFAULT_DIFFICULTY

        )

        objectives = self.format_learning_objectives(

            planner

        )

        visuals = self.format_visual_components(

            planner

        )

        curiosity = self.format_curiosity_prompts(

            planner

        )

        instruction = self.EDUCATIONAL_TEMPLATE.format(

            strategy=strategy,
        
            difficulty=difficulty,
        
            profile=profile,
        
            objectives=objectives,
        
            visuals=visuals,
        
            questions=curiosity
        
        )
        
        return instruction
    # =====================================================
    # TEACHING STRATEGY
    # =====================================================

    def strategy_instruction(
        self,
        strategy: str
    ) -> str:
        """
        Convert an internal strategy into
        natural-language guidance.
        """
    
        strategies = {
    
            STRATEGY_CONCEPT_FIRST:
                (
                    "Begin with the fundamental idea. "
                    "Develop intuition before introducing "
                    "technical details."
                ),
    
            STRATEGY_GUIDED:
                (
                    "Teach progressively from simple "
                    "concepts toward advanced understanding."
                ),
    
            STRATEGY_HISTORY:
                (
                    "Explain how the topic evolved over "
                    "time and why each milestone mattered."
                ),
    
            STRATEGY_RESEARCH:
                (
                    "Focus on landmark research, "
                    "state-of-the-art methods, "
                    "limitations and future work."
                )
    
        }
    
        return strategies.get(
    
            strategy,
    
            strategies[
    
                STRATEGY_CONCEPT_FIRST
    
            ]
    
        )

    # =====================================================
    # BUILD SYSTEM PROMPT
    # =====================================================

    def build_system_prompt(
        self,
        planner: PlannerResult
    ) -> str:
        """
        Build the adaptive system prompt.
        """

        strategy = (

            planner.teaching_strategy

            or

            self.DEFAULT_STRATEGY

        )

        instruction = self.strategy_instruction(

            strategy

        )

        lines = [

            self.SYSTEM_TEMPLATE,

            "",

            "Additional Instructions",

            "-----------------------",

            instruction,

            "",

            "Important Rules",

            "---------------",

            "- Never fabricate information.",

            "- Use only the retrieved context.",

            "- Clearly identify missing information.",

            "- Prefer educational explanations.",

            "- Use markdown headings.",

            "- Include practical intuition whenever appropriate.",

            "- Connect concepts with historical motivation."

        ]

        system_prompt = "\n".join(
        
            lines
        
        )
        
        return system_prompt


    # =====================================================
    # BUILD CONTEXT PROMPT
    # =====================================================

    def build_context_prompt(
        self,
        context: ContextResult
    ) -> str:
        """
        Build the formatted context block.
        """
    
        formatted_context = self.format_context(
    
            context
    
        )
    
        context_prompt = self.CONTEXT_TEMPLATE.format(
    
            context=formatted_context
    
        )
    
        return context_prompt
    
    # =====================================================
    # BUILD USER PROMPT
    # =====================================================

    def build_user_prompt(
        self,
        question: str,
        planner: PlannerResult
    ) -> str:
        """
        Build the user prompt.
        """
    
        profile = (
    
            planner.learning_profile
    
            or
    
            self.DEFAULT_PROFILE
    
        )
    
        difficulty = (
    
            planner.difficulty
    
            or
    
            self.DEFAULT_DIFFICULTY
    
        )
    
        lines = [
    
            self.USER_TEMPLATE.format(
    
                question=question
    
            ),
    
            "",
    
            "Expected Response",
    
            "-----------------",
    
            f"Learning Profile : {profile}",
    
            f"Difficulty       : {difficulty}",
    
            "",
    
            "Please:",
    
            "- Answer the user's question accurately.",
    
            "- Use the retrieved context as the primary source.",
    
            "- Explain concepts step by step.",
    
            "- Build intuition before technical details.",
    
            "- Use markdown headings.",
    
            "- Include practical examples where appropriate.",
    
            "- Clearly acknowledge missing information."
    
        ]
    
        return "\n".join(
    
            lines
    
        )

    # =====================================================
    # BUILD COMPLETE PROMPT
    # =====================================================

    def build_full_prompt(
        self,
        system_prompt: str,
        instruction_prompt: str,
        context_prompt: str,
        user_prompt: str
    ) -> str:
        """
        Assemble the complete prompt.
        """
    
        full_prompt = self.FULL_PROMPT_TEMPLATE.format(
    
            system_prompt=system_prompt,
    
            instruction_prompt=instruction_prompt,
    
            context_prompt=context_prompt,
    
            user_prompt=user_prompt
    
        )
    
        return full_prompt

    # =====================================================
    # BUILD
    # =====================================================

    def build(
        self,
        question: str,
        planner: PlannerResult,
        context: ContextResult
    ) -> PromptResult:
        """
        Build the complete prompt package.
        """
    
        system_prompt = self.build_system_prompt(
    
            planner
    
        )
    
        instruction_prompt = self.build_instruction_prompt(
    
            planner
    
        )
    
        context_prompt = self.build_context_prompt(
    
            context
    
        )
    
        user_prompt = self.build_user_prompt(
    
            question,
    
            planner
    
        )
    
        full_prompt = self.build_full_prompt(
    
            system_prompt,
    
            instruction_prompt,
    
            context_prompt,
    
            user_prompt
    
        )
    
        metadata = {
    
            "strategy":
    
                planner.teaching_strategy,
    
            "profile":
    
                planner.learning_profile,
    
            "difficulty":
    
                planner.difficulty,
    
            "context_sections":
    
                len(
    
                    context.items
    
                ),
    
            "retrieval_rate":
    
                context.statistics.retrieval_rate
    
        }
    
        return PromptResult(
    
            system_prompt=system_prompt,
    
            instruction_prompt=instruction_prompt,
    
            context_prompt=context_prompt,
    
            user_prompt=user_prompt,
    
            full_prompt=full_prompt,
    
            metadata=metadata
    
        )
    
    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(
        self,
        result: PromptResult
    ) -> bool:
        """
        Validate the generated prompt.
        """
    
        required = [
    
            result.system_prompt,
    
            result.instruction_prompt,
    
            result.context_prompt,
    
            result.user_prompt,
    
            result.full_prompt
    
        ]
    
        return all(
    
            part.strip()
    
            for part
    
            in required
    
        )

    # =====================================================
    # DEBUG
    # =====================================================

    def debug(
        self,
        question: str,
        planner: PlannerResult,
        context: ContextResult
    ) -> Dict[str, Any]:
        """
        Return every generated prompt component.

        Useful while developing prompts.
        """

        result = self.build(

            question,

            planner,

            context

        )

        return {

            "system_prompt":

                result.system_prompt,

            "instruction_prompt":

                result.instruction_prompt,

            "context_prompt":

                result.context_prompt,

            "user_prompt":

                result.user_prompt,

            "full_prompt":

                result.full_prompt,

            "metadata":

                result.metadata

        }


    # =====================================================
    # RESET
    # =====================================================

    def reset(
        self
    ) -> None:
        """
        Reserved for future prompt caching.

        PromptBuilder is intentionally stateless.
        """

        pass
# =========================================================
# PUBLIC API
# =========================================================

__all__ = [

    "PromptResult",

    "PromptBuilder"

]