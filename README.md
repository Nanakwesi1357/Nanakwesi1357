# Your Own Local AI — Private Offline Assistant for Windows (12 GB RAM)

Stop *renting* intelligence from a few companies. This project helps you **own**
yours: a capable AI model that runs entirely on your own Windows laptop, works
offline, reads nothing you don't give it, and can never be switched off,
re-priced, or have its rules changed by someone else.

Everything here is **free and open source**. No API key, no account, no
subscription, no cloud.

---

## What you will have when done

- A real AI chatbot running on your own machine (Ollama + an open model)
- A friendly terminal chat app (`chat.py`, no programming needed to use it)
- Optional beautiful web interface (Chatbox or Open WebUI)
- Your own **custom-named model** with a personality/system rules you define
- The ability to call your AI from any script or app on `localhost:11434`

## Requirements

- Windows 10 or 11
- 12 GB RAM (your machine — the model choices below are tuned for this)
- ~5 GB free disk space for the starter model
- Internet only for the one-time download; afterwards it runs offline

## Quick start (about 30–45 minutes, mostly download time)

1. **Install Ollama** — download the Windows installer from
   <https://ollama.com/download> and run it.
2. **Double-click `scripts\setup.bat`** (or run it in a terminal). It checks
   everything and downloads your starter model (~2 GB).
3. **Double-click `scripts\chat.bat`** and start talking to your AI.
4. *(Optional)* Want a pretty window instead of a terminal? See
   [docs/01-windows-setup.md](docs/01-windows-setup.md) → "Add a graphical
   interface".

Prefer typing the commands yourself? The full walkthrough with screenshots-in-words
is in **[docs/01-windows-setup.md](docs/01-windows-setup.md)**.

## Project map

| Path | What it is |
|---|---|
| `docs/01-windows-setup.md` | Detailed step-by-step Windows installation guide |
| `docs/02-choosing-a-model.md` | Which models fit 12 GB RAM, with sizes and speeds |
| `docs/03-customize-your-model.md` | Make it *your* model: name, personality, rules |
| `docs/04-troubleshooting.md` | Fixes for every common problem |
| `docs/05-next-steps.md` | Chat with your documents, APIs, fine-tuning, phone access |
| `app/chat.py` | Zero-dependency terminal chat client (streaming answers) |
| `app/one_shot.py` | Ask one question from a script / command line |
| `app/openai_client_example.py` | Same local AI, using the standard OpenAI Python library |
| `app/Modelfile.my-assistant` | Example definition of your own custom model |
| `scripts/setup.bat` | One-click environment check + model download |
| `scripts/chat.bat` | One-click launch of the chat client |
| `scripts/webui.bat` | One-click install/launch of the Open WebUI interface |
| `tests/mock_ollama.py` | Mock server used to validate the client code offline |

## Why this is genuinely private

Ollama binds to `localhost` — your machine only. Prompts never leave the laptop;
you can verify it by turning on Airplane Mode mid-conversation (it keeps
answering). Model weights are open weights you keep forever in
`C:\Users\<you>\.ollama` — no licence that can "run out".

## The one-paragraph idea behind this project

> Right now almost everyone rents their intelligence from three or four
> companies. Whoever runs the model can raise the price, change the rules, read
> what you send it, or switch you off. A capable open model that runs on your
> own laptop costs nothing and takes an afternoon to set up. The real divide
> will be between the people who own one and the people who need permission.

Start here → **[docs/01-windows-setup.md](docs/01-windows-setup.md)**
