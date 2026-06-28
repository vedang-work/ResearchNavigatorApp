"""
=========================================================
Research Navigator

Database Engine

Version : 3.0

=========================================================

This module is responsible for every interaction
with the SQLite knowledge index.

Responsibilities
----------------

✓ SQLite connection

✓ Database creation

✓ Synchronization

✓ Searching

✓ Relationship lookup

✓ Generic knowledge retrieval

✓ Statistics

This module NEVER performs:

✗ Prompt engineering

✗ LLM inference

✗ Intent detection

✗ Educational planning

Those belong to higher layers.

=========================================================
"""

from __future__ import annotations

# =========================================================
# STANDARD LIBRARY
# =========================================================

import sqlite3

from difflib import get_close_matches

from typing import Any, Dict, List, Optional


# =========================================================
# PROJECT IMPORTS
# =========================================================

import core.knowledge as knowledge

from core.config import settings

from core.constants import (

    ENTITY_TOPIC,

    ENTITY_RESEARCHER,

    ENTITY_PAPER,

    TABLE_TOPICS,

    TABLE_RESEARCHERS,

    TABLE_PAPERS

)


# =========================================================
# DATABASE LOCATION
# =========================================================

DATABASE_PATH = settings.database.database_path

# =========================================================
# SQLITE CONNECTION
# =========================================================

def connect() -> sqlite3.Connection:
    """
    Open a configured SQLite connection.
    """

    conn = sqlite3.connect(

        DATABASE_PATH,

        timeout=settings.database.timeout

    )

    conn.row_factory = sqlite3.Row

    conn.execute(

        f"PRAGMA journal_mode={settings.database.journal_mode};"

    )

    conn.execute(

        f"PRAGMA synchronous={settings.database.synchronous};"

    )

    if settings.database.foreign_keys:

        conn.execute(

            "PRAGMA foreign_keys = ON;"

        )

    return conn

# ---------------------------------------------------------

def close(
    conn: Optional[sqlite3.Connection]
) -> None:
    """
    Close a SQLite connection safely.
    """

    if conn is None:

        return

    try:

        conn.close()

    except sqlite3.Error:

        pass

# =========================================================
# DATABASE UTILITIES
# =========================================================

def database_exists() -> bool:
    """
    Return True if the SQLite database exists.
    """

    return (

        DATABASE_PATH.exists()

        and

        DATABASE_PATH.is_file()

    )

# ---------------------------------------------------------

def delete_database() -> None:
    """
    Delete the SQLite database.

    Useful during development.
    """

    if DATABASE_PATH.exists():

        DATABASE_PATH.unlink()


# ---------------------------------------------------------

def reset_database() -> None:
    """
    Delete and recreate database.
    """

    delete_database()

    initialize_database()
# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def create_tables():
    """
    Create every table required by Research Navigator.

    This function is idempotent and can safely be
    called multiple times.
    """

    conn = connect()

    try:

        cursor = conn.cursor()

        # -----------------------------------------------------
        # TOPICS
        # -----------------------------------------------------
    
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS topics(
    
                id INTEGER PRIMARY KEY AUTOINCREMENT,
    
                name TEXT UNIQUE NOT NULL,
    
                overview TEXT,
    
                quality TEXT,
    
                json_path TEXT
    
            )
            """
        )
    
        # -----------------------------------------------------
        # RESEARCHERS
        # -----------------------------------------------------
    
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS researchers(
    
                id INTEGER PRIMARY KEY AUTOINCREMENT,
    
                name TEXT UNIQUE NOT NULL,
    
                summary TEXT,
    
                json_path TEXT
    
            )
            """
        )
    
        # -----------------------------------------------------
        # PAPERS
        # -----------------------------------------------------
    
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS papers(
    
                id INTEGER PRIMARY KEY AUTOINCREMENT,
    
                title TEXT UNIQUE NOT NULL,
    
                year INTEGER,
    
                summary TEXT,
    
                json_path TEXT
    
            )
            """
        )
    
        # -----------------------------------------------------
        # TOPIC LINKS
        # -----------------------------------------------------
    
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS topic_links(
    
                id INTEGER PRIMARY KEY AUTOINCREMENT,
    
                parent_topic TEXT,
    
                child_topic TEXT
    
            )
            """
        )
    
        # -----------------------------------------------------
        # TOPIC RESEARCHERS
        # -----------------------------------------------------
    
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS topic_researchers(
    
                id INTEGER PRIMARY KEY AUTOINCREMENT,
    
                topic_name TEXT,
    
                researcher_name TEXT
    
            )
            """
        )
    
        # -----------------------------------------------------
        # TOPIC PAPERS
        # -----------------------------------------------------
    
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS topic_papers(
    
                id INTEGER PRIMARY KEY AUTOINCREMENT,
    
                topic_name TEXT,
    
                paper_title TEXT
    
            )
            """
        )
    
        conn.commit()

    finally:

        close(conn)


# =========================================================
# DATABASE CREATION
# =========================================================

def initialize_database() -> bool:
    """
    Initialize the SQLite database.

    Returns
    -------
    bool
        True if initialization succeeds.
    """

    conn = connect()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS metadata (

                key TEXT PRIMARY KEY,

                value TEXT

            )
            """
        )

        conn.commit()

        return True

    finally:

        close(conn)

# =========================================================
# DATABASE VALIDATION
# =========================================================

def table_exists(
    table_name: str
) -> bool:
    """
    Check whether a table exists.
    """

    conn = connect()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT name
    
            FROM sqlite_master
    
            WHERE type='table'
    
            AND name=?
            """,
            (table_name,)
        )
    
        exists = cursor.fetchone() is not None

    finally:

        close(conn)

        return exists


# ---------------------------------------------------------

def database_info() -> Dict[str, Any]:
    """
    Return database information.
    """

    conn = connect()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT name

            FROM sqlite_master

            WHERE type='table'
            """
        )

        tables = sorted(

            row["name"]

            for row in cursor.fetchall()

        )

        return {

            "database_path":

                str(DATABASE_PATH),

            "exists":

                database_exists(),

            "table_count":

                len(tables),

            "tables":

                tables

        }

    finally:

        close(conn)

# =========================================================
# TABLE MAINTENANCE
# =========================================================

def clear_table(
    table_name: str
):
    """
    Remove all rows from a table.
    """

    conn = connect()

    try:

        cursor = conn.cursor()

        cursor.execute(
    
            f"DELETE FROM {table_name}"
    
        )
    
        conn.commit()

    finally:

        close(conn)

# ---------------------------------------------------------

def clear_database() -> None:
    """
    Remove all indexed data while preserving schema.
    """

    tables = [

        TABLE_TOPICS,
    
        TABLE_RESEARCHERS,
    
        TABLE_PAPERS,
    
        TABLE_TOPIC_LINKS,
    
        TABLE_TOPIC_RESEARCHERS,
    
        TABLE_TOPIC_PAPERS
    
    ]
    
    for table in tables:

        clear_table(table)
# =========================================================
# SYNCHRONIZATION ENGINE
# =========================================================

def _json_filename(
    name: str
) -> str:
    """
    Return the JSON filename for an entity.
    """

    return (

        name.strip()

        .replace(

            " ",

            "_"

        )

        + ".json"

    )
    
def synchronize_database() -> Dict[str, int]:
    """
    Synchronize the database with the knowledge repository.
    """

    statistics = {

        TABLE_TOPICS: 0,

        TABLE_RESEARCHERS: 0,

        TABLE_PAPERS: 0

    }

    clear_cache()

    statistics[TABLE_TOPICS] = synchronize_topics()

    statistics[TABLE_RESEARCHERS] = synchronize_researchers()

    statistics[TABLE_PAPERS] = synchronize_papers()

    return statistics
    
def sync_topics() -> None:
    """
    Synchronize all Topic JSON objects into SQLite.

    JSON remains the source of truth.
    SQLite stores searchable metadata only.
    """

    clear_table(TABLE_TOPICS)

    topics = knowledge.load_all_objects(ENTITY_TOPIC)

    conn = connect()

    try:

        cursor = conn.cursor()

        for topic in topics:
    
            schema = knowledge.detect_schema(topic)
    
            if schema == "builder":
    
                identity = topic.get("identity", {})
                learning = topic.get("learning", {})
    
                name = identity.get("name", "")
                overview = learning.get("overview", "")
                quality = identity.get("quality_level", "")
    
            else:
    
                info = knowledge.flatten_for_database(topic)
    
                name = info.get("name", "")
                overview = info.get("overview", "")
                quality = info.get("quality", "")
    
            json_name = _json_filename(name)
    
            cursor.execute(
                """
                INSERT OR REPLACE INTO topics(
                    name,
                    overview,
                    quality,
                    json_path
                )
                VALUES(?,?,?,?)
                """,
                (
                    name,
                    overview,
                    quality,
                    json_name
                )
            )
    
        conn.commit()

    finally:

        close(conn)


# ---------------------------------------------------------

def sync_researchers() -> None:
    """
    Synchronize researchers.
    """

    clear_table(TABLE_RESEARCHERS)

    researchers = knowledge.load_all_objects(
        ENTITY_RESEARCHER
    )

    conn = connect()

    try:

        cursor = conn.cursor()

        for researcher in researchers:
    
            schema = knowledge.detect_schema(
                researcher
            )
    
            if schema == "builder":
    
                identity = researcher.get(
                    "identity",
                    {}
                )
    
                name = identity.get("name", "")
    
                summary = researcher.get(
                    "summary",
                    ""
                )
    
            else:
    
                info = knowledge.flatten_for_database(
                    researcher
                )
    
                name = info.get("name", "")
    
                summary = info.get(
                    "summary",
                    ""
                )
    
            json_name = _json_filename(name)
    
            cursor.execute(
                """
                INSERT OR REPLACE INTO researchers(
                    name,
                    summary,
                    json_path
                )
                VALUES(?,?,?)
                """,
                (
                    name,
                    summary,
                    json_name
                )
            )
    
        conn.commit()

    finally:

        close(conn)


# ---------------------------------------------------------

def sync_papers() -> None:
    """
    Synchronize papers.
    """

    clear_table(TABLE_PAPERS)

    papers = knowledge.load_all_objects(
        ENTITY_PAPER
    )

    conn = connect()

    try:

        cursor = conn.cursor()
    
        for paper in papers:
    
            schema = knowledge.detect_schema(
                paper
            )
    
            if schema == "builder":
    
                identity = paper.get(
                    "identity",
                    {}
                )
    
                title = identity.get(
                    "title",
                    identity.get(
                        "name",
                        ""
                    )
                )
    
                year = identity.get(
                    "year",
                    None
                )
    
                summary = paper.get(
                    "summary",
                    ""
                )
    
            else:
    
                info = knowledge.flatten_for_database(
                    paper
                )
    
                title = info.get(
                    "title",
                    ""
                )
    
                year = info.get(
                    "year",
                    None
                )
    
                summary = info.get(
                    "summary",
                    ""
                )
    
            json_name = _json_filename(title)
            
            cursor.execute(
                """
                INSERT OR REPLACE INTO papers(
                    title,
                    year,
                    summary,
                    json_path
                )
                VALUES(?,?,?,?)
                """,
                (
                    title,
                    year,
                    summary,
                    json_name
                )
            )
    
        conn.commit()

    finally:

        close(conn)


# ---------------------------------------------------------

def sync_relationships() -> None:
    """
    Synchronize topic relationships.

    Parent
    Child

    Topic → Researcher

    Topic → Paper
    """

    clear_table(TABLE_TOPIC_LINKS)

    clear_table(TABLE_TOPIC_RESEARCHERS)

    clear_table(TABLE_TOPIC_PAPERS)

    topics = knowledge.load_all_objects(
        ENTITY_TOPIC
    )

    conn = connect()

    try:

        cursor = conn.cursor()

        for topic in topics:
    
            schema = knowledge.detect_schema(
                topic
            )
    
            if schema == "builder":
    
                identity = topic.get(
                    "identity",
                    {}
                )
    
                relationships = topic.get(
                    "relationships",
                    {}
                )
    
                topic_name = identity.get(
                    "name",
                    ""
                )
    
            else:
    
                topic_name = topic.get(
                    "name",
                    ""
                )
    
                relationships = topic.get(
                    "relationships",
                    {}
                )
    
            # Parent Topics
    
            for parent in relationships.get(
                "parent_topics",
                []
            ):
    
                cursor.execute(
                    """
                    INSERT INTO topic_links(
                        parent_topic,
                        child_topic
                    )
                    VALUES(?,?)
                    """,
                    (
                        parent,
                        topic_name
                    )
                )
    
            # Researchers
    
            for researcher in topic.get(
                "researchers",
                []
            ):
    
                if isinstance(researcher, dict):
    
                    researcher = researcher.get(
                        "name",
                        ""
                    )
    
                cursor.execute(
                    """
                    INSERT INTO topic_researchers(
                        topic_name,
                        researcher_name
                    )
                    VALUES(?,?)
                    """,
                    (
                        topic_name,
                        researcher
                    )
                )
    
            # Papers
    
            for paper in topic.get(
                "papers",
                []
            ):
    
                if isinstance(paper, dict):
    
                    paper = paper.get(
                        "title",
                        ""
                    )
    
                cursor.execute(
                    """
                    INSERT INTO topic_papers(
                        topic_name,
                        paper_title
                    )
                    VALUES(?,?)
                    """,
                    (
                        topic_name,
                        paper
                    )
                )
    
        conn.commit()

    finally:

        close(conn)


# ---------------------------------------------------------

def sync_all() -> None:
    """
    Perform complete synchronization.
    """

    initialize_database()

    sync_topics()

    sync_researchers()

    sync_papers()

    sync_relationships()
# =========================================================
# KNOWLEDGE CACHE
# =========================================================

_ENTITY_CACHE: Dict[str, Dict[str, Dict]] = {
    ENTITY_TOPIC: {},
    ENTITY_RESEARCHER: {},
    ENTITY_PAPER: {}
}


# ---------------------------------------------------------

def refresh_cache() -> None:
    """
    Load all knowledge objects into memory.

    This avoids repeatedly scanning the JSON
    directories for every lookup.
    """

    _ENTITY_CACHE[ENTITY_TOPIC].clear()
    _ENTITY_CACHE[ENTITY_RESEARCHER].clear()
    _ENTITY_CACHE[ENTITY_PAPER].clear()

    # ---------------- Topics ----------------

    for obj in knowledge.load_all_objects(ENTITY_TOPIC):

        schema = knowledge.detect_schema(obj)

        if schema == "builder":

            name = (
                obj.get("identity", {})
                   .get("name", "")
            )

        else:

            name = obj.get("name", "")

        if name:

            _ENTITY_CACHE[ENTITY_TOPIC][
                name.lower()
            ] = obj

    # ---------------- Researchers ----------------

    for obj in knowledge.load_all_objects(ENTITY_RESEARCHER):

        schema = knowledge.detect_schema(obj)

        if schema == "builder":

            name = (
                obj.get("identity", {})
                   .get("name", "")
            )

        else:

            name = obj.get("name", "")

        if name:

            _ENTITY_CACHE[ENTITY_RESEARCHER][
                name.lower()
            ] = obj

    # ---------------- Papers ----------------

    for obj in knowledge.load_all_objects(ENTITY_PAPER):

        schema = knowledge.detect_schema(obj)

        if schema == "builder":

            identity = obj.get("identity", {})

            title = identity.get(
                "title",
                identity.get("name", "")
            )

        else:

            title = obj.get(
                "title",
                obj.get("name", "")
            )

        if title:

            _ENTITY_CACHE[ENTITY_PAPER][
                title.lower()
            ] = obj


# ---------------------------------------------------------

def cache_is_ready() -> bool:
    """
    Return True if cache has been loaded.
    """

    return bool(_ENTITY_CACHE[ENTITY_TOPIC])


# ---------------------------------------------------------

def ensure_cache() -> None:
    """
    Build cache on first use.
    """

    if not cache_is_ready():

        refresh_cache()


# =========================================================
# GENERIC ENTITY LOADER
# =========================================================

def load_entity(
    entity_type: str,
    entity_name: str
) -> Optional[Dict[str, Any]]:
    """
    Generic entity loader.
    """

    ensure_cache()

    entity_type = entity_type.lower()

    entity_name = entity_name.strip().lower()

    if not entity_name:

        return None

    return _ENTITY_CACHE.get(

        entity_type,

        {}

    ).get(

        entity_name

    )

# ---------------------------------------------------------

def load_topic(
    topic_name: str
) -> Optional[Dict[str, Any]]:
    """
    Load Topic.
    """

    return load_entity(

        ENTITY_TOPIC,

        topic_name

    )


# ---------------------------------------------------------

def load_researcher(
    researcher_name: str
) -> Optional[Dict[str, Any]]:
    """
    Load Researcher.
    """

    return load_entity(

        ENTITY_RESEARCHER,

        researcher_name

    )


# ---------------------------------------------------------

def load_paper(
    paper_title: str
) -> Optional[Dict[str, Any]]:
    """
    Load Paper.
    """

    return load_entity(

        ENTITY_PAPER,

        paper_title

    )


# =========================================================
# GENERIC SECTION RETRIEVAL
# =========================================================

def get_entity_section(
    entity_type: str,
    entity_name: str,
    section: str,
    default=None
):
    """
    Generic section loader.
    """

    entity = load_entity(

        entity_type,

        entity_name

    )

    if entity is None:

        return default

    schema = knowledge.detect_schema(

        entity

    )

    if schema == "builder":

        return entity.get(

            section,

            default

        )

    return entity.get(

        section,

        default

    )

# ---------------------------------------------------------

def get_topic_section(
    topic_name: str,
    section: str,
    default=None
):
    """
    Return any Topic section.
    """

    return get_entity_section(

        ENTITY_TOPIC,

        topic_name,

        section,

        default

    )


# ---------------------------------------------------------

def get_researcher_section(
    researcher_name: str,
    section: str,
    default=None
):
    """
    Return any Researcher section.
    """

    return get_entity_section(

        ENTITY_RESEARCHER,

        researcher_name,

        section,

        default

    )


# ---------------------------------------------------------

def get_paper_section(
    paper_title: str,
    section: str,
    default=None
):
    """
    Return any Paper section.
    """

    return get_entity_section(

        ENTITY_PAPER,

        paper_title,

        section,

        default

    )
# =========================================================
# SPECIALIZED TOPIC RETRIEVAL
# =========================================================

def get_topic_identity(
    topic_name: str
) -> Dict:
    """
    Return topic identity.
    """

    return get_topic_section(
        topic_name,
        "identity",
        {}
    )


# ---------------------------------------------------------

def get_topic_learning(
    topic_name: str
) -> Dict:
    """
    Return learning section.
    """

    return get_topic_section(
        topic_name,
        "learning",
        {}
    )


# ---------------------------------------------------------

def get_topic_history(
    topic_name: str
) -> Dict:
    """
    Return history section.
    """

    return get_topic_section(
        topic_name,
        "history",
        {}
    )


# ---------------------------------------------------------

def get_topic_timeline(
    topic_name: str
):
    """
    Return timeline.
    """

    return get_topic_section(
        topic_name,
        "timeline",
        []
    )


# ---------------------------------------------------------

def get_topic_researchers(
    topic_name: str
):
    """
    Return researcher list.
    """

    return get_topic_section(
        topic_name,
        "researchers",
        []
    )


# ---------------------------------------------------------

def get_topic_papers(
    topic_name: str
):
    """
    Return paper list.
    """

    return get_topic_section(
        topic_name,
        "papers",
        []
    )


# ---------------------------------------------------------

def get_topic_applications(
    topic_name: str
):
    """
    Return applications.
    """

    return get_topic_section(
        topic_name,
        "applications",
        []
    )


# ---------------------------------------------------------

def get_topic_future(
    topic_name: str
):
    """
    Return future directions.
    """

    return get_topic_section(
        topic_name,
        "future",
        {}
    )


# ---------------------------------------------------------

def get_topic_faq(
    topic_name: str
):
    """
    Return FAQ.
    """

    return get_topic_section(
        topic_name,
        "faq",
        []
    )


# ---------------------------------------------------------

def get_topic_relationships(
    topic_name: str
):
    """
    Return relationships.
    """

    return get_topic_section(
        topic_name,
        "relationships",
        {}
    )


# =========================================================
# CONVENIENCE HELPERS
# =========================================================

def get_topic_overview(
    topic_name: str
) -> str:
    """
    Return overview text.
    """

    learning = get_topic_learning(
        topic_name
    )

    return learning.get(
        "overview",
        ""
    )


# ---------------------------------------------------------

def get_topic_intuition(
    topic_name: str
) -> str:
    """
    Return intuition.
    """

    learning = get_topic_learning(
        topic_name
    )

    return learning.get(
        "intuition",
        ""
    )


# ---------------------------------------------------------

def get_topic_key_concepts(
    topic_name: str
):
    """
    Return key concepts.
    """

    learning = get_topic_learning(
        topic_name
    )

    return learning.get(
        "key_concepts",
        []
    )


# ---------------------------------------------------------

def get_topic_prerequisites(
    topic_name: str
):
    """
    Return prerequisites.
    """

    learning = get_topic_learning(
        topic_name
    )

    return learning.get(
        "prerequisites",
        []
    )


# ---------------------------------------------------------

def get_topic_takeaways(
    topic_name: str
):
    """
    Return key takeaways.
    """

    learning = get_topic_learning(
        topic_name
    )

    return learning.get(
        "key_takeaways",
        []
    )


# =========================================================
# ENTITY LISTING
# =========================================================

def get_all_topic_names():
    """
    Return all topic names.
    """

    ensure_cache()

    return sorted(

        _ENTITY_CACHE[ENTITY_TOPIC].keys()

    )


# ---------------------------------------------------------

def get_all_researcher_names():
    """
    Return all researcher names.
    """

    ensure_cache()

    return sorted(

        _ENTITY_CACHE[ENTITY_RESEARCHER].keys()

    )


# ---------------------------------------------------------

def get_all_paper_titles():
    """
    Return all paper titles.
    """

    ensure_cache()

    return sorted(

        _ENTITY_CACHE[ENTITY_PAPER].keys()

    )


# ---------------------------------------------------------

def entity_exists(
    entity_type: str,
    entity_name: str
) -> bool:
    """
    Check whether an entity exists.
    """

    ensure_cache()

    return (

        entity_name.lower()

        in

        _ENTITY_CACHE.get(

            entity_type.lower(),

            {}

        )

    )
# =========================================================
# SEARCH ENGINE
# =========================================================

# ---------------------------------------------------------

def _search_entity_names(
    entity_type: str,
    query: str,
    limit: int = 10,
    cutoff: float = 0.55
) -> List[str]:
    """
    Generic fuzzy search.
    """

    ensure_cache()

    query = query.strip().lower()

    if not query:

        return []

    names = sorted(

        _ENTITY_CACHE.get(

            entity_type.lower(),

            {}

        ).keys()

    )

    substring = [

        name

        for name in names

        if query in name

    ]

    fuzzy = get_close_matches(

        query,

        names,

        n=limit,

        cutoff=cutoff

    )

    results = []

    seen = set()

    for item in substring + fuzzy:

        if item in seen:

            continue

        results.append(item)

        seen.add(item)

        if len(results) >= limit:

            break

    return results

# =========================================================
# TOPIC SEARCH
# =========================================================

def search_topics(
    query: str,
    limit: int = 10
) -> List[str]:
    """
    Search topic names.
    """

    return _search_entity_names(

        ENTITY_TOPIC,

        query,

        limit

    )

# ---------------------------------------------------------

def search_researchers(
    query: str,
    limit: int = 10
) -> List[str]:
    """
    Search researchers.
    """

    return _search_entity_names(

        ENTITY_RESEARCHER,

        query,

        limit

    )


# ---------------------------------------------------------

def search_papers(
    query: str,
    limit: int = 10
) -> List[str]:
    """
    Search papers.
    """

    return _search_entity_names(

        ENTITY_PAPER,

        query,

        limit

    )


# =========================================================
# GLOBAL SEARCH
# =========================================================

def search_everything(
    query: str,
    limit_per_type: int = 5
) -> Dict[str, List[str]]:
    """
    Search every supported entity.
    """

    return {

        ENTITY_TOPIC:

            search_topics(

                query,

                limit_per_type

            ),

        ENTITY_RESEARCHER:

            search_researchers(

                query,

                limit_per_type

            ),

        ENTITY_PAPER:

            search_papers(

                query,

                limit_per_type

            )

    }
    
# =========================================================
# SEARCH SUGGESTIONS
# =========================================================

def suggest_entities(
    partial_text: str,
    limit: int = 10
) -> List[str]:
    """
    Return autocomplete suggestions.
    """

    if not partial_text.strip():

        return []

    results = []

    results.extend(

        search_topics(

            partial_text,

            limit

        )

    )

    results.extend(

        search_researchers(

            partial_text,

            limit

        )

    )

    results.extend(

        search_papers(

            partial_text,

            limit

        )

    )

    unique = []

    seen = set()

    for item in results:

        if item in seen:

            continue

        unique.append(item)

        seen.add(item)

        if len(unique) >= limit:

            break

    return unique

# =========================================================
# KNOWLEDGE GRAPH API
# =========================================================

def get_parent_topics(
    topic_name: str
) -> List[str]:
    """
    Return parent topics.
    """

    relationships = get_topic_relationships(
        topic_name
    )

    return relationships.get(
        "parent_topics",
        []
    )


# ---------------------------------------------------------

def get_child_topics(
    topic_name: str
) -> List[str]:
    """
    Return child topics.
    """

    relationships = get_topic_relationships(
        topic_name
    )

    return relationships.get(
        "child_topics",
        []
    )


# ---------------------------------------------------------

def get_related_topics(
    topic_name: str
) -> List[str]:
    """
    Return related topics.
    """

    relationships = get_topic_relationships(
        topic_name
    )

    return relationships.get(
        "related_topics",
        []
    )


# =========================================================

def get_neighbors(
    topic_name: str
) -> List[str]:
    """
    Return every directly connected topic.
    """

    neighbors = []

    neighbors.extend(

        get_parent_topics(
            topic_name
        )

    )

    neighbors.extend(

        get_child_topics(
            topic_name
        )

    )

    neighbors.extend(

        get_related_topics(
            topic_name
        )

    )

    # remove duplicates

    unique = []

    seen = set()

    for topic in neighbors:

        if topic not in seen:

            unique.append(topic)

            seen.add(topic)

    return unique


# =========================================================

def get_learning_path(
    topic_name: str
) -> Dict:
    """
    Return structured learning path.
    """

    return {

        "topic":

            topic_name,

        "prerequisites":

            get_topic_prerequisites(
                topic_name
            ),

        "parents":

            get_parent_topics(
                topic_name
            ),

        "children":

            get_child_topics(
                topic_name
            ),

        "related":

            get_related_topics(
                topic_name
            )

    }


# =========================================================

def explore_topic(
    topic_name: str
) -> Dict:
    """
    Return complete exploration summary.
    """

    return {

        "identity":

            get_topic_identity(
                topic_name
            ),

        "overview":

            get_topic_overview(
                topic_name
            ),

        "neighbors":

            get_neighbors(
                topic_name
            ),

        "applications":

            get_topic_applications(
                topic_name
            ),

        "future":

            get_topic_future(
                topic_name
            )

    }


# =========================================================

def topic_exists(
    topic_name: str
) -> bool:
    """
    Convenience wrapper.
    """

    return entity_exists(
        ENTITY_TOPIC,
        topic_name
    )


# =========================================================

def researcher_exists(
    researcher_name: str
) -> bool:
    """
    Convenience wrapper.
    """

    return entity_exists(
        ENTITY_RESEARCHER,
        researcher_name
    )


# =========================================================

def paper_exists(
    paper_title: str
) -> bool:
    """
    Convenience wrapper.
    """

    return entity_exists(
        ENTITY_PAPER,
        paper_title
    )


# =========================================================

def database_statistics() -> Dict[str, Any]:
    """
    Return database statistics.
    """

    ensure_cache()

    statistics = {

        "topics":

            len(

                _ENTITY_CACHE[
                    ENTITY_TOPIC
                ]

            ),

        "researchers":

            len(

                _ENTITY_CACHE[
                    ENTITY_RESEARCHER
                ]

            ),

        "papers":

            len(

                _ENTITY_CACHE[
                    ENTITY_PAPER
                ]

            )

    }

    statistics["total_entities"] = (

        statistics["topics"]

        +

        statistics["researchers"]

        +

        statistics["papers"]

    )

    statistics["database"] = (

        database_info()

    )

    return statistics

# =========================================================

def warmup() -> None:
    """
    Initialize the database and cache.
    """

    initialize_database()

    create_tables()

    sync_all()

# =========================================================
# GENERIC ENTITY API
# =========================================================

def get_entity_identity(
    entity_type: str,
    entity_name: str
) -> Dict:
    """
    Return identity section for any entity.
    """

    entity = load_entity(
        entity_type,
        entity_name
    )

    if entity is None:
        return {}

    schema = knowledge.detect_schema(entity)

    if schema == "builder":

        return entity.get(
            "identity",
            {}
        )

    return entity


# ---------------------------------------------------------

def get_entity_summary(
    entity_type: str,
    entity_name: str
) -> str:
    """
    Return best available summary.
    """

    entity = load_entity(
        entity_type,
        entity_name
    )

    if entity is None:
        return ""

    schema = knowledge.detect_schema(entity)

    if schema == "builder":

        learning = entity.get(
            "learning",
            {}
        )

        if learning.get("overview"):

            return learning["overview"]

        if entity.get("summary"):

            return entity["summary"]

        return ""

    return entity.get(
        "summary",
        entity.get(
            "overview",
            ""
        )
    )


# ---------------------------------------------------------

def get_entity_tags(
    entity_type: str,
    entity_name: str
):
    """
    Return entity tags.
    """

    identity = get_entity_identity(
        entity_type,
        entity_name
    )

    return identity.get(
        "tags",
        []
    )


# ---------------------------------------------------------

def get_entity_names(
    entity_type: str
):
    """
    Generic entity listing.
    """

    ensure_cache()

    entity_type = entity_type.lower()

    return sorted(

        list(

            _ENTITY_CACHE.get(
                entity_type,
                {}
            ).keys()

        )

    )


# =========================================================
# CACHE MAINTENANCE
# =========================================================

def clear_cache() -> None:
    """
    Clear all in-memory caches.
    """

    try:

        knowledge.clear_cache()

    except AttributeError:

        pass

# ---------------------------------------------------------

def rebuild_cache():
    """
    Rebuild cache.
    """

    clear_cache()

    refresh_cache()


# ---------------------------------------------------------

def rebuild_database() -> None:
    """
    Perform a complete rebuild.
    """

    reset_database()

    create_tables()

    sync_all()

    rebuild_cache()

# =========================================================
# DATABASE HEALTH
# =========================================================

def database_health() -> Dict[str, Any]:
    """
    Return database health information.
    """

    health = {

        "database_exists": database_exists(),

        "database_path": str(DATABASE_PATH),

        "connection": False,

        "tables": 0

    }

    if not health["database_exists"]:

        return health

    conn = None

    conn = connect()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)

            FROM sqlite_master

            WHERE type='table'
            """
        )

        health["tables"] = cursor.fetchone()[0]

        health["connection"] = True

    except sqlite3.Error:

        pass

    finally:

        close(conn)

    return health

# =========================================================
# VERSION
# =========================================================

DATABASE_VERSION = "3.0.0"
# =========================================================
# DATABASE MAINTENANCE
# =========================================================

def vacuum_database() -> None:
    """
    Optimize SQLite storage.
    """

    conn = connect()

    try:
        
        conn.execute("VACUUM")

    finally:
        
        close(conn)


# ---------------------------------------------------------

def optimize_database() -> None:
    """
    Optimize database resources.
    """

    vacuum_database()

    refresh_cache()

# =========================================================
# MODULE INITIALIZATION
# =========================================================

try:

    if settings.database.auto_initialize:

        if not database_exists():

            initialize_database()

            create_tables()

except Exception:

    #
    # Database will be initialized later.
    #

    pass

# =========================================================
# PUBLIC API
# =========================================================

__all__ = [

    # Connection

    "connect",
    "close",

    # Database

    "initialize_database",
    "create_tables",
    "delete_database",
    "reset_database",
    "database_exists",
    "table_exists",
    "database_info",

    # Maintenance

    "clear_table",
    "clear_database",
    "vacuum_database",
    "optimize_database",

    # Synchronization

    "sync_topics",
    "sync_researchers",
    "sync_papers",
    "sync_relationships",
    "sync_all",

    # Cache

    "refresh_cache",
    "rebuild_cache",
    "clear_cache",
    "cache_is_ready",

    # Generic Loaders

    "load_entity",
    "load_topic",
    "load_researcher",
    "load_paper",

    # Generic Retrieval

    "get_entity_section",
    "get_topic_section",
    "get_researcher_section",
    "get_paper_section",

    # Topic Retrieval

    "get_topic_identity",
    "get_topic_learning",
    "get_topic_history",
    "get_topic_timeline",
    "get_topic_researchers",
    "get_topic_papers",
    "get_topic_applications",
    "get_topic_future",
    "get_topic_faq",
    "get_topic_relationships",

    # Helpers

    "get_topic_overview",
    "get_topic_intuition",
    "get_topic_key_concepts",
    "get_topic_prerequisites",
    "get_topic_takeaways",

    # Listings

    "get_all_topic_names",
    "get_all_researcher_names",
    "get_all_paper_titles",

    "entity_exists",
    "topic_exists",
    "researcher_exists",
    "paper_exists",

    # Search

    "search_topics",
    "search_researchers",
    "search_papers",
    "search_everything",
    "suggest_entities",

    # Knowledge Graph

    "get_parent_topics",
    "get_child_topics",
    "get_related_topics",
    "get_neighbors",
    "get_learning_path",
    "explore_topic",

    # Generic Entity API

    "get_entity_identity",
    "get_entity_summary",
    "get_entity_tags",
    "get_entity_names",

    # Statistics

    "database_statistics",
    "database_health",

    # Utilities

    "warmup",
    "rebuild_database",

    # Version

    "DATABASE_VERSION"

]