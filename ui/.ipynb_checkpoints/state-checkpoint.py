"""
=========================================================
Research Navigator

UI State

Version : 3.0

=========================================================

Central UI state shared across the Streamlit
application.

This module contains NO Streamlit code.

=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from typing import Dict, List, Optional

from research_assistant import ResearchAssistant

from builder.response_builder import ResponseResult

from ui.sidebar import SidebarSettings


# =========================================================
# CHAT MESSAGE
# =========================================================

@dataclass
class ChatMessage:
    """
    Single conversation message.
    """

    role: str

    content: str


# =========================================================
# UI STATE
# =========================================================

@dataclass
class UIState:
    """
    Streamlit session state.
    """

    #
    # Backend
    #

    assistant: ResearchAssistant

    #
    # Conversation
    #

    messages: List[ChatMessage] = field(

        default_factory=list

    )

    #
    # Model
    #

    current_model: str = ""

    #
    # Sidebar
    #

    sidebar_settings: Optional[SidebarSettings] = None

    #
    # Debug
    #

    debug_enabled: bool = False

    #
    # Latest response
    #

    last_response: Optional[ResponseResult] = None

    #
    # Health
    #

    last_health: Dict = field(

        default_factory=dict

    )
# =========================================================
# UI STATE METHODS
# =========================================================

def add_user_message(
    state: UIState,
    message: str
):
    """
    Add a user message to the conversation.
    """

    state.messages.append(

        ChatMessage(

            role="user",

            content=message

        )

    )


def add_assistant_message(
    state: UIState,
    message: str
):
    """
    Add an assistant message to the conversation.
    """

    state.messages.append(

        ChatMessage(

            role="assistant",

            content=message

        )

    )


def clear_messages(
    state: UIState
):
    """
    Clear the current conversation.
    """

    state.messages.clear()

    state.last_response = None


def conversation_length(
    state: UIState
) -> int:
    """
    Number of messages.
    """

    return len(

        state.messages

    )


def has_messages(
    state: UIState
) -> bool:
    """
    Whether a conversation exists.
    """

    return (

        len(

            state.messages

        )

        > 0

    )


# =========================================================
# PUBLIC API
# =========================================================

__all__ = [

    "ChatMessage",

    "UIState",

    "add_user_message",

    "add_assistant_message",

    "clear_messages",

    "conversation_length",

    "has_messages"

]