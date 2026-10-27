# 04 — Troubleshooting

## "'ollama' is not recognized as an internal or external command"

The installer adds Ollama to your PATH, but already-open terminals don't notice.
**Close the terminal completely, open a new one, try again.** If it persists,
re-run the installer from <https://ollama.com/download> and check the Ollama
icon is in the system tray (bottom-right, near the clock).

## "Cannot reach Ollama" / chat.py can't connect

1. Is Ollama running? Look for the llama icon in the system tray. Missing?
   Start Ollama from the Start menu.
2. Check the engine answers: open <http://localhost:11434> in a browser. You
   should see `Ollama is running`.
3. If you changed the port or host, point the client at it:
   `py app\chat.py --host http://localhost:11434`
   (or set the `OLLAMA_HOST` environment variable).

## Model pull fails or keeps stalling

Re-run the **same** `ollama pull ...` command — downloads resume, they don't
restart. On a metered/slow connection prefer the 3B model (~1.9 GB) over the
7B (~4.7 GB).

## "model not found" / HTTP 404 from the client

The model name isn't installed. `ollama list` shows what you have; install the
missing one with `ollama pull <name>`. Note names include the tag (e.g.
`qwen2.5:3b`, not just `qwen2.5`).

## Answers are slow

- Use a 3B model (`qwen2.5:3b`) — on a CPU laptop it's often 3–5× faster than
  7B.
- Close big apps (browsers with many tabs, games) to free RAM.
- Unload idle models: `ollama stop <name>` (or check `ollama ps`).
- Smaller context uses less memory: lower `num_ctx` in your Modelfile.
- First prompt after starting is always slowest (model loads from disk into
  RAM); the next ones are faster.

## Out-of-memory errors / the laptop freezes

You're over the 12 GB budget. Switch to a smaller model, and avoid 14B+
models entirely. A reboot clears a stuck model from RAM, then `ollama run` a
3B model.

## Python: "'py' is not recognized"

Python isn't installed or PATH wasn't ticked. Re-run the installer from
<https://www.python.org/downloads/> and **tick "Add python.exe to PATH"** on
the first screen, then open a new terminal.

## `openai` import error in the optional example

`app/openai_client_example.py` is the only script needing a library:

```powershell
py -m pip install -r requirements.txt
```

The main `chat.py` and `one_shot.py` never need this.

## Open WebUI won't start or install

- Use Python 3.11 or 3.12 (very new Python versions sometimes lag behind
  Open WebUI's dependencies).
- Try the module form directly: `py -m open_webui serve`.
- Port 8080 already in use? Close whatever uses it, or simply use Chatbox
  instead (see [01-windows-setup.md](01-windows-setup.md)) — it needs none of
  this.

## Want to wipe everything and start over

1. Quit Ollama from the tray.
2. Delete the folder `C:\Users\<you>\.ollama` (this removes all downloaded
   models — re-pull afterwards).
3. Optionally uninstall Ollama from *Settings → Apps*.

## Something else

Collect the exact error text and the output of `ollama --version` and
`ollama list` — those three things diagnose nearly every problem. Also worth
browsing: <https://github.com/ollama/ollama/issues>.
