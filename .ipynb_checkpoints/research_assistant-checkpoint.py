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

from typing import (

    Dict,

    List,

    Optional

)

from core.ollama_client import (

    OllamaClient,

    OllamaResponse

)

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

# =========================================================
# SESSION
# =========================================================

@dataclass(slots=True)
class AssistantSession:
    """
    Stores conversation state.
    """

    conversation_id: str = ""

    turn_count: int = 0

    last_question: str = ""

    last_intent: Optional[Intent] = None

    last_plan: Optional[PlannerResult] = None

    metadata: Dict[str, str] = field(

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
        """
        Initialize every system component.
        """
    
        self.intent_resolver = IntentResolver()
    
        self.knowledge_planner = KnowledgePlanner()
    
        self.context_builder = ContextBuilder()
    
        self.prompt_builder = PromptBuilder()
    
        self.response_builder = ResponseBuilder()
    
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

            raise RuntimeError(
        
                "Ollama client has not been initialized."
        
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

        self.session.last_question = question

        self.session.last_intent = intent

        # -----------------------------------------
        # Build educational plan
        # -----------------------------------------

        planner = self._build_plan(

            intent

        )

        self.session.last_plan = planner

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

        # -----------------------------------------
        # Build structured response
        # -----------------------------------------

        result = self._build_response(

            llm_response.response,

            planner

        )

        return result


    # =====================================================
    # SESSION INFO
    # =====================================================

    def session_info(
        self
    ) -> Dict[str, object]:
        """
        Return current session information.
        """
    
        return {
    
            "conversation_id":
    
                self.session.conversation_id,
    
            "turn_count":
    
                self.session.turn_count,
    
            "last_question":
    
                self.session.last_question,
    
            "last_intent":
    
                (
    
                    self.session.last_intent.intent
    
                    if self.session.last_intent
    
                    else None
    
                ),
    
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
        intermediate pipeline results.
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
    
            "question":
    
                question,
    
            "intent":
    
                intent,
    
            "planner":
    
                planner,
    
            "context":
    
                context,
    
            "prompt":
    
                prompt,
    
            "session":
    
                self.session_info()
    
        }
    
    # =====================================================
    # RESET SESSION
    # =====================================================

    def reset(
        self
    ) -> None:
        """
        Reset the assistant state.
        """
    
        self.session = AssistantSession()
    
        self.intent_resolver.reset()
    
        self.knowledge_planner.reset()
    
        self.context_builder.reset()
    
        self.prompt_builder.reset()
    
        self.response_builder.reset()

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    def health(
        self
    ) -> Dict[str, bool]:
        """
        Return health information about all
        assistant components.
        """
    
        ollama_health = False
    
        try:
    
            ollama_health = self.ollama.health()
    
        except Exception:
    
            ollama_health = False
    
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
    
            "ollama":
    
                ollama_health
    
        }

    # =====================================================
    # AVAILABLE MODELS
    # =====================================================
    
    def available_models(
        self
    ) -> List[str]:
        """
        Return installed Ollama models.
        """
    
        try:
    
            return self.ollama.available_models()
    
        except Exception:
    
            return []
    
    # =====================================================
    # VALIDATE
    # =====================================================
    
    def validate(
        self
    ) -> Dict[str, bool]:
        """
        Validate every assistant component.
        """
    
        ollama_valid = False
    
        try:
    
            ollama_valid = self.ollama.validate()
    
        except Exception:
    
            ollama_valid = False
    
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
    
                ollama_valid
    
        }


    # =====================================================
    # COMPONENTS
    # =====================================================

    def components(
        self
    ) -> Dict[str, object]:
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