from typing import AsyncGenerator, List

from anthropic import (
    AsyncAnthropic,
    APIError as AnthropicAPIError,
    APIConnectionError as AnthropicConnectionError,
    RateLimitError as AnthropicRateLimitError,
)

from clients.base import BaseLLMClient
from schemas import ChatMessage, ModelResponse, Provider


class AnthropicClient(BaseLLMClient):

    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float,
        max_tokens: int,
    ):
        self._client = AsyncAnthropic(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def _convertir_mensajes(
        self,
        messages: List[ChatMessage]
    ):
        system_message = None
        mensajes = []

        for message in messages:

            if message.role == "system":
                system_message = message.content

            else:
                mensajes.append({
                    "role": message.role,
                    "content": message.content,
                })

        return mensajes, system_message

    async def generate(
        self,
        messages: List[ChatMessage]
    ) -> ModelResponse:

        try:

            mensajes, system_message = self._convertir_mensajes(messages)

            parametros = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "messages": mensajes,
            }

            if system_message:
                parametros["system"] = system_message

            response = await self._client.messages.create(
                **parametros
            )

            return ModelResponse(
                provider=Provider.ANTHROPIC,
                model=self.model,
                content=response.content[0].text,
            )

        except AnthropicRateLimitError as e:

            return ModelResponse(
                provider=Provider.ANTHROPIC,
                model=self.model,
                content="",
                error=f"Límite de cuota excedido: {e}",
            )

        except AnthropicConnectionError as e:

            return ModelResponse(
                provider=Provider.ANTHROPIC,
                model=self.model,
                content="",
                error=f"Error de conexión: {e}",
            )

        except AnthropicAPIError as e:

            return ModelResponse(
                provider=Provider.ANTHROPIC,
                model=self.model,
                content="",
                error=f"Error de la API de Anthropic: {e}",
            )

    async def generate_stream(
        self,
        messages: List[ChatMessage]
    ) -> AsyncGenerator[str, None]:

        try:

            mensajes, system_message = self._convertir_mensajes(messages)

            parametros = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "messages": mensajes,
            }

            if system_message:
                parametros["system"] = system_message

            async with self._client.messages.stream(
                **parametros
            ) as stream:

                async for texto in stream.text_stream:
                    yield texto

        except (
            AnthropicRateLimitError,
            AnthropicConnectionError,
            AnthropicAPIError,
        ) as e:

            yield f"\n[ERROR durante el streaming de Anthropic: {e}]"