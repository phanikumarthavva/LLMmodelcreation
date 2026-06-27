from functools import lru_cache

from transformers import pipeline

MODEL_NAME = "distilgpt2"


@lru_cache(maxsize=1)
def get_generator():
    return pipeline("text-generation", model=MODEL_NAME)


def generate_text(prompt: str, max_new_tokens: int = 50) -> str:
    generator = get_generator()
    result = generator(prompt, max_new_tokens=max_new_tokens, do_sample=True, top_p=0.9)
    return result[0]["generated_text"]
