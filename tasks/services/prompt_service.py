import logging
from tasks.models import SystemPrompt as Prompt

# Logger definieren
logger = logging.getLogger(__name__)

def get_prompt(
        key: str,
        default_text: str = ""
) -> str:
    """
    Holt den Prompt aus der Datenbank anhand 'name'.
    Gibt 'default_text' zurück, falls keines gefunden.
    """
    logger.info(f"Retrieving Prompt with key {key} from Database.")
    try:
        p = Prompt.objects.get(name=key)
        return p.content
    except Prompt.DoesNotExist:
        logger.warning("Name not found, using default.")
        return default_text
