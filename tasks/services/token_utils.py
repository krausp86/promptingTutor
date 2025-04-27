import logging
import tiktoken

# Logger definieren
logger = logging.getLogger(__name__)

def count_tokens(text: str, model_name: str = "gpt-3.5-turbo") -> int:
    if not text.strip():
        return 0
    tokenizer = tiktoken.encoding_for_model(model_name)
    return len(tokenizer.encode(text))
