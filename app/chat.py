#!/usr/bin/env python3
"""
chat.py — a tiny, dependency-free chat client for your local Ollama AI.

It uses ONLY the Python standard library, so on Windows it runs with a normal
Python install — no `pip install` needed.

Usage:
    py app\\chat.py                          # chat with the default model
    py app\\chat.py --model qwen2.5:7b       # chat with a different installed model
    py app\\chat.py --system "You are a terse coding tutor."

Inside the chat:
    /exit   quit        /clear  forget the conversation so far
    /help   show commands       Ctrl+C also quits

Environment variables:
    OLLAMA_HOST       Ollama server address (default http://localhost:11434)
    LOCAL_AI_MODEL    default model name (overridden by --model)
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_MODEL = "qwen2.5:3b"
DEFAULT_HOST = "http://localhost:11434"
BANNER = """\
============================================================
  Local AI chat — everything stays on this machine.
  Type your message and press Enter.
  Commands: /help   /clear   /exit
============================================================"""


def post_chat(host, model, messages):
    """POST to Ollama's /api/chat and yield streamed text chunks."""
    payload = json.dumps(
        {"model": model, "messages": messages, "stream": True}
    ).encode("utf-8")
    req = urllib.request.Request(
        host.rstrip("/") + "/api/chat",
        data=payload,
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
                    yield text
                if chunk.get("done"):
                    break
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise SystemExit(
                f"\n[!] Ollama doesn't have the model '{model}'.\n"
                f"    Open a terminal and run:  ollama pull {model}\n"
                f"    Or list installed models with:  ollama list"
            )
        detail = exc.read().decode("utf-8", errors="replace")[:300]
        raise SystemExit(f"\n[!] Ollama returned HTTP {exc.code}: {detail}")
    except urllib.error.URLError:
        raise SystemExit(
            "\n[!] Cannot reach Ollama at " + host + ".\n"
            "    Is Ollama installed and running?\n"
            "    - Install it from https://ollama.com/download\n"
            "    - Start it from the Windows Start menu (look for 'Ollama'),\n"
            "      then re-run this script."
        )


def main():
    parser = argparse.ArgumentParser(description="Chat with a local Ollama model")
    parser.add_argument(
        "--model",
        default=os.environ.get("LOCAL_AI_MODEL", DEFAULT_MODEL),
        help=f"installed Ollama model (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("OLLAMA_HOST", DEFAULT_HOST),
        help=f"Ollama server URL (default: {DEFAULT_HOST})",
    )
    parser.add_argument(
        "--system",
        default=None,
        help="optional system prompt that sets the AI's behaviour",
    )
    args = parser.parse_args()

    history = []
    if args.system:
        history.append({"role": "system", "content": args.system})

    print(BANNER)
    print(f"Model: {args.model}   |   Server: {args.host}\n")

    while True:
        try:
            user_text = input("you › ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye — your AI stays here whenever you need it.")
            break

        if not user_text:
            continue
        if user_text in ("/exit", "/quit"):
            print("Bye — your AI stays here whenever you need it.")
            break
        if user_text == "/help":
            print("  /exit   quit\n  /clear  start the conversation over\n")
            continue
        if user_text == "/clear":
            history = []
            if args.system:
                history.append({"role": "system", "content": args.system})
            print("  (conversation cleared)\n")
            continue

        history.append({"role": "user", "content": user_text})
        print("ai  › ", end="", flush=True)
        answer_parts = []
        try:
            for piece in post_chat(args.host, args.model, history):
                answer_parts.append(piece)
                print(piece, end="", flush=True)
        except KeyboardInterrupt:
            print("\n  (interrupted)")
            history.pop()  # don't keep an unanswered question
            print()
            continue
        print("\n")
        history.append({"role": "assistant", "content": "".join(answer_parts)})


if __name__ == "__main__":
    main()
