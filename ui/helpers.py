"""
=========================================================
Research Navigator

UI Helper Functions

Version : 3.0

=========================================================

Formatting helpers used throughout the UI.

This module NEVER renders Streamlit components.

It ONLY formats values.

=========================================================
"""

from __future__ import annotations

from typing import Any


# =========================================================
# FORMAT LABEL
# =========================================================

def format_label(
    text: str
) -> str:
    """
    Convert snake_case into a readable label.
    """

    return (

        text

        .replace(

            "_",

            " "

        )

        .title()

    )


# =========================================================
# FORMAT BOOLEAN
# =========================================================

def format_boolean(
    value: bool
) -> str:
    """
    Format a boolean value.
    """

    return (

        "Yes"

        if value

        else

        "No"

    )


# =========================================================
# FORMAT NUMBER
# =========================================================

def format_number(
    value: Any
) -> str:
    """
    Format numeric values.
    """

    if isinstance(

        value,

        int

    ):

        return f"{value:,}"

    if isinstance(

        value,

        float

    ):

        return f"{value:.2f}"

    return str(

        value

    )


# =========================================================
# FORMAT VALUE
# =========================================================

def format_value(
    value: Any
) -> str:
    """
    Convert any value into a readable string.
    """

    if value is None:

        return "None"

    if isinstance(

        value,

        bool

    ):

        return format_boolean(

            value

        )

    if isinstance(

        value,

        (

            int,

            float

        )

    ):

        return format_number(

            value

        )

    if isinstance(

        value,

        list

    ):

        if not value:

            return "None"

        return ", ".join(

            str(item)

            for item in value

        )

    if isinstance(

        value,

        dict

    ):

        return str(

            value

        )

    return str(

        value

    )
# =========================================================
# FORMAT METADATA
# =========================================================

def format_metadata(
    metadata: dict
) -> dict:
    """
    Format response metadata for display.
    """

    if not metadata:

        return {}

    formatted = {}

    for key, value in metadata.items():

        formatted[
            format_label(key)
        ] = format_value(
            value
        )

    return formatted


# =========================================================
# FORMAT STATISTICS
# =========================================================

def format_statistics(
    statistics: dict
) -> dict:
    """
    Format statistics for display.
    """

    if not statistics:

        return {}

    formatted = {}

    for key, value in statistics.items():

        formatted[
            format_label(key)
        ] = format_number(
            value
        )

    return formatted


# =========================================================
# FORMAT HEALTH
# =========================================================

def format_health(
    health: dict
) -> dict:
    """
    Format health information.
    """

    if not health:

        return {}

    formatted = {}

    for key, value in health.items():

        label = format_label(

            key

        )

        if isinstance(

            value,

            bool

        ):

            formatted[
                label
            ] = format_boolean(
                value
            )

        elif isinstance(

            value,

            dict

        ):

            formatted[
                label
            ] = format_metadata(
                value
            )

        else:

            formatted[
                label
            ] = format_value(
                value
            )

    return formatted


# =========================================================
# FORMAT KEY-VALUE TABLE
# =========================================================

def format_key_value(
    data: dict
) -> list[tuple[str, str]]:
    """
    Convert a dictionary into a list of
    (label, value) tuples.
    """

    if not data:

        return []

    rows = []

    for key, value in data.items():

        rows.append(

            (

                format_label(

                    key

                ),

                format_value(

                    value

                )

            )

        )

    return rows


# =========================================================
# FORMAT LIST
# =========================================================

def format_list(
    values: list
) -> list[str]:
    """
    Format every value inside a list.
    """

    return [

        format_value(

            value

        )

        for value in values

    ]
