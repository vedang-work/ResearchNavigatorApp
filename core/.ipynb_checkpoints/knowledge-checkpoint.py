"""
=========================================================
Research Navigator
Knowledge Engine
Version : 2.0
=========================================================

Responsibilities
----------------
✓ Create Knowledge Objects
✓ Validate Objects
✓ Save JSON
✓ Load JSON
✓ Update JSON
✓ Delete JSON
✓ Search JSON
✓ List Objects

This module NEVER communicates directly with SQLite.
Database synchronization is handled exclusively by
core/database.py.

Author : Research Navigator
"""

from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any

from core.schema import *


# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

KNOWLEDGE_FOLDER = PROJECT_ROOT / "knowledge"

TOPICS_FOLDER = KNOWLEDGE_FOLDER / "topics"

RESEARCHERS_FOLDER = KNOWLEDGE_FOLDER / "researchers"

PAPERS_FOLDER = KNOWLEDGE_FOLDER / "papers"


# Create folders automatically

TOPICS_FOLDER.mkdir(parents=True, exist_ok=True)

RESEARCHERS_FOLDER.mkdir(parents=True, exist_ok=True)

PAPERS_FOLDER.mkdir(parents=True, exist_ok=True)


# ==========================================================
# PATH HELPERS
# ==========================================================

def _sanitize_filename(name: str) -> str:
    """
    Convert a title into a safe filename.
    """

    return (
        name.strip()
            .replace("/", "-")
            .replace("\\", "-")
            .replace(":", "-")
            .replace("*", "")
            .replace("?", "")
            .replace('"', "")
            .replace("<", "")
            .replace(">", "")
            .replace("|", "")
            .replace(" ", "_")
    )


def _object_folder(object_type: str) -> Path:
    """
    Return folder for a given object type.
    """

    if object_type == TOPIC:
        return TOPICS_FOLDER

    if object_type == RESEARCHER:
        return RESEARCHERS_FOLDER

    if object_type == PAPER:
        return PAPERS_FOLDER

    raise ValueError(f"Unknown object type : {object_type}")


def _object_path(
    object_type: str,
    object_name: str
) -> Path:
    """
    Full path to JSON object.
    """

    folder = _object_folder(object_type)

    filename = _sanitize_filename(object_name) + ".json"

    return folder / filename


# ==========================================================
# CREATE OBJECT
# ==========================================================

def create_object(data: Dict) -> Dict:
    """
    Creates a deep copy of a knowledge object.

    Supports both

    Legacy Schema

    Builder Schema

    Returns
    -------
    dict
    """

    return copy.deepcopy(data)


# ==========================================================
# DETECT SCHEMA VERSION
# ==========================================================

def detect_schema(obj: Dict) -> str:
    """
    Detect object format.

    Returns

    legacy

    or

    builder
    """

    if "learning" in obj:

        return "builder"

    if "content" in obj:

        return "legacy"

    return "unknown"


# ==========================================================
# OBJECT EXISTS
# ==========================================================

def object_exists(
    object_type: str,
    object_name: str
) -> bool:

    return _object_path(
        object_type,
        object_name
    ).exists()


# ==========================================================
# SAVE OBJECT
# ==========================================================

def save_object(
    obj: Dict,
    overwrite: bool = True
) -> Path:
    """
    Save object to JSON.
    """

    schema = detect_schema(obj)

    if schema == "builder":

        object_type = obj["type"]

        object_name = obj["identity"]["name"]

    elif schema == "legacy":

        object_type = obj["type"]

        object_name = obj["name"]

    else:

        raise ValueError(
            "Unknown schema."
        )

    path = _object_path(
        object_type,
        object_name
    )

    if path.exists() and not overwrite:

        raise FileExistsError(path)

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            obj,
            f,
            indent=4,
            ensure_ascii=False
        )

    return path


# ==========================================================
# LOAD OBJECT
# ==========================================================

def load_object(
    object_type: str,
    object_name: str
) -> Dict:
    """
    Load JSON object.
    """

    path = _object_path(
        object_type,
        object_name
    )

    if not path.exists():

        raise FileNotFoundError(path)

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)
# ==========================================================
# UPDATE OBJECT
# ==========================================================

def update_object(
    obj: Dict
) -> Path:
    """
    Update an existing knowledge object.

    Simply overwrites the existing JSON.
    """

    return save_object(
        obj,
        overwrite=True
    )


# ==========================================================
# DELETE OBJECT
# ==========================================================

def delete_object(
    object_type: str,
    object_name: str
) -> None:
    """
    Delete a knowledge object.
    """

    path = _object_path(
        object_type,
        object_name
    )

    if not path.exists():

        raise FileNotFoundError(path)

    path.unlink()


# ==========================================================
# COPY OBJECT
# ==========================================================

def copy_object(
    object_type: str,
    source_name: str,
    new_name: str
) -> Path:
    """
    Duplicate an existing object.
    """

    source = _object_path(
        object_type,
        source_name
    )

    if not source.exists():

        raise FileNotFoundError(source)

    destination = _object_path(
        object_type,
        new_name
    )

    shutil.copy2(
        source,
        destination
    )

    return destination


# ==========================================================
# RENAME OBJECT
# ==========================================================

def rename_object(
    object_type: str,
    old_name: str,
    new_name: str
) -> Path:
    """
    Rename a knowledge object.
    """

    obj = load_object(
        object_type,
        old_name
    )

    schema = detect_schema(obj)

    if schema == "builder":

        obj["identity"]["name"] = new_name

    else:

        obj["name"] = new_name

    delete_object(
        object_type,
        old_name
    )

    return save_object(obj)


# ==========================================================
# LIST OBJECTS
# ==========================================================

def list_objects(
    object_type: str
) -> List[str]:
    """
    Return every object name.
    """

    folder = _object_folder(
        object_type
    )

    return sorted(

        file.stem

        for file in folder.glob("*.json")

    )


# ==========================================================
# SEARCH OBJECTS
# ==========================================================

def search_objects(
    object_type: str,
    keyword: str
) -> List[str]:
    """
    Search by object filename.

    Case insensitive.
    """

    keyword = keyword.lower()

    results = []

    for name in list_objects(object_type):

        if keyword in name.lower():

            results.append(name)

    return results


# ==========================================================
# LOAD ALL OBJECTS
# ==========================================================

def load_all_objects(
    object_type: str
) -> List[Dict]:
    """
    Load every object of one type.
    """

    objects = []

    for name in list_objects(object_type):

        objects.append(

            load_object(
                object_type,
                name
            )

        )

    return objects


# ==========================================================
# EXPORT OBJECT
# ==========================================================

def export_object(
    object_type: str,
    object_name: str,
    destination: Path
):
    """
    Export a JSON object to another folder.
    """

    destination.mkdir(
        parents=True,
        exist_ok=True
    )

    source = _object_path(
        object_type,
        object_name
    )

    shutil.copy2(

        source,

        destination / source.name

    )


# ==========================================================
# BACKUP ALL OBJECTS
# ==========================================================

def backup_objects(
    object_type: str,
    backup_folder: Path
):
    """
    Backup an entire object collection.
    """

    backup_folder.mkdir(

        parents=True,

        exist_ok=True

    )

    folder = _object_folder(
        object_type
    )

    for file in folder.glob("*.json"):

        shutil.copy2(

            file,

            backup_folder / file.name

        )


# ==========================================================
# OBJECT SUMMARY
# ==========================================================

def object_summary(
    obj: Dict
) -> Dict:
    """
    Return a lightweight summary.

    Useful for UI and search.
    """

    schema = detect_schema(obj)

    if schema == "builder":

        return {

            "name":

                obj["identity"]["name"],

            "type":

                obj["type"],

            "difficulty":

                obj["identity"]["difficulty"],

            "quality":

                obj["identity"]["quality_level"]

        }

    return {

        "name":

            obj["name"],

        "type":

            obj["type"]

    }


# ==========================================================
# DATABASE READY OBJECT
# ==========================================================

def flatten_for_database(
    obj: Dict
) -> Dict:
    """
    Extract a lightweight representation suitable
    for SQLite indexing.
    """

    schema = detect_schema(obj)

    if schema == "builder":

        return {

            "type":

                obj["type"],

            "name":

                obj["identity"]["name"],

            "overview":

                obj["learning"]["overview"],

            "quality":

                obj["identity"]["quality_level"]

        }

    return {

        "type":

            obj["type"],

        "name":

            obj["name"],

        "overview":

            obj.get("overview", "")

    }
# ==========================================================
# VALIDATION
# ==========================================================

def validate_object(obj: Dict):
    """
    Validate a knowledge object.

    Returns
    -------
    (is_valid, missing_fields)
    """

    schema = detect_schema(obj)

    missing = []

    # ------------------------------------------------------
    # Builder Schema
    # ------------------------------------------------------

    if schema == "builder":

        if "type" not in obj:
            missing.append("type")

        # Identity

        identity = obj.get("identity", {})

        if not identity.get("name"):
            missing.append("identity.name")

        if not identity.get("domain"):
            missing.append("identity.domain")

        if not identity.get("difficulty"):
            missing.append("identity.difficulty")

        if not identity.get("quality_level"):
            missing.append("identity.quality_level")

        # Learning

        learning = obj.get("learning", {})

        required_learning = [

            "overview",

            "why_it_matters",

            "intuition",

            "key_concepts",

            "prerequisites",

            "key_takeaways"

        ]

        for field in required_learning:

            if field not in learning:

                missing.append(

                    f"learning.{field}"

                )

        # History

        if "history" not in obj:

            missing.append("history")

        # Timeline

        if "timeline" not in obj:

            missing.append("timeline")

        # Researchers

        if "researchers" not in obj:

            missing.append("researchers")

        # Papers

        if "papers" not in obj:

            missing.append("papers")

        # Applications

        if "applications" not in obj:

            missing.append("applications")

        # Future

        if "future" not in obj:

            missing.append("future")

        # FAQ

        if "faq" not in obj:

            missing.append("faq")

        # Relationships

        if "relationships" not in obj:

            missing.append("relationships")

        return (

            len(missing) == 0,

            missing

        )

    # ------------------------------------------------------
    # Legacy Schema
    # ------------------------------------------------------

    if schema == "legacy":

        required = [

            "type",

            "name",

            "overview",

            "metadata",

            "content",

            "relationships"

        ]

        for field in required:

            if field not in obj:

                missing.append(field)

        return (

            len(missing) == 0,

            missing

        )

    return (

        False,

        ["Unknown schema"]

    )


# ==========================================================
# LEGACY -> BUILDER
# ==========================================================

def legacy_to_builder(
    legacy: Dict
) -> Dict:
    """
    Convert old schema to new schema.
    """

    builder = {

        "type": legacy["type"],

        "identity": {

            "name": legacy["name"],

            **legacy.get(

                "metadata",

                {}

            )

        },

        "learning": {

            "overview":

                legacy.get(

                    "overview",

                    ""

                ),

            **legacy.get(

                "content",

                {}

            )

        },

        "history": {},

        "timeline":

            legacy.get(

                "content",

                {}

            ).get(

                "timeline",

                []

            ),

        "researchers":

            legacy.get(

                "content",

                {}

            ).get(

                "key_researchers",

                []

            ),

        "papers": [],

        "applications":

            legacy.get(

                "content",

                {}

            ).get(

                "applications",

                []

            ),

        "future": {

            "open_problems":

                legacy.get(

                    "content",

                    {}

                ).get(

                    "open_problems",

                    []

                ),

            "future_directions":

                legacy.get(

                    "content",

                    {}

                ).get(

                    "future_directions",

                    []

                )

        },

        "faq":

            legacy.get(

                "content",

                {}

            ).get(

                "faqs",

                []

            ),

        "relationships":

            legacy.get(

                "relationships",

                {}

            )

    }

    return builder


# ==========================================================
# BUILDER -> LEGACY
# ==========================================================

def builder_to_legacy(
    builder: Dict
) -> Dict:
    """
    Convert new schema to legacy schema.
    """

    return {

        "type":

            builder["type"],

        "name":

            builder["identity"]["name"],

        "overview":

            builder["learning"]["overview"],

        "metadata":

            builder["identity"],

        "content": {

            **builder["learning"],

            "timeline":

                builder["timeline"],

            "key_researchers":

                builder["researchers"],

            "applications":

                builder["applications"],

            "open_problems":

                builder["future"][
                    "open_problems"
                ],

            "future_directions":

                builder["future"][
                    "future_directions"
                ],

            "faqs":

                builder["faq"]

        },

        "relationships":

            builder["relationships"]

    }


# ==========================================================
# KNOWLEDGE STATISTICS
# ==========================================================

def knowledge_statistics():

    return {

        "topics":

            len(

                list_objects(TOPIC)

            ),

        "researchers":

            len(

                list_objects(RESEARCHER)

            ),

        "papers":

            len(

                list_objects(PAPER)

            )

    }


# ==========================================================
# PUBLIC API
# ==========================================================

__all__ = [

    "create_object",

    "validate_object",

    "save_object",

    "load_object",

    "update_object",

    "delete_object",

    "copy_object",

    "rename_object",

    "object_exists",

    "list_objects",

    "search_objects",

    "load_all_objects",

    "export_object",

    "backup_objects",

    "object_summary",

    "flatten_for_database",

    "legacy_to_builder",

    "builder_to_legacy",

    "knowledge_statistics"

]