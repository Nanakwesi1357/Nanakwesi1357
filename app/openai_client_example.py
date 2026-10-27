#!/usr/bin/env python3
"""
openai_client_example.py — talk to your LOCAL model with the standard OpenAI
Python library. Ollama exposes an OpenAI-compatible API, so nearly every
tutorial or framework written for ChatGPT works offline by changing two lines.

Setup (one time):
    py -m pip install -r requirements.txt

Usage:
    py app\\openai_client_example.py "Explain recursion with a Ghanaian folk analogy."

Nothing here contacts OpenAI. The base URL points at your own machine and the
API key is a dummy string — Ollama doesn't check it.
"""

import sys

from openai import OpenAI

LOCAL_MODEL = "qwen2.5:3b"

client = OpenAI(
    base_url="http://localhost:11434/v1",  # your Ollama, not the cloud
    api_key="not-needed-for-local-ollama",
)


def main():
    question = " ".join(sys.argv[1:]) or "In one sentence, what can you do for me?"

    stream = client.chat.completions.create(
        model=LOCAL_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful, concise assistant."},
            {"role": "user", "content": question},
        ],
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
    print()


if __name__ == "__main__":
    main()
