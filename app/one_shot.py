#!/usr/bin/env python3
"""
one_shot.py — ask your local AI a single question and print the answer.

Handy for scripts, automation, notebooks, or piping text around.
Standard library only — no pip install required.

Usage:
    py app\\one_shot.py "Summarise what DNS is in two sentences."
    py app\\one_shot.py --model qwen2.5:7b "Write a birthday message for Ama."
    type notes.txt | py app\\one_shot.py "Summarise this text."
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_MODEL = "qwen2.5:3b"
DEFAULT_HOST = "http://localhost:11434"


def ask(host, model, prompt, system=None):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    req = urllib.request.Request(
        host.rstrip("/") + "/api/chat",
        data=json.dumps(
            {"model": model, "messages": messages, "stream": True}
        ).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            for raw_line in resp:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line:
                    continue
                chunk = json.loads(line)
                text = chunk.get("message", {}).get("content", "")
                if text:
                    print(text, end="", flush=True)
                if chunk.get("done"):
                    break
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            print(
                f"[!] Model '{model}' isn't installed. Run: ollama pull {model}",
                file=sys.stderr,
            )
        else:
            print(f"[!] HTTP {exc.code} from Ollama", file=sys.stderr)
        return 1
    except urllib.error.URLError:
        print(
            "[!] Cannot reach Ollama. Is it installed and running? "
            "See https://ollama.com/download",
            file=sys.stderr,
        )
        return 1
    print()
    return 0


def main():
    parser = argparse.ArgumentParser(description="One question to a local Ollama model")
    parser.add_argument("prompt", nargs="?", help="your question (or pipe text via stdin)")
    parser.add_argument("--model", default=os.environ.get("LOCAL_AI_MODEL", DEFAULT_MODEL))
    parser.add_argument("--host", default=os.environ.get("OLLAMA_HOST", DEFAULT_HOST))
    parser.add_argument("--system", default=None)
    args = parser.parse_args()

    prompt = args.prompt
    if prompt is None:
        if sys.stdin.isatty():
            parser.error("give a prompt as an argument, or pipe text into stdin")
        stdin_text = sys.stdin.read().strip()
        if not stdin_text:
            parser.error("stdin was empty")
        prompt = stdin_text

    return ask(args.host, args.model, prompt, args.system)


if __name__ == "__main__":
    sys.exit(main())
