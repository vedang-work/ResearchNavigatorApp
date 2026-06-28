"""
=========================================================
Research Navigator

Sidebar Components

Version : 3.0

=========================================================

Reusable Streamlit sidebar components.

This module ONLY renders sidebar content.

It never performs business logic.

=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from typing import Dict, List, Optional

import streamlit as st

from core.config import settings

from ui.helpers import (

    format_label,

    format_statistics

)

@dataclass
class ModelSelection:
    """
    Selected language model.
    """

    selected_model: str

    changed: bool

# =========================================================
# SIDEBAR SETTINGS
# =========================================================

@dataclass
class SidebarSettings:
    """
    Sidebar configuration selected by the user.
    """

    streaming: bool

    statistics: bool

    visualizations: bool

    curiosity: bool
    
# =========================================================
# SIDEBAR HEADER
# =========================================================

def sidebar_header():
    """
    Render the application sidebar header.
    """

    st.sidebar.title(
        settings.project_name
    )

    st.sidebar.caption(
        f"Version {settings.version}"
    )

    st.sidebar.divider()


# =========================================================
# NAVIGATION
# =========================================================

def navigation() -> str:
    """
    Render the main navigation.

    Returns
    -------
    str
        Selected page.
    """

    return st.sidebar.radio(

        "Navigation",

        [

            "Assistant",

            "Knowledge Explorer",

            "System Health",

            "Settings"

        ]

    )


# =========================================================
# HEALTH SUMMARY
# =========================================================

def health_summary(
    health: Dict
):
    """
    Display a compact health summary.
    """

    st.sidebar.subheader(
        "System Status"
    )

    application = health.get(

        "application",

        False

    )

    if application:

        st.sidebar.success(

            "Application Running"

        )

    else:

        st.sidebar.error(

            "Application Stopped"

        )

    database = health.get(

        "database",

        {}

    )

    if isinstance(database, dict):

        st.sidebar.caption(

            f"Database: "

            f"{database.get('status', 'Unknown')}"

        )

    assistant = health.get(

        "assistant",

        {}

    )

    if assistant:

        ready = all(

            assistant.values()

        )

        if ready:

            st.sidebar.success(

                "Assistant Ready"

            )

        else:

            st.sidebar.warning(

                "Assistant Partially Ready"

            )

    st.sidebar.divider()


# =========================================================
# SIMPLE SIDEBAR SECTION
# =========================================================

def sidebar_section(
    title: str
):
    """
    Render a sidebar section heading.
    """

    st.sidebar.markdown(

        f"### {title}"

    )
# =========================================================
# MODEL SELECTION
# =========================================================

def model_selector(
    models: List[str],
    current_model: Optional[str] = None
) -> str:
    """
    Display available LLM models.

    Parameters
    ----------
    models:
        Installed Ollama models.

    current_model:
        Currently active model.

    Returns
    -------
    str
        Selected model.
    """

    sidebar_section(

        "Language Model"

    )

    if not models:

        st.sidebar.warning(

            "No models detected."

        )

        return ""

    if current_model not in models:

        current_model = models[0]

    index = models.index(

        current_model

    )

    selected = st.sidebar.selectbox(

        "Model",

        options=models,

        index=index

    )

    st.sidebar.caption(

        f"Active Model: {selected}"

    )

    st.sidebar.divider()

    return ModelSelection(
    
        selected_model=selected,
    
        changed=(
    
            selected != current_model
    
        )
    
    )

# =========================================================
# KNOWLEDGE SUMMARY
# =========================================================

def knowledge_summary(
    statistics: Dict
):
    """
    Display knowledge base statistics.
    """

    sidebar_section(

        "Knowledge Base"

    )

    if not statistics:

        st.sidebar.info(

            "Statistics unavailable."

        )

        st.sidebar.divider()

        return

    #
    # Format statistics first
    #

    statistics = format_statistics(

        statistics

    )

    #
    # Display metrics
    #

    for label, value in statistics.items():

        st.sidebar.metric(

            label,

            value

        )

    st.sidebar.divider()

# =========================================================
# CONVERSATION CONTROLS
# =========================================================

def conversation_controls() -> Dict:
    """
    Display conversation controls.

    Returns
    -------
    Dict
        Button states.
    """

    sidebar_section(

        "Conversation"

    )

    new_chat = st.sidebar.button(

        "🆕 New Conversation",

        use_container_width=True

    )

    clear_chat = st.sidebar.button(

        "🗑️ Clear Chat",

        use_container_width=True

    )

    export_chat = st.sidebar.button(

        "📄 Export Conversation",

        use_container_width=True

    )

    st.sidebar.divider()

    return {

        "new_chat": new_chat,

        "clear_chat": clear_chat,

        "export_chat": export_chat

    }


# =========================================================
# SESSION SUMMARY
# =========================================================

def session_summary(
    message_count: int,
    response_count: int
):
    """
    Display session statistics.
    """

    sidebar_section(

        "Session"

    )

    col1, col2 = st.sidebar.columns(2)

    with col1:

        st.metric(

            "Messages",

            message_count

        )

    with col2:

        st.metric(

            "Responses",

            response_count

        )

    st.sidebar.divider()
# =========================================================
# SETTINGS PANEL
# =========================================================

def settings_panel() -> SidebarSettings:
    """
    Display application settings.

    Returns
    -------
    Dict
        Selected settings.
    """

    sidebar_section(

        "Settings"

    )

    streaming = st.sidebar.toggle(

        "Enable Streaming",

        value=settings.ui.enable_streaming

    )

    show_statistics = st.sidebar.toggle(

        "Show Statistics",

        value=settings.ui.show_statistics

    )

    show_visualizations = st.sidebar.toggle(

        "Show Visualizations",

        value=settings.ui.show_visualizations

    )

    show_curiosity = st.sidebar.toggle(

        "Show Curiosity Questions",

        value=settings.ui.show_curiosity

    )

    st.sidebar.divider()

    return SidebarSettings(
        
        streaming=streaming,
        
        statistics=show_statistics,
        
        visualizations=show_visualizations,
        
        curiosity=show_curiosity
    
    )


# =========================================================
# DEBUG PANEL
# =========================================================

def debug_panel(
    debug_information: Dict
):
    """
    Display debug information.
    """

    sidebar_section(

        "Debug"

    )

    if not debug_information:

        st.sidebar.info(

            "Debug information unavailable."

        )

        st.sidebar.divider()

        return

    with st.sidebar.expander(

        "Debug Information",

        expanded=False

    ):

        st.json(

            debug_information

        )

    st.sidebar.divider()


# =========================================================
# ABOUT PANEL
# =========================================================

def about_panel():
    """
    Display project information.
    """

    sidebar_section(

        "About"

    )

    st.sidebar.markdown(

        f"**{settings.project_name}**"

    )

    st.sidebar.caption(

        settings.application_description

    )

    st.sidebar.write(

        f"Version: {settings.version}"

    )

    st.sidebar.write(

        f"Author: {settings.author}"

    )

    st.sidebar.divider()
# =========================================================
# FOOTER
# =========================================================

def sidebar_footer():
    """
    Display sidebar footer.
    """

    st.sidebar.markdown("---")

    st.sidebar.caption(

        f"{settings.project_name}"

    )

    st.sidebar.caption(

        f"Version {settings.version}"

    )
# =========================================================
# PUBLIC API
# =========================================================

__all__ = [

    "SidebarSettings",

    "sidebar_header",

    "navigation",

    "health_summary",

    "sidebar_section",

    "model_selector",

    "knowledge_summary",

    "conversation_controls",

    "session_summary",

    "settings_panel",

    "debug_panel",

    "about_panel",

    "sidebar_footer"

]