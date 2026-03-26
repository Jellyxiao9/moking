from openai import OpenAI
from app.infrastructure.config import get_settings

settings = get_settings()


def get_llm_client() -> OpenAI:
    return OpenAI(
        api_key=settings.deepseek_api_key,
        base_url=settings.deepseek_base_url,
    )


def chat(messages: list[dict], stream: bool = False):
    client = get_llm_client()
    response = client.chat.completions.create(
        model=settings.deepseek_model,
        messages=messages,
        stream=stream,
    )
    return response