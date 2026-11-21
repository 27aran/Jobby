from jobby.config import settings
from ollama import chat
import json
import requests

def generate(prompt: str) -> str:
    provider = settings.llm_provider
    if provider == "ollama":
        return _generate_with_ollama(prompt)
    elif provider == "openrouter":
        return _generate_with_openrouter(prompt)
    else:
        raise AttributeError(
            f"Unknown provider: {provider}\n Please choose either ollama or openrouter")

def _generate_with_ollama(prompt: str) -> str:
    model = settings.llm_model

    response = chat(
        model=model,
        messages=[{"role": 'user', "content": prompt}],
        think=False
    )
    return response.message.content

def _generate_with_openrouter(prompt: str) -> str:
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
        }),
        timeout=settings.llm_timeout,
    )
    response.raise_for_status()
    response = response.json()
    return response['choices'][0]['messages']['content']

tutor_chunk = """Erfahrung & Projekte
Tutor Datenstrukturen und Algorithmen April 2026 – vsl. Juli 2026
Universität Stuttgart Stuttgart
• Leitung wöchentlicher Übungsgruppen und Betreuung von Studierenden
• Korrektur von Übungsblättern und Vermittlung technischer Inhalte"""

porsche_chunk = """Erfahrung & Projekte
Praktikum Data Scientist Januar 2026 – April 2026
Porsche AG, Abteilung Qualität (EES4) Stuttgart
• Unterstützung in der Datenanalyse von Felddaten batterieelektrischer Fahrzeuge
• Mitarbeit in F&E-Projekten, insbesondere Predictive Maintenance und Batterielebensdauerprognose
• Einarbeitung in die Unsicherheitsquantifizierung im ML und Aufbau eines strukturierten Methodenbaukastens
• Implementierung und Anwendung konkreter Algorithmen, z. B. Kalibrierungsverfahren, Conformal Prediction und Bayessche Neuronale Netze (BNN)"""

def check(requirement: str, chunk: str) -> str:
    prompt = (
        "Antworte nur mit Ja oder Nein.\n"
        f"Belegt der folgende Lebenslauf-Abschnitt die Anforderung '{requirement}'?\n\n"
        f"Abschnitt:\n{chunk}"
    )
    return generate(prompt)

if __name__ == "__main__":
    print("SAP + Tutor:           ", check("Erfahrung mit SAP", tutor_chunk))
    print("Unsicherheit + Porsche:", check("Erfahrung mit Unsicherheitsquantifizierung", porsche_chunk))