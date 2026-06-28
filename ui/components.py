"""
=========================================================
Research Navigator

Reusable Streamlit Components

Version : 3.0

=========================================================

This module contains reusable UI components.

It NEVER performs business logic.

It ONLY renders data supplied by the backend.

=========================================================
"""

from __future__ import annotations

from typing import Dict, Optional, Any

import streamlit as st

from core.config import settings

from builder.response_builder import ResponseResult

from ui.helpers import (

    format_label,

    format_metadata

)

# =========================================================
# PAGE TITLE
# =========================================================

def page_header():

    """
    Display the application header.
    """

    st.title(settings.project_name)

    st.caption(
        "Educational AI Research Assistant"
    )

    st.divider()


# =========================================================
# SIDEBAR HEADER
# =========================================================

def sidebar_header():

    """
    Sidebar heading.
    """

    st.sidebar.title(
        "Navigation"
    )

    st.sidebar.caption(
        "Research Navigator v3.0"
    )

    st.sidebar.divider()


# =========================================================
# STATUS CARD
# =========================================================

def status_card(
    title: str,
    value: str,
    success: bool = True
):

    """
    Small reusable status indicator.
    """

    icon = "✅" if success else "❌"

    st.metric(

    label=title,

    value=value

)

st.caption(icon)


# =========================================================
# SECTION TITLE
# =========================================================

def section_title(
    title: str
):

    """
    Standard section title.
    """

    st.subheader(title)
# =========================================================
# USER MESSAGE
# =========================================================

def user_message(
    message: str
):
    """
    Display a user chat message.
    """

    with st.chat_message("user"):

        st.markdown(message)


# =========================================================
# ASSISTANT MESSAGE
# =========================================================

def assistant_message(
    result: ResponseResult
):
    """
    Display an assistant response.
    """

    with st.chat_message("assistant"):

        st.markdown(

            result.response

        )


# =========================================================
# RESPONSE METADATA
# =========================================================

def response_metadata(
    result: ResponseResult
):
    """
    Display response metadata.
    """

    metadata = getattr(

        result,

        "metadata",

        {}

    )

    #
    # Format metadata using helpers
    #

    metadata = format_metadata(

        metadata

    )

    if not metadata:

        return

    with st.expander(

        "Response Metadata",

        expanded=False

    ):

        for key, value in metadata.items():

            st.write(

                f"**{key}**"

            )

            st.write(

                value

            )

# =========================================================
# RESPONSE SECTIONS
# =========================================================

def response_sections(
    result: ResponseResult
):
    """
    Display generated response sections.
    """

    sections = getattr(

        result,

        "sections",

        []

    )

    if not sections:

        return

    with st.expander(

        "Generated Sections",

        expanded=False

    ):

        for section in sections:

            st.markdown(

                f"### {section.title}"

            )

            st.markdown(

                section.content

            )


# =========================================================
# COMPLETE RESPONSE
# =========================================================

def display_response(
    result: ResponseResult
):
    """
    Display the complete assistant response.
    """

    assistant_message(

        result

    )

    response_sections(

        result

    )

    response_metadata(

        result

    )
# =========================================================
# HEALTH PANEL
# =========================================================

def health_panel(
    health: Dict[str, Any]
):
    """
    Display application health.
    """

    st.subheader("System Health")

    application = health.get(

        "application",

        False

    )

    database = health.get(

        "database",

        {}

    )

    assistant = health.get(

        "assistant",

        {}

    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Application",

            "Running"

            if application

            else

            "Stopped"

        )

    with col2:

        if isinstance(database, dict):

            st.metric(

                "Database",

                database.get(

                    "status",

                    "Unknown"

                )

            )

        else:

            st.metric(

                "Database",

                str(database)

            )

    if assistant:

        st.markdown("---")

        st.markdown("### Assistant Components")

        for component, state in assistant.items():

            icon = "✅" if state else "❌"

            st.write(

                f"{icon} **{component}**"

            )


# =========================================================
# KNOWLEDGE PANEL
# =========================================================

def knowledge_panel(
    statistics: Dict[str, Any]
):
    """
    Display knowledge statistics.
    """

    st.subheader(

        "Knowledge Base"

    )

    if not statistics:

        st.info(

            "No statistics available."

        )

        return

    columns = st.columns(2)

    index = 0

    for key, value in statistics.items():

        with columns[

            index % 2

        ]:

            st.metric(

                format_label(key),

                value

            )

        index += 1


# =========================================================
# INFORMATION PANEL
# =========================================================

def information_panel(
    title: str,
    information: Dict[str, Any]
):
    """
    Generic expandable information panel.
    """

    with st.expander(

        title,

        expanded=False

    ):

        if not information:

            st.info(

                "Nothing to display."

            )

            return

        for key, value in information.items():

            st.write(

                f"**{format_label(key)}**"

            )

            st.write(

                value

            )


# =========================================================
# SIMPLE LABEL FORMATTER
# =========================================================

def format_label(
    text: str
):
    """
    Convert snake_case into
    readable labels.
    """

    return (

        text

        .replace(

            "_",

            " "

        )

        .title()

    )
