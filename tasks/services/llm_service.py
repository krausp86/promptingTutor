import json
import logging
from openai import OpenAI
from tasks.models import Configuration as Config
from .prompt_service import get_prompt

# Logger definieren
logger = logging.getLogger(__name__)

# --- OpenAI Client initialisieren
def init_openai_api():
    """
    Liest den OpenAI-API-Key aus der Configuration.
    """
    logger.info("Getting OpenAI API Key")
    api_key = Config.get_value("OPENAI_API_KEY", default=None)
    if not api_key:
        logger.error("No OpenAI API Key found in Configuration!")
        raise ValueError("Kein OPENAI_API_KEY in der Configuration gefunden!")
    client = OpenAI(api_key=api_key)
    return client

# --- Eingabe prüfen (Guidelines + Aufgabenbezug)
def evaluate_prompt(user_input: str, task_text: str) -> (bool, str):
    """
    Prüft, ob der User-Input ein guter Prompt ist und die Aufgabenstellung adressiert.
    Gibt zurück: (ok: bool, feedback: str)
    """
    client = init_openai_api()

    # Guidelines laden
    guidelines = get_prompt(
        key="Prompting_Guidelines",
        default_text="Ein guter Prompt ist klar, vollständig und zielgerichtet."
    )

    system_prompt = "Du bist ein Experte für Prompt-Engineering. Beurteile Prompts streng nach den Kriterien."

    user_prompt = f"""
Prüfe folgenden Benutzer-Input auf zwei Kriterien:

1) Entspricht der Prompt den Guidelines? (Guidelines: {guidelines})
2) Bezieht sich der Prompt ausreichend auf die folgende Aufgabenstellung: "{task_text}"

Antwortformat:

{{
  "guidelines_ok": true/false,
  "task_relevance_ok": true/false,
  "feedback": "Hinweise, was besser gemacht werden könnte."
}}

Benutzer-Input:
{user_input}
"""

    logger.info("Calling OpenAI to evaluate prompt")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0
    )

    raw_content = response.choices[0].message.content.strip()

    try:
        data = json.loads(raw_content)
        ok = data.get("guidelines_ok", False) and data.get("task_relevance_ok", False)
        feedback = data.get("feedback", "Kein Feedback erhalten.")
        return ok, feedback
    except Exception as e:
        logger.error(f"Error parsing LLM response: {e}")
        return False, "Antwort konnte nicht ausgewertet werden. Bitte versuche es erneut."

