import tiktoken
from ..services.get_summary import MODEL

def truncate_text_to_token_limit(text, max_tokens=6000):
    # Use the GPT-compatible tokenizer
    encoding = tiktoken.get_encoding("cl100k_base")
    
    tokens = encoding.encode(text)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]

    return encoding.decode(tokens)
