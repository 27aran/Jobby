from jobby.config import settings
from ollama import chat
import json
import requests

def generate(prompt: str) -> str:
    provider = settings.llm_provider

    if provider == "ollama":
        api_key = settings.ollama_api_key
        model = settings.llm_model

        response = chat(
            model=model,
            messages=[{"role": 'user', "content": prompt}],
            think=False
        )
        return response.message.content

    elif provider == "openrouter":
        api_key = settings.openrouter_api_key
        model = settings.llm_model

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "reasoning": {"enabled": False}
            })
        )
        response = response.json()
        response = response['choices'][0]['message']['content']
        return response
    else:
        raise AttributeError(
            f"Unknown provider: {provider}\n Please choose either ollama or openrouter")


