# 05 — Next steps once your local AI is running

You now own a private, offline AI. Here's where people usually go next, roughly
in order of value-for-effort.

## 1. Chat with your own documents (RAG)

RAG ("retrieval-augmented generation") lets the model quote from *your* PDFs,
notes, contracts or code without retraining anything.

- **Easiest:** Open WebUI (see `scripts\webui.bat`) has document upload built
  in — drag a file into a chat and enable the document/collection toggle.
- **In code:** libraries like **LlamaIndex** or **LangChain** handle chunking,
  local embeddings (e.g. `nomic-embed-text` via `ollama pull
  nomic-embed-text`) and retrieval, then send context to your local model over
  the same `localhost:11434` API. Nothing leaves the machine.

## 2. Call your AI from other software

Ollama exposes two local APIs:

- Native: `POST http://localhost:11434/api/chat`
- OpenAI-compatible: `POST http://localhost:11434/v1/chat/completions`

The second one means almost any tool, library or tutorial written for OpenAI
works locally — just change the base URL and use a dummy key. A ready example
is [`app/openai_client_example.py`](../app/openai_client_example.py). Plain
PowerShell works too:

```powershell
$body = @{
  model = "qwen2.5:3b"
  messages = @(@{ role = "user"; content = "Draft a polite late-invoice reminder." })
  stream = $false
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:11434/api/chat -Method Post -Body $body `
  | Select-Object -ExpandProperty message | Select-Object -ExpandProperty content
```

## 3. Automate everyday tasks

`app/one_shot.py` is built for this — call it from scripts, scheduled tasks,
file watchers:

```powershell
type meeting.txt | py app\one_shot.py "Turn these notes into 5 bullet action items."
py app\one_shot.py "Generate 5 commit-message subjects for this diff" > ideas.txt
```

Windows Task Scheduler can run these on a schedule; the model is local so no
API costs or rate limits apply.

## 4. Fine-tuning — changing what the model *knows*, not just how it behaves

A Modelfile shapes behaviour. **Fine-tuning** (usually LoRA) actually trains
the weights on your examples — useful for a distinctive writing voice or
narrow specialised output.

Reality check:
- Meaningful fine-tuning wants an NVIDIA GPU with 8–16 GB VRAM. Most 12 GB RAM
  Windows laptops without a gaming GPU aren't there.
- The standard beginner route is **Unsloth** (`unsloth.ai`) with a free
  cloud GPU (Google Colab/Kaggle), fine-tuning a 3B/7B base on a few hundred
  high-quality examples, then importing the result into Ollama via a GGUF
  conversion (`ollama create` accepts a GGUF `FROM`).
- Try RAG + a strong system prompt first — they solve ~90% of "I need it to
  know my stuff" requests at zero training cost.

## 5. Reach it from your phone or other devices (same Wi-Fi)

1. Tell Ollama to listen beyond localhost: set user environment variable
   `OLLAMA_HOST=0.0.0.0:11434`, then quit and restart Ollama from the tray.
2. Allow port 11434 through **Windows Defender Firewall** when prompted.
3. Find the laptop's LAN IP (`ipconfig`, e.g. `192.168.1.22`).
4. Point a phone client (e.g. the Chatbox mobile app) at
   `http://192.168.1.22:11434`.

**Only do this on a trusted home network.** Never forward the port to the
internet without authentication — an open Ollama port lets anyone on the
network use your machine.

## 6. Keeping it maintained

- `ollama update` every few weeks; re-pull models occasionally to pick up
  improved builds.
- Watch disk usage with `ollama list`; delete experiments with
  `ollama rm <name>`.
- Browse new models at <https://ollama.com/search> — the open-model ecosystem
  moves fast, and trying one is just a `pull` away.

## Where to learn more

- Ollama docs: <https://github.com/ollama/ollama> (README) and
  <https://docs.ollama.com>
- Modelfile reference: <https://docs.ollama.com/modelfile>
- Models: <https://ollama.com/library>
- RAG frameworks: <https://docs.llamaindex.ai>, <https://python.langchain.com>
- Fine-tuning: <https://docs.unsloth.ai>
