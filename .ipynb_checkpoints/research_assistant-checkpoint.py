"""
=========================================================
Research Navigator

Research Assistant

Version : 3.0

=========================================================

Main orchestration layer.

Coordinates every component of the system.

Responsibilities

• Resolve intent

• Plan retrieval

• Retrieve context

• Build prompts

• Query the LLM

• Build final responses

=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from typing import Dict, Optional

from core.ollama_client import OllamaResponse

from agents.intent_resolver import (
    IntentResolver,
    Intent
)

from agents.knowledge_planner import (
    KnowledgePlanner,
    PlannerResult
)

from builder.context_builder import (
    ContextBuilder,
    ContextResult
)

from builder.prompt_builder import (
    PromptBuilder,
    PromptResult
)

from builder.response_builder import (
    ResponseBuilder,
    ResponseResult
)

from core.config import settings

print(settings.version)
print(settings.project_name)
print(settings.application_description)

# =========================================================
# SESSION
# =========================================================

@dataclass
class AssistantSession:
    """
    Stores conversation state.
    """

    conversation_id: str = ""

    turn_count: int = 0

    metadata: Dict = field(
        default_factory=dict
    )


# =========================================================
# RESEARCH ASSISTANT
# =========================================================

class ResearchAssistant:
    """
    Main application controller.
    """

    def __init__(self):

        self.intent_resolver = IntentResolver()

        self.knowledge_planner = KnowledgePlanner()

        self.context_builder = ContextBuilder()

        self.prompt_builder = PromptBuilder()

        self.response_builder = ResponseBuilder()

        # Ollama client will be added later

        self.ollama = OllamaClient()

        self.session = AssistantSession()
    # =====================================================
    # INTENT
    # =====================================================

    def _resolve_intent(
        self,
        question: str
    ) -> Intent:
        """
        Resolve user intent.
        """

        return self.intent_resolver.resolve(
            question
        )


    # =====================================================
    # KNOWLEDGE PLAN
    # =====================================================

    def _build_plan(
        self,
        intent: Intent
    ) -> PlannerResult:
        """
        Build the educational plan.
        """

        return self.knowledge_planner.execute(
            intent
        )


    # =====================================================
    # CONTEXT
    # =====================================================

    def _build_context(
        self,
        planner: PlannerResult
    ) -> ContextResult:
        """
        Retrieve educational context.
        """

        return self.context_builder.build(
            planner
        )


    # =====================================================
    # PROMPT
    # =====================================================

    def _build_prompt(
        self,
        question: str,
        planner: PlannerResult,
        context: ContextResult
    ) -> PromptResult:
        """
        Build the LLM prompt.
        """

        return self.prompt_builder.build(

            question,

            planner,

            context

        )

    # =====================================================
    # LLM
    # =====================================================

    def _call_llm(
        self,
        prompt: PromptResult
    ) -> OllamaResponse:
        """
        Query the language model.

        Placeholder until OllamaClient
        is implemented.
        """

        if self.ollama is None:

            return (
                "LLM client has not yet been "
                "configured."
            )

        return self.ollama.generate(
            prompt
        )


    # =====================================================
    # RESPONSE
    # =====================================================

    def _build_response(
        self,
        response: str,
        planner: PlannerResult
    ) -> ResponseResult:
        """
        Build the final structured response.
        """

        return self.response_builder.build(

            response,

            planner

        )
    # =====================================================
    # ASK
    # =====================================================

    def ask(
        self,
        question: str
    ) -> ResponseResult:
        """
        Execute the complete Research Navigator
        pipeline.
        """

        # -----------------------------------------
        # Update session
        # -----------------------------------------

        self.session.turn_count += 1

        # -----------------------------------------
        # Resolve intent
        # -----------------------------------------

        intent = self._resolve_intent(

            question

        )

        # -----------------------------------------
        # Build educational plan
        # -----------------------------------------

        planner = self._build_plan(

            intent

        )

        # -----------------------------------------
        # Retrieve context
        # -----------------------------------------

        context = self._build_context(

            planner

        )

        # -----------------------------------------
        # Build prompt
        # -----------------------------------------

        prompt = self._build_prompt(

            question,

            planner,

            context

        )
        # -----------------------------------------
        # Query LLM
        # -----------------------------------------

        llm_response = self._call_llm(
            prompt
        )

        result = self._build_response(
        
            llm_response.response,
        
            planner
        
        )

        # -----------------------------------------
        # Build structured response
        # -----------------------------------------

        result = self._build_response(

            llm_response,

            planner

        )

        return result


    # =====================================================
    # SESSION INFO
    # =====================================================

    def session_info(
        self
    ) -> Dict:
        """
        Return current session information.
        """

        return {

            "conversation_id":

                self.session.conversation_id,

            "turn_count":

                self.session.turn_count,

            "metadata":

                self.session.metadata

        }


    # =====================================================
    # DEBUG PIPELINE
    # =====================================================

    def debug_pipeline(
        self,
        question: str
    ) -> Dict:
        """
        Execute every stage while exposing
        intermediate results.
        """

        intent = self._resolve_intent(
        
            question
        
        )
        
        planner = self._build_plan(
        
            intent
        
        )
        
        context = self._build_context(
        
            planner
        
        )
        
        prompt = self._build_prompt(
        
            question,
        
            planner,
        
            context
        
        )
        
        return {
        
            "intent":
        
                intent,
        
            "planner":
        
                planner,
        
            "context":
        
                context,
        
            "prompt":
        
                prompt
        
        }
    # =====================================================
    # RESET SESSION
    # =====================================================

    def reset(
        self
    ):
        """
        Reset the current assistant session.
        """

        self.session = AssistantSession()

        self.intent_resolver.reset()


    # =====================================================
    # HEALTH CHECK
    # =====================================================

    def health(
        self
    ) -> Dict:
        """
        Return health information about all
        assistant components.
        """

        return {

            "intent_resolver":

                self.intent_resolver is not None,

            "knowledge_planner":

                self.knowledge_planner is not None,

            "context_builder":

                self.context_builder is not None,

            "prompt_builder":

                self.prompt_builder is not None,

            "response_builder":

                self.response_builder is not None,

            "llm":

                self.ollama.health()

        }

    # =====================================================
    # AVAILABLE MODELS
    # =====================================================
    
    def available_models(
        self
    ):
        """
        Return installed Ollama models.
        """
    
        return self.ollama.available_models()

    # =====================================================
    # VALIDATE
    # =====================================================
    
    def validate(
        self
    ) -> Dict:
        """
        Validate assistant components.
        """
    
        return {
    
            "assistant": True,
    
            "intent_resolver":
    
                self.intent_resolver is not None,
    
            "knowledge_planner":
    
                self.knowledge_planner is not None,
    
            "context_builder":
    
                self.context_builder is not None,
    
            "prompt_builder":
    
                self.prompt_builder is not None,
    
            "response_builder":
    
                self.response_builder is not None,
    
            "ollama":
    
                self.ollama.validate()
    
        }


    # =====================================================
    # COMPONENTS
    # =====================================================

    def components(
        self
    ) -> Dict:
        """
        Return references to every component.
        Useful for debugging.
        """

        return {

            "intent_resolver":

                self.intent_resolver,

            "knowledge_planner":

                self.knowledge_planner,

            "context_builder":

                self.context_builder,

            "prompt_builder":

                self.prompt_builder,

            "response_builder":

                self.response_builder,

            "ollama":

                self.ollama

        }

# =========================================================
# PUBLIC API
# =========================================================

__all__ = [

    "AssistantSession",

    "ResearchAssistant"

]