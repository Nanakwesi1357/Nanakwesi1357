# 01 — Windows setup, step by step

This guide assumes Windows 10/11 with 12 GB RAM. Every command below works in
**PowerShell**, **Command Prompt**, or **Windows Terminal** — they all accept
the same `ollama` commands.

---

## Step 1 — Install Ollama (the engine that runs models)

1. Open <https://ollama.com/download> in your browser.
2. Download **Ollama for Windows** and run the installer (`OllamaSetup.exe`).
3. Accept the defaults. Ollama installs:
   - a background app (you'll see a small llama icon in the system tray), and
   - the `ollama` command for terminals.
4. **Close any terminal windows that were already open**, then open a new one
   and verify:

   ```powershell
   ollama --version
   ```

   You should see a version number. If you get *"ollama is not recognized"*,
   see [04-troubleshooting.md](04-troubleshooting.md).

## Step 2 — Install Python (for the chat apps in this project)

1. Open <https://www.python.org/downloads/> and download the latest stable
   Python for Windows.
2. Run the installer. **On the first screen, tick "Add python.exe to PATH"**,
   then click *Install Now*.
3. Verify in a **new** terminal:

   ```powershell
   py --version
   ```

   You should see something like `Python 3.12.x`. (The chat client itself uses
   only Python's built-in libraries — no `pip install` is required for it.)

## Step 3 — Download your first model

The easiest route: double-click **`scripts\setup.bat`** in this folder. It
checks both installs above, downloads the starter model, and shows what you
have.

Or do it manually — this is the whole thing:

```powershell
ollama pull qwen2.5:3b
```

That downloads roughly **2 GB** once. If your connection drops, run the same
command again and it resumes instead of starting over.

## Step 4 — Say hello

Option A — Ollama's own built-in chat:

```powershell
ollama run qwen2.5:3b
```

Type questions at the `>>> Send a message` prompt. Type `/bye` to exit.

Option B — the chat client from this project:

```powershell
scripts\chat.bat
```

(or `py app\chat.py` from the project root). It streams answers, keeps
conversation history, and supports `/clear` and `/exit`.

**Now the privacy test:** turn on Airplane Mode / disconnect Wi-Fi, ask
another question. It still answers. Everything is on your machine.

## Step 5 — Add a graphical interface (optional but nice)

The terminal is fine, but a windowed app feels more like a product.

### Chatbox — lightest option (recommended on 12 GB)

1. Download Chatbox from <https://chatboxai.app> and install it.
2. Settings → Model Provider → choose **Ollama**.
3. API host: `http://localhost:11434` (the default). Model: `qwen2.5:3b`.
4. Save. Chatbox is now a polished desktop UI for your local model.

### Open WebUI — a full local "ChatGPT" in your browser

Double-click **`scripts\webui.bat`** (it installs via pip and launches the
server), then open <http://localhost:8080>. The first launch takes a minute
and downloads a few hundred MB of components. Create a local account on first
run — that account exists only on your laptop.

## Where your models live

By default everything is stored at:

```
C:\Users\<your-name>\.ollama\models
```

If your `C:` drive is small, move the collection to another drive:

1. Create e.g. `D:\ollama-models`.
2. Open Start → search "environment variables" → *Edit environment variables
   for your account* → **New**:
   - Variable name: `OLLAMA_MODELS`
   - Variable value: `D:\ollama-models`
3. Quit Ollama from the tray icon and start it again. Re-pull models; from now
   on they land on the other drive.

## Useful everyday commands

| Command | What it does |
|---|---|
| `ollama list` | Models installed on this machine |
| `ollama run qwen2.5:3b` | Start a chat with a model |
| `ollama pull qwen2.5:7b` | Download another model |
| `ollama ps` | Models currently loaded in memory |
| `ollama rm qwen2.5:3b` | Delete a model and reclaim its disk |
| `ollama update` | Update Ollama itself |

Next: [02-choosing-a-model.md](02-choosing-a-model.md)
