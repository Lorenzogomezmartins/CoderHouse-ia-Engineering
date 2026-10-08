# Unified Async LLM Client

Cliente unificado y asíncrono para interactuar con diferentes proveedores de modelos de lenguaje mediante una interfaz común.

El proyecto implementa generación normal, streaming asíncrono, validación con Pydantic y manejo controlado de errores.

## Características

* Interfaz común para diferentes proveedores LLM.
* Clientes asíncronos utilizando los SDK oficiales.
* Soporte para OpenAI y Anthropic.
* Soporte adicional para Google Gemini.
* Generación normal mediante `async/await`.
* Streaming mediante generadores asíncronos (`async for` + `yield`).
* Validación de mensajes y configuración mediante Pydantic.
* Manejo controlado de errores de API, conexión y límites de cuota.
* Selección del proveedor mediante una variable de entorno.
* Variables sensibles almacenadas mediante `.env`.

## Estructura

```text
unified-async-llm-client/
│
├── clients/
│   ├── __init__.py
│   ├── base.py
│   ├── openai_client.py
│   ├── anthropic_client.py
│   └── gemini_client.py
│
├── schemas.py
├── manager.py
├── main.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Requisitos

* Python 3.12 o superior
* Cuenta y API Key del proveedor que se quiera utilizar

## Instalación

Crear y activar un entorno virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

## Configuración

Crear un archivo `.env` a partir de `.env.example`.

Ejemplo:

```env
LLM_PROVIDER=gemini

OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=

OPENAI_MODEL=gpt-4o-mini
ANTHROPIC_MODEL=claude-3-5-haiku-latest
GEMINI_MODEL=gemini-3.7-flash
```

Las API Keys deben mantenerse únicamente en `.env`.

El archivo `.env` está incluido en `.gitignore` y no debe subirse al repositorio.

## Proveedores

El proveedor se selecciona mediante:

```env
LLM_PROVIDER=gemini
```

Valores disponibles:

```text
openai
anthropic
gemini
```

El proyecto fue diseñado principalmente para cumplir con la interfaz común entre OpenAI y Anthropic, incorporando Gemini como proveedor adicional.

## Ejecución

Con el entorno virtual activado:

```powershell
python main.py
```

El script realiza las siguientes pruebas:

1. Generación normal mediante `async/await`.
2. Generación mediante streaming.
3. Validación de parámetros con Pydantic.
4. Manejo controlado de errores de API.

La pregunta utilizada para las pruebas es:

```text
¿Qué es la entropía?
```

## Arquitectura

Todos los proveedores implementan la clase abstracta:

```python
BaseLLMClient
```

Esta define dos operaciones principales:

```python
async def generate(...)
```

y:

```python
async def generate_stream(...)
```

Cada proveedor implementa estos métodos utilizando sus respectivos SDK asíncronos.

El `AsyncLLMManager` selecciona el cliente correspondiente según la configuración del proveedor.

## Validación

Pydantic se utiliza para validar:

* Rol y contenido de los mensajes.
* Proveedor seleccionado.
* Modelo.
* Temperatura, con valores entre `0` y `2`.
* Cantidad máxima de tokens.
* API Keys mediante `SecretStr`.

## Streaming

El streaming utiliza generadores asíncronos.

Los fragmentos recibidos de la API se exponen mediante:

```python
async for chunk in stream:
    yield chunk
```

Esto permite procesar la respuesta progresivamente sin bloquear el event loop.

## Manejo de errores

Se contemplan errores relacionados con:

* API Keys inválidas.
* Límites de cuota.
* Rate limiting.
* Errores de conexión.
* Errores de las APIs de los proveedores.

Los errores se devuelven de forma controlada mediante `ModelResponse` o mediante mensajes durante el streaming, evitando que un error de la API provoque un crash inesperado del programa.

## Tecnologías

* Python
* asyncio
* Pydantic
* OpenAI SDK
* Anthropic SDK
* Google GenAI SDK
* python-dotenv

## Autor

Lorenzo Gomez Martins
