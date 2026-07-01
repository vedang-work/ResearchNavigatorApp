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

from typing import Any, Dict, List, Optional, Iterator

import ollama

from builder.prompt_builder import PromptResult

from core.config import settings

# =========================================================
# GENERATION CONFIGURATION
# =========================================================

@dataclass(slots=True)
class GenerationConfig:
    """
    Generation parameters supplied
    to Ollama.
    """

    host: str = settings.ollama.host

    model: str = settings.ollama.model

    temperature: float = settings.ollama.temperature

    top_p: float = settings.ollama.top_p

    num_predict: int = settings.ollama.num_predict

    stream: bool = settings.ollama.stream

    options: Dict[str, Any] = field(
        default_factory=dict
    )

# =========================================================
# OLLAMA RESPONSE
# =========================================================

@dataclass(slots=True)
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

    metadata: Dict[str, Any] = field(
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

            host=self.config.host

        )
    # =====================================================
    # SERVER CONNECTION
    # =====================================================

    def is_server_running(
        self
    ) -> bool:
        """
        Check server availability.
        """
    
        return self.health().get(
    
            "server_running",
    
            False
    
        )

    # =====================================================
    # AVAILABLE MODELS
    # =====================================================

    def available_models(
        self
    ) -> List[str]:
        """
        Return installed model names.
        """
    
        return self.health().get(
    
            "installed_models",
    
            []
    
        )

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
    
        model = model or self.config.model
    
        return (
    
            model
    
            in
    
            self.health().get(
    
                "installed_models",
    
                []
    
            )
    
        )

    # =====================================================
    # HEALTH
    # =====================================================

    def health(
        self
    ) -> Dict[str, Any]:
        """
        Return client health information.
        """
    
        try:
    
            response = self.client.list()
    
            if hasattr(response, "models"):
    
                iterable = response.models
    
            elif isinstance(response, dict):
    
                iterable = response.get(
    
                    "models",
    
                    []
    
                )
    
            else:
    
                iterable = []
    
            models = []
    
            for model in iterable:
    
                if hasattr(model, "model"):
    
                    models.append(
    
                        model.model
    
                    )
    
                elif isinstance(model, dict):
    
                    models.append(
    
                        model.get(
    
                            "model",
    
                            model.get(
    
                                "name",
    
                                ""
    
                            )
    
                        )
    
                    )
    
                else:
    
                    models.append(
    
                        str(model)
    
                    )
    
            return {
    
                "server_running": True,
    
                "configured_model":
    
                    self.config.model,
    
                "model_available":
    
                    self.config.model in models,
    
                "installed_models":
    
                    models,
    
                "host":
    
                    self.config.host
    
            }
    
        except Exception:
    
            return {
    
                "server_running": False,
    
                "configured_model":
    
                    self.config.model,
    
                "model_available": False,
    
                "installed_models": [],
    
                "host":
    
                    self.config.host
    
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
    # RESPONSE NORMALIZATION
    # =====================================================
    
    def _response_to_dict(
        self,
        response: Any
    ) -> Dict[str, Any]:
        """
        Convert an Ollama SDK response into a dictionary.
    
        Supports both older and newer SDK versions.
        """
    
        if isinstance(response, dict):
    
            return response
    
        if hasattr(response, "model_dump"):
    
            return response.model_dump()
    
        if hasattr(response, "dict"):
    
            return response.dict()
    
        return {}
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

        self.validate()

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

        metadata = self._response_to_dict(

            response

        )
        
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
    ) -> Iterator[str]:
        """
        Stream response chunks from Ollama.
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
    
            stream=config.stream
    
        )
    
        for chunk in stream:
    
            chunk = self._response_to_dict(
    
                chunk
    
            )
    
            text = chunk.get(
    
                "response",
    
                ""
    
            )
    
            if text:
    
                yield text
    
    # =====================================================
    # RESET
    # =====================================================

    def reset(
        self
    ) -> None:
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
    ) -> Dict[str, Any]:
        """
        Return diagnostic information.
        """
    
        return {
    
            "health":
    
                self.health(),
    
            "configuration": {
    
                "host":
    
                    self.config.host,
    
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
    ) -> None:
        """
        Update generation configuration.
        """
    
        for key, value in kwargs.items():
    
            if hasattr(
    
                self.config,
    
                key
    
            ):
    
                setattr(
    
                    self.config,
    
                    key,
    
                    value
    
                )
    
        #
        # Recreate SDK client
        #
    
        self.client = ollama.Client(
    
            host=self.config.host
    
        )

    # =====================================================
    # CURRENT MODEL
    # =====================================================

    @property
    def model(
        self
    ) -> str:
        """
        Active model.
        """
    
        return self.config.model
    
    
    @model.setter
    def model(
        self,
        value: str
    ):
    
        value = value.strip()
    
        if not value:
    
            raise ValueError(
    
                "Model name cannot be empty."
    
            )
    
        self.config.model = value
    
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