"""
=========================================================
Research Navigator

Ollama Client

Version : 3.0

=========================================================

Lightweight wrapper around the Ollama Python SDK.

Responsibilities

• Verify server availability

• Verify model availability

• Generate responses

• Stream responses

• Return structured outputs

The Ollama Client never

• Builds prompts

• Retrieves knowledge

• Parses responses

=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from typing import Dict, List, Optional

import ollama

from builder.prompt_builder import PromptResult


# =========================================================
# DEFAULT CONFIGURATION
# =========================================================

from core.config import settings

# =========================================================
# GENERATION CONFIGURATION
# =========================================================

@dataclass
class GenerationConfig:
    """
    Generation parameters supplied
    to Ollama.
    """

    self.client = ollama.Client(

        host=settings.ollama.host

    )
    
    stream: bool = False

    options: Dict = field(
        default_factory=dict
    )


# =========================================================
# OLLAMA RESPONSE
# =========================================================

@dataclass
class OllamaResponse:
    """
    Structured model response.
    """

    model: str = ""

    response: str = ""

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    duration: float = 0.0

    metadata: Dict = field(
        default_factory=dict
    )

# =========================================================
# EXCEPTIONS
# =========================================================

class OllamaClientError(Exception):
    """
    Base exception for Ollama client.
    """
    pass


class OllamaConnectionError(
    OllamaClientError
):
    """
    Raised when the Ollama server
    cannot be reached.
    """
    pass


class OllamaModelNotFoundError(
    OllamaClientError
):
    """
    Raised when the configured
    model does not exist.
    """
    pass

# =========================================================
# OLLAMA CLIENT
# =========================================================

class OllamaClient:
    """
    Thin wrapper around the Ollama SDK.
    """

    def __init__(

        self,

        config: Optional[
            GenerationConfig
        ] = None

    ):

        self.config = (

            config

            or

            GenerationConfig()

        )

        self.client = ollama.Client(

            host=DEFAULT_HOST

        )
    # =====================================================
    # SERVER CONNECTION
    # =====================================================

    def is_server_running(
        self
    ) -> bool:
        """
        Check whether the Ollama server is
        reachable.
        """

        try:

            self.client.list()

            return True

        except Exception:

            return False


    # =====================================================
    # AVAILABLE MODELS
    # =====================================================

    def available_models(
        self
    ) -> List[str]:
        """
        Return every installed model.
        """

        try:

            response = self.client.list()

        except Exception:

            return []

        models = []

        #
        # Compatible with multiple SDK versions.
        #

        if hasattr(response, "models"):

            iterable = response.models

        elif isinstance(response, dict):

            iterable = response.get(

                "models",

                []

            )

        else:

            iterable = []

        for model in iterable:

            #
            # New SDK objects
            #

            if hasattr(model, "model"):

                models.append(

                    model.model

                )

                continue

            #
            # Older dictionary responses
            #

            if isinstance(model, dict):

                name = (

                    model.get("model")

                    or

                    model.get("name")

                )

                if name:

                    models.append(

                        name

                    )

                continue

            #
            # Fallback
            #

            models.append(

                str(model)

            )

        return models


    # =====================================================
    # MODEL EXISTS
    # =====================================================

    def model_exists(
        self,
        model: Optional[str] = None
    ) -> bool:
        """
        Check whether a model exists.
        """

        model = (

            model

            or

            self.config.model

        )

        return (

            model

            in

            self.available_models()

        )


    # =====================================================
    # HEALTH
    # =====================================================

    def health(
        self
    ) -> Dict:
        """
        Return client health information.
        """

        models = self.available_models()

        return {

            "server_running":

                self.is_server_running(),

            "configured_model":

                self.config.model,

            "model_available":

                self.config.model in models,

            "installed_models":

                models,

            "host":

                DEFAULT_HOST

        }


    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(
        self
    ) -> bool:
        """
        Validate the current client.
        """

        if not self.is_server_running():

            raise OllamaConnectionError(

                "Unable to connect to the "
                "Ollama server."

            )

        if not self.model_exists():

            raise OllamaModelNotFoundError(

                f"Model '{self.config.model}' "
                "is not installed."

            )

        return True
    # =====================================================
    # GENERATE
    # =====================================================

    def generate(
        self,
        prompt: PromptResult,
        config: Optional[GenerationConfig] = None
    ) -> OllamaResponse:
        """
        Generate a response using Ollama.
        """

        config = config or self.config

        if not self.validate():

            raise RuntimeError(

                "Ollama server or configured model "
                "is not available."

            )

        response = self.client.generate(

            model=config.model,

            prompt=prompt.full_prompt,

            options={

                "temperature": config.temperature,

                "top_p": config.top_p,

                "num_predict": config.num_predict,

                **config.options

            },

            stream=False

        )

        metadata = {}

        if hasattr(response, "dict"):

            metadata = response.dict()

        elif isinstance(response, dict):

            metadata = response

        return OllamaResponse(

            model=config.model,

            response=metadata.get(

                "response",

                ""

            ),

            prompt_tokens=metadata.get(

                "prompt_eval_count",

                0

            ),

            completion_tokens=metadata.get(

                "eval_count",

                0

            ),

            total_tokens=(

                metadata.get(

                    "prompt_eval_count",

                    0

                )

                +

                metadata.get(

                    "eval_count",

                    0

                )

            ),

            duration=float(

                metadata.get(

                    "total_duration",

                    0

                )

            ),

            metadata=metadata

        )


    # =====================================================
    # STREAM GENERATION
    # =====================================================

    def stream_generate(
        self,
        prompt: PromptResult,
        config: Optional[GenerationConfig] = None
    ):
        """
        Stream tokens from Ollama.

        Yields
        ------
        str
            Individual response chunks.
        """

        config = config or self.config

        self.validate()
        
        stream = self.client.generate(

            model=config.model,

            prompt=prompt.full_prompt,

            options={

                "temperature": config.temperature,

                "top_p": config.top_p,

                "num_predict": config.num_predict,

                **config.options

            },

            stream=True

        )

        for chunk in stream:

            if hasattr(chunk, "dict"):

                chunk = chunk.dict()

            yield chunk.get(

                "response",

                ""

            )
    # =====================================================
    # RESET
    # =====================================================

    def reset(
        self
    ):
        """
        Reserved for future implementations.

        The Ollama client is intentionally
        stateless.
        """

        pass


    # =====================================================
    # DEBUG
    # =====================================================

    def debug(
        self
    ) -> Dict:
        """
        Return diagnostic information.
        """

        return {

            "health": self.health(),

            "configuration": {

                "model":

                    self.config.model,

                "temperature":

                    self.config.temperature,

                "top_p":

                    self.config.top_p,

                "num_predict":

                    self.config.num_predict,

                "stream":

                    self.config.stream

            }

        }


    # =====================================================
    # UPDATE CONFIGURATION
    # =====================================================

    def update_config(
        self,
        **kwargs
    ):
        """
        Update generation configuration.
        """

        for key, value in kwargs.items():

            if hasattr(self.config, key):

                setattr(

                    self.config,

                    key,

                    value

                )


    # =====================================================
    # CURRENT MODEL
    # =====================================================

    @property
    def model(
        self
    ) -> str:
        """
        Active model name.
        """

        return self.config.model
# =========================================================
# PUBLIC API
# =========================================================

__all__ = [

    "GenerationConfig",

    "OllamaResponse",

    "OllamaClient",

    "OllamaClientError",

    "OllamaConnectionError",

    "OllamaModelNotFoundError"

]