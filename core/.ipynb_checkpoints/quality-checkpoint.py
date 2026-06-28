"""
=========================================================
Research Navigator
Knowledge Quality Engine
Version : 1.0
=========================================================

Responsibilities
----------------
✓ Evaluate Topics
✓ Evaluate Researchers
✓ Evaluate Papers
✓ Compute Knowledge Score
✓ Determine Quality Level
✓ Generate Quality Reports

This module NEVER modifies knowledge.
It only evaluates it.

Author : Research Navigator
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Any

from core.schema import *


# ==========================================================
# QUALITY THRESHOLDS
# ==========================================================

QUALITY_THRESHOLDS = {

    "Diamond": 95,

    "Platinum": 90,

    "Gold": 80,

    "Silver": 65,

    "Bronze": 0

}


# ==========================================================
# DEFAULT SECTION WEIGHTS
# ==========================================================

TOPIC_WEIGHTS = {

    "identity": 10,

    "learning": 20,

    "history": 10,

    "timeline": 10,

    "researchers": 10,

    "papers": 10,

    "applications": 10,

    "future": 10,

    "faq": 5,

    "relationships": 5

}


# ==========================================================
# QUALITY REPORT
# ==========================================================

@dataclass

class QualityReport:

    object_name: str

    object_type: str

    total_score: float = 0

    quality_level: str = "Bronze"

    section_scores: Dict[str, float] = field(

        default_factory=dict

    )

    missing_sections: List[str] = field(

        default_factory=list

    )

    warnings: List[str] = field(

        default_factory=list

    )

    recommendations: List[str] = field(

        default_factory=list
    )


# ==========================================================
# HELPERS
# ==========================================================

def _percent(

    obtained: float,

    maximum: float

) -> float:

    if maximum == 0:

        return 0.0

    return round(

        obtained / maximum * 100,

        2

    )


def _quality_level(

    score: float

) -> str:

    for level, minimum in QUALITY_THRESHOLDS.items():

        if score >= minimum:

            return level

    return "Bronze"


# ==========================================================
# SECTION SCORE
# ==========================================================

def score_section(

    value: Any

) -> float:
    """
    Returns a percentage score
    for one section.
    """

    if value is None:

        return 0

    if isinstance(

        value,

        str

    ):

        return 100 if value.strip() else 0

    if isinstance(

        value,

        list

    ):

        if len(value) == 0:

            return 0

        if len(value) >= 5:

            return 100

        return round(

            len(value) / 5 * 100,

            2

        )

    if isinstance(

        value,

        dict

    ):

        if len(value) == 0:

            return 0

        filled = sum(

            bool(v)

            for v in value.values()

        )

        return _percent(

            filled,

            len(value)

        )

    return 0


# ==========================================================
# EMPTY REPORT
# ==========================================================

def create_report(

    object_name: str,

    object_type: str

) -> QualityReport:

    return QualityReport(

        object_name=object_name,

        object_type=object_type

    )


# ==========================================================
# WEIGHTED SCORE
# ==========================================================

def weighted_score(

    section_scores: Dict[str, float],

    weights: Dict[str, float]

) -> float:

    obtained = 0

    total = 0

    for section, weight in weights.items():

        total += weight

        obtained += (

            section_scores.get(

                section,

                0

            )

            * weight

            / 100

        )

    return round(

        obtained / total * 100,

        2

    )
# ==========================================================
# TOPIC EVALUATION
# ==========================================================

def evaluate_topic(topic: Dict) -> QualityReport:
    """
    Evaluate a Topic knowledge object.
    """

    report = create_report(
        topic["identity"]["name"],
        "Topic"
    )

    scores = {}

    # ---------------- Identity ----------------

    scores["identity"] = score_section(
        topic.get("identity", {})
    )

    # ---------------- Learning ----------------

    scores["learning"] = score_section(
        topic.get("learning", {})
    )

    # ---------------- History ----------------

    scores["history"] = score_section(
        topic.get("history", {})
    )

    # ---------------- Timeline ----------------

    scores["timeline"] = score_section(
        topic.get("timeline", [])
    )

    # ---------------- Researchers ----------------

    scores["researchers"] = score_section(
        topic.get("researchers", [])
    )

    # ---------------- Papers ----------------

    scores["papers"] = score_section(
        topic.get("papers", [])
    )

    # ---------------- Applications ----------------

    scores["applications"] = score_section(
        topic.get("applications", [])
    )

    # ---------------- Future ----------------

    scores["future"] = score_section(
        topic.get("future", {})
    )

    # ---------------- FAQ ----------------

    scores["faq"] = score_section(
        topic.get("faq", [])
    )

    # ---------------- Relationships ----------------

    scores["relationships"] = score_section(
        topic.get("relationships", {})
    )

    report.section_scores = scores

    report.total_score = weighted_score(
        scores,
        TOPIC_WEIGHTS
    )

    report.quality_level = _quality_level(
        report.total_score
    )

    # Missing Sections

    for section, score in scores.items():

        if score == 0:

            report.missing_sections.append(section)

    # Recommendations

    if scores["papers"] < 50:

        report.recommendations.append(
            "Add landmark research papers."
        )

    if scores["researchers"] < 50:

        report.recommendations.append(
            "Add influential researchers."
        )

    if scores["timeline"] < 50:

        report.recommendations.append(
            "Expand historical timeline."
        )

    if scores["relationships"] < 50:

        report.recommendations.append(
            "Link this topic to other knowledge nodes."
        )

    return report


# ==========================================================
# RESEARCHER EVALUATION
# ==========================================================

def evaluate_researcher(
    researcher: Dict
) -> QualityReport:

    report = create_report(

        researcher["identity"]["name"],

        "Researcher"

    )

    scores = {}

    for section, value in researcher.items():

        if section in [

            "type",

            "identity"

        ]:

            continue

        scores[section] = score_section(value)

    report.section_scores = scores

    if len(scores):

        report.total_score = round(

            sum(scores.values()) / len(scores),

            2

        )

    report.quality_level = _quality_level(

        report.total_score

    )

    return report


# ==========================================================
# PAPER EVALUATION
# ==========================================================

def evaluate_paper(

    paper: Dict

) -> QualityReport:

    report = create_report(

        paper["identity"]["title"],

        "Paper"

    )

    scores = {}

    for section, value in paper.items():

        if section in [

            "type",

            "identity"

        ]:

            continue

        scores[section] = score_section(

            value

        )

    report.section_scores = scores

    if len(scores):

        report.total_score = round(

            sum(

                scores.values()

            ) / len(scores),

            2

        )

    report.quality_level = _quality_level(

        report.total_score

    )

    return report


# ==========================================================
# GENERIC EVALUATOR
# ==========================================================

def evaluate(

    obj: Dict

) -> QualityReport:
    """
    Automatically detect object type.
    """

    obj_type = obj.get("type", "").lower()

    if obj_type == "topic":

        return evaluate_topic(obj)

    if obj_type == "researcher":

        return evaluate_researcher(obj)

    if obj_type == "paper":

        return evaluate_paper(obj)

    raise ValueError(

        f"Unsupported object type: {obj_type}"

    )
