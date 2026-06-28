"""
=========================================================
Research Navigator

Streamlit Application

Version : 3.0

=========================================================

Main Streamlit interface.

Responsibilities

• Configure page

• Initialize UI state

• Render sidebar

• Render chat

• Coordinate backend

=========================================================
"""

from __future__ import annotations

import streamlit as st

from core.config import settings

from research_assistant import ResearchAssistant

#
# UI Components
#

from ui.components import (

    page_header,

    user_message,

    display_response

)

from ui.sidebar import (

    sidebar_header,

    navigation,

    health_summary,

    model_selector,

    knowledge_summary,

    conversation_controls,

    session_summary,

    settings_panel,

    debug_panel,

    about_panel,

    sidebar_footer

)

from ui.state import (

    UIState,

    add_user_message,

    add_assistant_message,

    clear_messages

)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(

    page_title=settings.ui.page_title,

    page_icon=settings.ui.page_icon,

    layout=settings.ui.layout,

    initial_sidebar_state=settings.ui.sidebar_state

)

# =========================================================
# APPLICATION STYLE
# =========================================================

st.markdown(
    """
    <style>

    .block-container{
        padding-top:2rem;
        padding-bottom:2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SESSION INITIALIZATION
# =========================================================

def initialize_session():
    """
    Initialize Streamlit session state.
    """

    if "ui" in st.session_state:

        return

    assistant = ResearchAssistant()

    models = assistant.available_models()

    current_model = (

        models[0]

        if models

        else ""

    )

    st.session_state.ui = UIState(

        assistant=assistant,

        current_model=current_model

    )


# =========================================================
# GET UI STATE
# =========================================================

def state() -> UIState:
    """
    Return the active UI state.
    """

    return st.session_state.ui
# =========================================================
# SIDEBAR
# =========================================================

def render_sidebar() -> dict:
    """
    Render the complete sidebar.

    Returns
    -------
    dict
        Sidebar selections.
    """

    ui = state()

    sidebar_header()

    #
    # Navigation
    #

    page = navigation()

    #
    # Health
    #

    health_summary(

        ui.last_health = ui.assistant.health()

    )

    #
    # Model
    #

    model = model_selector(

        models=ui.assistant.available_models(),

        current_model=ui.current_model

    )

    #
    # Knowledge
    #

    try:

        statistics = ui.assistant.knowledge.statistics()

    except Exception:

        statistics = {}

    knowledge_summary(

        statistics

    )

    #
    # Conversation
    #

    conversation = conversation_controls()

    #
    # Session
    #

    session_summary(

        message_count=len(

            ui.messages

        ),

        response_count=1

        if ui.last_response

        else 0

    )

    #
    # Settings
    #

    settings_result = settings_panel()

    ui.sidebar_settings = settings_result

    #
    # Debug
    #

    if ui.debug_enabled:

        debug_panel(

            ui.assistant.debug_pipeline()

        )

    #
    # About
    #

    about_panel()

    sidebar_footer()

    return {

        "page": page,

        "model": model,

        "conversation": conversation,

        "settings": settings_result

    }


# =========================================================
# CHAT HISTORY
# =========================================================

def render_chat():
    """
    Render conversation history.
    """

    ui = state()

    for message in ui.messages:

        if message.role == "user":

            user_message(

                message.content

            )

        else:

            st.chat_message(

                "assistant"

            ).markdown(

                message.content

            )
# =========================================================
# HANDLE USER INPUT
# =========================================================

def handle_user_input():
    """
    Process user questions.
    """

    ui = state()

    question = st.chat_input(

        "Ask a research question..."

    )

    if not question:

        return

    #
    # Store user message
    #

    add_user_message(

        ui,

        question

    )

    #
    # Display user message
    #

    user_message(

        question

    )

    #
    # Generate response
    #

    with st.spinner(

        "Researching..."

    ):

        result = ui.assistant.ask(

            question

        )

    #
    # Save latest response
    #

    ui.last_response = result

    #
    # Store assistant message
    #

    add_assistant_message(

        ui,

        result.response

    )

    #
    # Display response
    #

    display_response(

        result

    )


# =========================================================
# MAIN PAGE
# =========================================================

def render_page():
    """
    Render the main application.
    """

    initialize_session()

    ui = state()

    #
    # Refresh health
    #

    ui.last_health = (

        ui.assistant.health()

    )

    #
    # Sidebar
    #

    sidebar = render_sidebar()

    #
    # Conversation buttons
    #

    controls = sidebar[

        "conversation"

    ]

    if controls.get(

        "clear_chat"

    ):

        clear_messages(

            ui

        )

        st.rerun()

    #
    # Header
    #

    page_header()

    #
    # Existing chat
    #

    render_chat()

    #
    # User input
    #

    handle_user_input() 
# =========================================================
# APPLICATION
# =========================================================

def main():
    """
    Main Streamlit application.
    """

    render_page()


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":

    main()