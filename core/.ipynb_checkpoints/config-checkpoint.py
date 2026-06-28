"""
=========================================================
Research Navigator

Configuration

Version : 3.0

=========================================================

Central configuration for the application.

Configuration contains runtime settings.

It intentionally DOES NOT contain project
constants such as section names or entity
types. Those belong in constants.py.

=========================================================
"""

from __future__ import annotations

import os

from dataclasses import dataclass, field

from pathlib import Path

from typing import Any, Dict

from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

DATABASE_DIR = DATA_DIR / "database"

CACHE_DIR = DATA_DIR / "cache"

LOG_DIR = PROJECT_ROOT / "logs"


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

@dataclass
class DatabaseConfig:
    """
    SQLite database configuration.
    """

    filename: str = os.getenv(

        "RN_DATABASE",

        "research_universe.db"

    )

    auto_initialize: bool = True

    backup_on_startup: bool = False

    foreign_keys: bool = True

    timeout: int = 30

    journal_mode: str = "WAL"

    synchronous: str = "NORMAL"

    @property
    def database_path(
        self
    ) -> Path:

        return DATABASE_DIR / self.filename


# =========================================================
# OLLAMA CONFIGURATION
# =========================================================

@dataclass
class OllamaConfig:
    """
    Local LLM configuration.
    """

    host: str = os.getenv(

        "OLLAMA_HOST",

        "http://localhost:11434"

    )

    model: str = os.getenv(

        "OLLAMA_MODEL",

        "llama3.2:3b"

    )

    temperature: float = float(

        os.getenv(

            "OLLAMA_TEMPERATURE",

            "0.2"

        )

    )

    top_p: float = float(

        os.getenv(

            "OLLAMA_TOP_P",

            "0.9"

        )

    )

    num_predict: int = int(

        os.getenv(

            "OLLAMA_NUM_PREDICT",

            "1024"

        )

    )

    stream: bool = False

    options: Dict = field(

        default_factory=dict

    )


# =========================================================
# PROMPT CONFIGURATION
# =========================================================

@dataclass
class PromptConfig:
    """
    Prompt generation configuration.
    """

    include_statistics: bool = True

    include_visual_plan: bool = True

    include_curiosity: bool = True

    include_learning_objectives: bool = True

    include_metadata: bool = False

    max_context_sections: int = 20

    markdown_output: bool = True

    strict_grounding: bool = True
# =========================================================
# USER INTERFACE CONFIGURATION
# =========================================================

@dataclass
class UIConfig:
    """
    Streamlit configuration.
    """

    page_title: str = "Research Navigator"

    page_icon: str = "📚"

    layout: str = "wide"

    sidebar_state: str = "expanded"

    show_debug: bool = False

    enable_streaming: bool = True

    show_statistics: bool = True

    show_visualizations: bool = True

    show_curiosity: bool = True


# =========================================================
# LOGGING CONFIGURATION
# =========================================================

@dataclass
class LoggingConfig:
    """
    Logging configuration.
    """

    enabled: bool = True

    level: str = "INFO"

    log_directory: Path = LOG_DIR

    log_filename: str = "research_navigator.log"

    console_output: bool = True

    file_output: bool = True

    @property
    def log_path(
        self
    ) -> Path:

        return self.log_directory / self.log_filename


# =========================================================
# GLOBAL SETTINGS
# =========================================================

@dataclass
class Settings:
    """
    Complete application configuration.
    """

    application_description: str = (
        "Research Navigator Educational AI Assistant"
    )
    
    database: DatabaseConfig = field(
        default_factory=DatabaseConfig
    )

    ollama: OllamaConfig = field(
        default_factory=OllamaConfig
    )

    prompt: PromptConfig = field(
        default_factory=PromptConfig
    )

    ui: UIConfig = field(
        default_factory=UIConfig
    )

    logging: LoggingConfig = field(
        default_factory=LoggingConfig
    )

    version: str = "3.0"

    project_name: str = "Research Navigator"

    author: str = "Vedang Singh"

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# =========================================================
# SINGLETON SETTINGS
# =========================================================

settings = Settings()
# =========================================================
# SETTINGS METHODS
# =========================================================

def validate() -> bool:
    """
    Validate the complete application configuration.

    Returns
    -------
    bool
        True if the configuration is valid.

    Raises
    ------
    ValueError
        If an invalid configuration value is found.
    """

    #
    # Create required directories
    #

    DATA_DIR.mkdir(

        parents=True,

        exist_ok=True

    )

    DATABASE_DIR.mkdir(

        parents=True,

        exist_ok=True

    )

    CACHE_DIR.mkdir(

        parents=True,

        exist_ok=True

    )

    LOG_DIR.mkdir(

        parents=True,

        exist_ok=True

    )

    #
    # Validate Ollama configuration
    #

    if not settings.ollama.host.strip():

        raise ValueError(

            "OLLAMA_HOST cannot be empty."

        )

    if not settings.ollama.model.strip():

        raise ValueError(

            "OLLAMA_MODEL cannot be empty."

        )

    if not (

        0.0

        <=

        settings.ollama.temperature

        <=

        2.0

    ):

        raise ValueError(

            "Temperature must be between 0 and 2."

        )

    if not (

        0.0

        <

        settings.ollama.top_p

        <=

        1.0

    ):

        raise ValueError(

            "top_p must be between 0 and 1."

        )

    if settings.ollama.num_predict <= 0:

        raise ValueError(

            "num_predict must be positive."

        )

    #
    # Database
    #

    if not settings.database.filename.strip():

        raise ValueError(

            "Database filename cannot be empty."

        )

    return True


# =========================================================
# DEBUG
# =========================================================

def debug() -> Dict[str, Any]:
    """
    Return the active configuration.
    """

    return {

        "project_name": settings.project_name,

        "version": settings.version,

        "author": settings.author,

        "database": {

            "path":

                str(

                    settings.database.database_path

                ),

            "filename":

                settings.database.filename,

            "auto_initialize":

                settings.database.auto_initialize,

            "journal_mode":

                settings.database.journal_mode,

            "synchronous":

                settings.database.synchronous

        },

        "ollama": {

            "host":

                settings.ollama.host,

            "model":

                settings.ollama.model,

            "temperature":

                settings.ollama.temperature,

            "top_p":

                settings.ollama.top_p,

            "num_predict":

                settings.ollama.num_predict,

            "stream":

                settings.ollama.stream

        },

        "prompt": {

            "include_statistics":

                settings.prompt.include_statistics,

            "include_visual_plan":

                settings.prompt.include_visual_plan,

            "include_curiosity":

                settings.prompt.include_curiosity,

            "include_learning_objectives":

                settings.prompt.include_learning_objectives,

            "include_metadata":

                settings.prompt.include_metadata,

            "max_context_sections":

                settings.prompt.max_context_sections,

            "markdown_output":

                settings.prompt.markdown_output,

            "strict_grounding":

                settings.prompt.strict_grounding

        },

        "ui": {

            "page_title":

                settings.ui.page_title,

            "layout":

                settings.ui.layout,

            "sidebar_state":

                settings.ui.sidebar_state,

            "show_debug":

                settings.ui.show_debug

        },

        "logging": {

            "enabled":

                settings.logging.enabled,

            "level":

                settings.logging.level,

            "path":

                str(

                    settings.logging.log_path

                )

        }

    }

# =========================================================
# PUBLIC API
# =========================================================

__all__ = [

    "PROJECT_ROOT",

    "DATA_DIR",

    "DATABASE_DIR",

    "CACHE_DIR",

    "LOG_DIR",

    "DatabaseConfig",

    "OllamaConfig",

    "PromptConfig",

    "UIConfig",

    "LoggingConfig",

    "Settings",

    "settings",

    "validate",

    "debug"

]