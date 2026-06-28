"""
=========================================================
Research Navigator
Notebook Setup Utility
Version : 1.0
=========================================================

Purpose
-------
✓ Configure notebook environment
✓ Add project root to Python path
✓ Reload project modules
✓ Verify project structure
✓ Verify Ollama (optional)

Usage
-----

from utils.notebook_setup import setup_project

setup_project()

Author : Vedang Singh
"""

from __future__ import annotations

import sys
import importlib
from pathlib import Path


# ==========================================================
# PROJECT ROOT
# ==========================================================

def get_project_root() -> Path:
    """
    Detect project root from notebooks folder.
    """

    return Path.cwd().parent


# ==========================================================
# PYTHON PATH
# ==========================================================

def add_project_to_path():

    root = get_project_root()

    if str(root) not in sys.path:

        sys.path.insert(0, str(root))

    return root


# ==========================================================
# VERIFY FOLDERS
# ==========================================================

def verify_project():

    root = get_project_root()

    required = [

        "core",

        "agents",

        "knowledge",

        "notebooks"

    ]

    print("=" * 60)

    print("PROJECT VERIFICATION")

    print("=" * 60)

    print("Root :", root)

    print()

    for folder in required:

        exists = (root / folder).exists()

        status = "OK" if exists else "MISSING"

        print(f"{folder:<15} {status}")

    print("=" * 60)


# ==========================================================
# RELOAD MODULE
# ==========================================================

def reload_module(module_name: str):

    try:

        module = importlib.import_module(module_name)

        importlib.reload(module)

        print(f"Reloaded : {module_name}")

    except ModuleNotFoundError:

        print(f"Not Found : {module_name}")

    except Exception as e:

        print(f"Error     : {module_name}")

        print(e)


# ==========================================================
# RELOAD PROJECT
# ==========================================================

def reload_project():

    modules = [

        "core.schema",

        "core.builder",

        "core.knowledge",

        "core.database",

        "core.quality",

        "agents.ollama_client",

        "agents.research_assistant"

    ]

    print()

    print("=" * 60)

    print("RELOADING MODULES")

    print("=" * 60)

    print()

    for module in modules:

        reload_module(module)

    print()

    print("=" * 60)

    print("Reload Complete")

    print("=" * 60)


# ==========================================================
# PYTHON INFO
# ==========================================================

def python_info():

    print()

    print("=" * 60)

    print("PYTHON")

    print("=" * 60)

    print(sys.version)

    print()


# ==========================================================
# OLLAMA STATUS
# ==========================================================

def ollama_status():

    try:

        from agents.ollama_client import OllamaClient

        client = OllamaClient()

        print("=" * 60)

        print("OLLAMA")

        print("=" * 60)

        if client.is_running():

            print("Status : Running")

            print()

            print("Installed Models")

            print("----------------")

            for model in client.list_models():

                print(model)

        else:

            print("Status : Not Running")

        print("=" * 60)

        print()

    except Exception as e:

        print()

        print("Could not verify Ollama")

        print(e)

        print()


# ==========================================================
# COMPLETE SETUP
# ==========================================================

def setup_project(

    reload_modules: bool = True,

    show_python: bool = False,

    check_ollama: bool = True

):

    root = add_project_to_path()

    print()

    print("=" * 60)

    print("RESEARCH NAVIGATOR")

    print("=" * 60)

    print("Project Root")

    print(root)

    print("=" * 60)

    verify_project()

    if reload_modules:

        reload_project()

    if show_python:

        python_info()

    if check_ollama:

        ollama_status()

    print()

    print("Notebook Ready.")

    print()


# ==========================================================
# PUBLIC API
# ==========================================================

__all__ = [

    "setup_project",

    "reload_project",

    "verify_project",

    "ollama_status",

    "python_info"

]