"""
=========================================================
Research Navigator

Global Constants

Version : 3.0

Single source of truth for the project.

=========================================================
"""

# =========================================================
# ENTITY TYPES
# =========================================================

ENTITY_TOPIC = "topic"

ENTITY_RESEARCHER = "researcher"

ENTITY_PAPER = "paper"

ENTITY_DATASET = "dataset"

ENTITY_ALGORITHM = "algorithm"


# =========================================================
# KNOWLEDGE SECTIONS
# =========================================================

SECTION_IDENTITY = "identity"

SECTION_OVERVIEW = "overview"

SECTION_CONCEPT = "concept"

SECTION_HISTORY = "history"

SECTION_TIMELINE = "timeline"

SECTION_RESEARCHERS = "researchers"

SECTION_PAPERS = "papers"

SECTION_RELATIONSHIPS = "relationships"

SECTION_APPLICATIONS = "applications"

SECTION_LEARNING = "learning"

SECTION_COMPARISON = "comparison"

SECTION_FUTURE = "future"

SECTION_SUMMARY = "summary"


# =========================================================
# LEARNING PROFILES
# =========================================================

PROFILE_BEGINNER = "beginner"

PROFILE_INTERMEDIATE = "intermediate"

PROFILE_ADVANCED = "advanced"

PROFILE_RESEARCHER = "researcher"


# =========================================================
# TEACHING STRATEGIES
# =========================================================

STRATEGY_CONCEPT_FIRST = "concept_first"

STRATEGY_GUIDED = "guided_learning"

STRATEGY_RESEARCH = "research_driven"

STRATEGY_HISTORY = "historical_journey"

STRATEGY_EXAMPLE = "example_driven"


# =========================================================
# DIFFICULTY
# =========================================================

DIFFICULTY_EASY = "Easy"

DIFFICULTY_MEDIUM = "Medium"

DIFFICULTY_HARD = "Hard"


# =========================================================
# KNOWLEDGE SOURCES
# =========================================================

SOURCE_DATABASE = "database"

SOURCE_WIKIPEDIA = "wikipedia"

SOURCE_ARXIV = "arxiv"

SOURCE_PDF = "pdf"

SOURCE_INTERNET = "internet"


# =========================================================
# VISUAL COMPONENTS
# =========================================================

VISUAL_TIMELINE = "timeline"

VISUAL_CHRONOLOGY = "chronology"

VISUAL_HISTORY = "historical_timeline"

VISUAL_RESEARCH_NETWORK = "research_network"

VISUAL_CITATION_GRAPH = "citation_graph"

VISUAL_KNOWLEDGE_GRAPH = "knowledge_graph"

VISUAL_APPLICATION_MAP = "application_map"

VISUAL_CONCEPT_MAP = "concept_map"

VISUAL_LEARNING_PATH = "learning_path"

VISUAL_COMPARISON_TABLE = "comparison_table"

VISUAL_FUTURE_ROADMAP = "future_roadmap"


# =========================================================
# RESPONSE TYPES
# =========================================================

RESPONSE_MARKDOWN = "markdown"

RESPONSE_JSON = "json"

RESPONSE_TEXT = "text"


# =========================================================
# LLM PROVIDERS
# =========================================================

LLM_OLLAMA = "ollama"

LLM_OPENAI = "openai"

LLM_GEMINI = "gemini"

LLM_CLAUDE = "claude"

# =========================================================
# RESPONSE SECTIONS
# =========================================================

RESPONSE_OVERVIEW = "overview"

RESPONSE_MAIN = "main"

RESPONSE_EXAMPLES = "examples"

RESPONSE_VISUALIZATION = "visualization"

RESPONSE_STATISTICS = "statistics"

RESPONSE_CURIOSITY = "curiosity"

RESPONSE_OBJECTIVES = "learning_objectives"

RESPONSE_SUMMARY = "summary"

# =========================================================
# DATABASE TABLES
# =========================================================

TABLE_TOPICS = "topics"

TABLE_PAPERS = "papers"

TABLE_RESEARCHERS = "researchers"

TABLE_DATASETS = "datasets"

TABLE_RELATIONSHIPS = "relationships"

TABLE_TOPIC_LINKS = "topic_links"

TABLE_TOPIC_RESEARCHERS = "topic_researchers"

TABLE_TOPIC_PAPERS = "topic_papers"

# =========================================================
# PUBLIC API
# =========================================================

__all__ = [

    name

    for name in globals()

    if name.isupper()

]