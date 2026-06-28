"""
=========================================================
Research Navigator

Response Builder

Version : 3.0

=========================================================

Transforms raw LLM responses into a structured
educational response.

Responsibilities

• Clean LLM output

• Organize sections

• Extract markdown

• Build UI metadata

• Prepare the final response object

=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from typing import (

    Dict,

    List,

    Optional

)

from builder.prompt_builder import (

    PromptResult

)


# =========================================================
# RESPONSE SECTION
# =========================================================

@dataclass
class ResponseSection:
    """
    One educational section returned
    by the LLM.
    """

    title: str

    content: str

    order: int

    expandable: bool = True

    metadata: Dict = field(

        default_factory=dict

    )


# =========================================================
# RESPONSE RESULT
# =========================================================

@dataclass
class ResponseResult:
    """
    Final structured response.
    """

    answer: str = ""

    sections: List[ResponseSection] = field(

        default_factory=list

    )

    suggested_questions: List[str] = field(

        default_factory=list

    )

    visual_components: List[str] = field(

        default_factory=list

    )

    metadata: Dict = field(

        default_factory=dict

    )


# =========================================================
# RESPONSE BUILDER
# =========================================================

class ResponseBuilder:
    """
    Converts raw LLM output into a
    structured educational response.
    """

    def __init__(self):

        pass
    # =====================================================
    # CLEAN RESPONSE
    # =====================================================

    def clean_response(
        self,
        response: str
    ) -> str:
        """
        Clean the raw LLM response.
        """

        if response is None:

            return ""

        response = response.replace(

            "\r\n",

            "\n"

        )

        while "\n\n\n" in response:

            response = response.replace(

                "\n\n\n",

                "\n\n"

            )

        return response.strip()


    # =====================================================
    # SPLIT INTO SECTIONS
    # =====================================================

    def split_sections(
        self,
        response: str
    ) -> List[str]:
        """
        Split markdown into sections.

        Headings beginning with ##
        start a new section.
        """

        if not response:

            return []

        sections = []

        current = []

        for line in response.splitlines():

            if line.startswith("## "):

                if current:

                    sections.append(

                        "\n".join(current)

                    )

                    current = []

            current.append(line)

        if current:

            sections.append(

                "\n".join(current)

            )

        return sections


    # =====================================================
    # BUILD RESPONSE SECTION
    # =====================================================

    def parse_section(
        self,
        text: str,
        order: int
    ) -> ResponseSection:
        """
        Convert one markdown section into
        a ResponseSection.
        """

        lines = text.splitlines()

        if not lines:

            return ResponseSection(

                title="",

                content="",

                order=order

            )

        title = lines[0]

        if title.startswith("## "):

            title = title[3:]

        content = "\n".join(

            lines[1:]

        ).strip()

        return ResponseSection(

            title=title,

            content=content,

            order=order

        )


    # =====================================================
    # PARSE RESPONSE
    # =====================================================

    def parse_response(
        self,
        response: str
    ) -> List[ResponseSection]:
        """
        Parse the complete LLM response.
        """

        response = self.clean_response(

            response

        )

        chunks = self.split_sections(

            response

        )

        sections = []

        for index, chunk in enumerate(

            chunks,

            start=1

        ):

            sections.append(

                self.parse_section(

                    chunk,

                    index

                )

            )

        return sections
    # =====================================================
    # ANSWER SUMMARY
    # =====================================================

    def extract_summary(
        self,
        response: str
    ) -> str:
        """
        Extract the introductory summary.

        The summary is everything before the
        first markdown section.
        """

        response = self.clean_response(response)

        lines = response.splitlines()

        summary = []

        for line in lines:

            if line.startswith("## "):

                break

            summary.append(line)

        return "\n".join(summary).strip()


    # =====================================================
    # SECTION METADATA
    # =====================================================

    def enrich_sections(
        self,
        sections: List[ResponseSection]
    ) -> List[ResponseSection]:
        """
        Attach useful metadata to each section.
        """

        for section in sections:

            section.metadata = {

                "word_count":

                    len(section.content.split()),

                "character_count":

                    len(section.content),

                "empty":

                    len(section.content.strip()) == 0

            }

        return sections


    # =====================================================
    # RESPONSE METADATA
    # =====================================================

    def build_metadata(
        self,
        response: str,
        sections: List[ResponseSection]
    ) -> Dict:
        """
        Build metadata describing the response.
        """

        total_words = len(response.split())

        return {

            "word_count": total_words,

            "section_count": len(sections),

            "has_sections": len(sections) > 0,

            "is_markdown": "##" in response

        }


    # =====================================================
    # VISUAL PLAN
    # =====================================================

    def build_visual_plan(
        self,
        planner
    ) -> List[str]:
        """
        Reuse planner visual decisions.

        This keeps UI logic outside the LLM.
        """

        if planner is None:

            return []

        return list(

            planner.visual_components

        )


    # =====================================================
    # CURIOSITY PROMPTS
    # =====================================================

    def build_curiosity_prompts(
        self,
        planner
    ) -> List[str]:
        """
        Reuse planner curiosity prompts.
        """

        if planner is None:

            return []

        return list(

            planner.suggested_questions

        )
    # =====================================================
    # BUILD RESPONSE
    # =====================================================

    def build(
        self,
        response: str,
        planner: Optional[PlannerResult] = None
    ) -> ResponseResult:
        """
        Build the final structured response.
        """

        cleaned = self.clean_response(

            response

        )

        summary = self.extract_summary(

            cleaned

        )

        sections = self.parse_response(

            cleaned

        )

        sections = self.enrich_sections(

            sections

        )

        metadata = self.build_metadata(

            cleaned,

            sections

        )

        visuals = self.build_visual_plan(

            planner

        )

        curiosity = self.build_curiosity_prompts(

            planner

        )

        result = ResponseResult(

            answer=summary,

            sections=sections,

            suggested_questions=curiosity,

            visual_components=visuals,

            metadata=metadata

        )

        return result


    # =====================================================
    # DEBUG
    # =====================================================

    def debug(
        self,
        response: str,
        planner: Optional[PlannerResult] = None
    ) -> Dict:
        """
        Debug helper.
        """

        result = self.build(

            response,

            planner

        )

        return {

            "summary":

                result.answer,

            "sections":

                len(result.sections),

            "visuals":

                result.visual_components,

            "curiosity":

                result.suggested_questions,

            "metadata":

                result.metadata

        }


    # =====================================================
    # RESET
    # =====================================================

    def reset(self):
        """
        Reserved for future conversation-aware
        response builders.
        """

        pass
# =========================================================
# PUBLIC API
# =========================================================

__all__ = [

    "ResponseSection",

    "ResponseResult",

    "ResponseBuilder"

]