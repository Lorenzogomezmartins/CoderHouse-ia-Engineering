import asyncio
import os

from dotenv import load_dotenv
from pydantic import SecretStr, ValidationError

from manager import AsyncLLMManager
from schemas import ChatMessage, LLMConfig, Provider


load_dotenv()


def crear_configuracion() -> LLMConfig:

    provider = os.getenv(
        "LLM_PROVIDER",
        "gemini"
    ).lower()

    if provider == "openai":

        return LLMConfig(
            provider=Provider.OPENAI,
            model=os.getenv(
                "OPENAI_MODEL",
                "gpt-4o-mini"
            ),
            openai_api_key=SecretStr(
                os.getenv("OPENAI_API_KEY", "")
            ),
            temperature=0.7,
            max_tokens=200,
        )

    if provider == "anthropic":

        return LLMConfig(
            provider=Provider.ANTHROPIC,
            model=os.getenv(
                "ANTHROPIC_MODEL",
                "claude-3-5-haiku-latest"
            ),
            anthropic_api_key=SecretStr(
                os.getenv("ANTHROPIC_API_KEY", "")
            ),
            temperature=0.7,
            max_tokens=200,
        )

    if provider == "gemini":

        return LLMConfig(
            provider=Provider.GEMINI,
            model=os.getenv(
                "GEMINI_MODEL",
                "gemini-3.8-flash"
            ),
            google_api_key=SecretStr(
                os.getenv("GOOGLE_API_KEY", "")
            ),
            temperature=0.7,
            max_tokens=200,
        )

    raise ValueError(
        f"Proveedor no soportado: {provider}"
    )


async def probar_generacion_normal(
    manager: AsyncLLMManager,
    messages: list[ChatMessage],
):
    print("\n" + "=" * 60)
    print("RESPUESTA NORMAL")
    print("=" * 60)

    resultado = await manager.generate(messages)

    if resultado.error:
        print(f"ERROR: {resultado.error}")
        return

    print(resultado.content)


async def probar_streaming(
    manager: AsyncLLMManager,
    messages: list[ChatMessage],
):
    print("\n" + "=" * 60)
    print("RESPUESTA CON STREAMING")
    print("=" * 60)

    async for fragmento in manager.generate_stream(messages):
        print(fragmento, end="", flush=True)

    print()


def probar_validacion():

    print("\n" + "=" * 60)
    print("PRUEBA DE VALIDACIÓN PYDANTIC")
    print("=" * 60)

    try:

        LLMConfig(
            provider=Provider.GEMINI,
            model="gemini-3.8-flash",
            temperature=5,
            max_tokens=200,
        )

    except ValidationError as error:

        print("Validación detectada correctamente:")
        print(error)


async def probar_error_controlado():

    print("\n" + "=" * 60)
    print("PRUEBA DE ERROR CONTROLADO")
    print("=" * 60)

    config = LLMConfig(
        provider=Provider.GEMINI,
        model=os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        ),
        google_api_key=SecretStr(
            "API_KEY_INVALIDA_PARA_PRUEBA"
        ),
        temperature=0.7,
        max_tokens=100,
    )

    manager = AsyncLLMManager(config)

    messages = [
        ChatMessage(
            role="user",
            content="Hola"
        )
    ]

    resultado = await manager.generate(messages)

    if resultado.error:
        print("El error fue capturado correctamente.")
        print(resultado.error)
    else:
        print("La API respondió inesperadamente.")


async def main():

    print("=" * 60)
    print("UNIFIED ASYNC LLM CLIENT")
    print("=" * 60)

    try:

        config = crear_configuracion()

        print(f"Proveedor: {config.provider.value}")
        print(f"Modelo: {config.model}")

        manager = AsyncLLMManager(config)

        messages = [
            ChatMessage(
                role="user",
                content="¿Qué es la entropía?"
            )
        ]

        await probar_generacion_normal(
            manager,
            messages
        )

        await probar_streaming(
            manager,
            messages
        )

        probar_validacion()

        await probar_error_controlado()

    except Exception as error:

        print("\nERROR NO CONTROLADO:")
        print(error)


if __name__ == "__main__":
    asyncio.run(main())