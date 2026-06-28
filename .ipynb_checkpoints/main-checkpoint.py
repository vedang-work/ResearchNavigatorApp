"""
=========================================================
Research Navigator

Main Entry Point

Version : 3.0

=========================================================

Application bootstrap.

Responsibilities

• Load configuration

• Validate environment

• Initialize database

• Create assistant

• Perform startup checks

• Launch CLI

=========================================================
"""

from __future__ import annotations

import sys

from typing import Dict

from core.config import settings

from builder.response_builder import ResponseResult

from core.database import (

    database_exists,

    initialize_database,

    database_health

)

from research_assistant import (

    ResearchAssistant

)


# =========================================================
# APPLICATION
# =========================================================

class ResearchNavigatorApp:
    """
    Main application controller.
    """

    def __init__(self):

        self.running = False

        self.assistant = None

    # =====================================================
    # STARTUP
    # =====================================================

    def initialize(self):
        """
        Initialize the application.
        """

        #
        # Validate configuration
        #

        settings.validate()

        #
        # Initialize database
        #

        if not database_exists():

            initialize_database()

        #
        # Create assistant
        #

        self.assistant = ResearchAssistant()

        self.running = True

    # =====================================================
    # HEALTH
    # =====================================================

    def health(self) -> Dict:
        """
        Return application health.
        """

        return {

            "application":

                self.running,

            "database":

                database_health(),

            "assistant":

                self.assistant.health()

                if self.assistant

                else None

        }

    # =====================================================
    # BANNER
    # =====================================================

    @staticmethod
    def banner():
        """
        Print startup banner.
        """

        print()

        print("=" * 70)

        print(

            f"{settings.project_name}"

        )

        print(

            f"Version : {settings.version}"

        )

        print("=" * 70)

        print()

    # =====================================================
    # READY MESSAGE
    # =====================================================

    @staticmethod
    def ready():
        """
        Display startup completion.
        """

        print(

            "System initialized successfully."

        )

        print(

            "Type 'help' for available commands."

        )

        print()
    # =====================================================
    # HELP
    # =====================================================

    @staticmethod
    def help():
        """
        Display available commands.
        """

        print()

        print("Available Commands")

        print("------------------------------")

        print("help      Show this help")

        print("health    Display application health")

        print("models    List installed Ollama models")

        print("clear     Clear the screen")

        print("exit      Exit Research Navigator")

        print()

        print("Or simply ask a research question.")

        print()


    # =====================================================
    # CLEAR SCREEN
    # =====================================================

    @staticmethod
    def clear():
        """
        Clear the terminal.
        """

        import os

        os.system(

            "cls"

            if os.name == "nt"

            else "clear"

        )


    # =====================================================
    # PROCESS COMMAND
    # =====================================================

    def process_command(
        self,
        command: str
    ) -> bool:
        """
        Process built-in commands.

        Returns
        -------
        bool
            True if the command was handled.
        """

        command = command.strip().lower()

        if command == "":

            return True

        if command == "help":

            self.help()

            return True

        if command == "health":

            self.print_health()

            return True
            
        if command == "models":

            print()

            for model in self.assistant.available_models():

                print(f"• {model}")

            print()

            return True

        if command == "clear":

            self.clear()

            self.banner()

            return True

        if command in (

            "exit",

            "quit"

        ):

            self.running = False

            return True

        return False


    # =====================================================
    # CLI LOOP
    # =====================================================

    def run_cli(
        self
    ):
        """
        Interactive command-line interface.
        """

        self.banner()

        self.ready()

        while self.running:

            try:

                question = input(

                    "Research Navigator > "

                ).strip()

            except (

                KeyboardInterrupt,

                EOFError

            ):

                print()

                break

            #
            # Built-in command?
            #

            if self.process_command(

                question

            ):

                continue

            #
            # Ask assistant
            #

            try:

                result = self.assistant.ask(

                    question

                )

                self.display_response(

                    result

                )
                
            except Exception as error:

                print()

                print(

                    f"Error: {error}"

                )

                print()
    # =====================================================
    # FORMAT HEALTH
    # =====================================================

    def print_health(
        self
    ):
        """
        Display formatted health information.
        """

        health = self.health()

        print()

        print("=" * 70)

        print("System Health")

        print("=" * 70)

        print(

            f"Application : "

            f"{'Running' if health['application'] else 'Stopped'}"

        )

        database = health.get(

            "database",

            {}

        )

        if isinstance(database, dict):

            print(

                f"Database    : "

                f"{database.get('status', 'Unknown')}"

            )

        else:

            print(

                f"Database    : {database}"

            )

        assistant = health.get(

            "assistant",

            {}

        )

        if isinstance(assistant, dict):

            print()

            print("Assistant Components")

            print("------------------------------")

            for name, state in assistant.items():

                print(

                    f"{name:<20}: {state}"

                )

        print()

        print("=" * 70)

        print()


    # =====================================================
    # STARTUP
    # =====================================================

    def startup(
        self
    ):
        """
        Start the application.
        """

        self.initialize()

        self.banner()

        self.ready()

    # =====================================================
    # DISPLAY RESPONSE
    # =====================================================
    
    def display_response(
        self,
        result: ResponseResult
    ):
        """
        Display a formatted assistant response.
        """
    
        print()
    
        print("=" * 70)
    
        print("Research Navigator Response")
    
        print("=" * 70)
    
        print()
    
        print(
    
            result.response
    
        )
    
        #
        # Optional metadata
        #
    
        if hasattr(result, "metadata"):
    
            metadata = result.metadata
    
            if metadata:
    
                print()
    
                print("-" * 70)
    
                print("Metadata")
    
                print("-" * 70)
    
                for key, value in metadata.items():
    
                    print(
    
                        f"{key}: {value}"
    
                    )
    
        print()
    
        print("=" * 70)
    
        print()

    # =====================================================
    # SHUTDOWN
    # =====================================================

    def shutdown(
        self
    ):
        """
        Gracefully shutdown the application.
        """

        self.running = False

        print()

        print("=" * 70)

        print(

            "Thank you for using "

            f"{settings.project_name}"

        )

        print("=" * 70)

        print()


    # =====================================================
    # RUN
    # =====================================================

    def run(
        self
    ):
        """
        Run the application.
        """

        try:

            self.startup()

            self.run_cli()

        finally:

            self.shutdown()