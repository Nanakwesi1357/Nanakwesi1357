# 02 — Choosing a model for a 12 GB Windows machine

You don't train a model — you **download open weights** (a finished,
freely-licensed model published by teams like Qwen/Alibaba, Meta and Mistral)
and Ollama runs them. Switching models is one command; you can keep several
installed and compare them.

## How to read the sizes

- A model's download size (below) is its disk footprint.
- At runtime it needs roughly that much RAM, plus room for Windows and your
  apps. On 12 GB, keep the running model at ~5 GB or below for comfort.
- `Q4` quantisation (the default for these tags) is the sweet spot: nearly
  full quality at a quarter of the original size.

## Recommended models, smallest to strongest

| Command to install | Disk | Feels like | Best for |
|---|---:|---|---|
| `ollama pull qwen2.5:3b` | ~1.9 GB | Fast, snappy | **Start here.** Daily chat, writing, summaries, coding questions |
| `ollama pull llama3.2:3b` | ~2.0 GB | Fast | Meta's alternative 3B; try both, pick the one you prefer |
| `ollama pull qwen2.5:7b` | ~4.7 GB | Thoughtful, still fine on 12 GB | **Best quality that fits comfortably.** Long answers, analysis, code |
| `ollama pull llama3.1:8b` | ~4.9 GB | Thoughtful | Strong all-rounder; close race with Qwen 7B |
| `ollama pull deepseek-r1:7b` | ~4.7 GB | Reasoning, "thinks out loud" | Maths, logic, hard problems — slower because it reasons step by step |

Avoid 14B+ models (9 GB and up) on this machine — they'll crawl or fail with
out-of-memory errors. Revisit them if you ever get a 32 GB machine.

## Rough speed expectations (CPU-only laptop)

- 3B models: often **15–30 words' worth of tokens per second** — answers feel
  instant.
- 7B/8B models: roughly **5–12 tokens/sec** — you'll watch it write, like a
  fast typist. Perfectly usable; just not instant.

## How to switch

Models stay installed; switching is free:

```powershell
ollama run qwen2.5:7b
```

Or with this project's client:

```powershell
py app\chat.py --model llama3.1:8b
```

Set a permanent default for the client with an environment variable:

```powershell
setx LOCAL_AI_MODEL "qwen2.5:7b"
```

(new terminal needed for it to take effect).

## Context window — how much it can remember at once

Models track a fixed amount of recent conversation ("context"). The default is
usually 4,096 tokens (~3,000 words). If you paste long documents and it starts
"forgetting" the start, raise it in a custom model — see
[03-customize-your-model.md](03-customize-your-model.md) (`PARAMETER num_ctx`).
Bigger context uses more memory, so increase gradually (8192, then 16384).

## What about vision, images, speech?

- Vision models (e.g. `llama3.2-vision`) can read screenshots and photos, but
  the usable ones are heavy; experiment once you're comfortable with the
  basics.
- Speech-to-text and text-to-speech are separate tools (e.g. Whisper); ask
  for them when you're ready — they slot alongside Ollama.

Next: [03-customize-your-model.md](03-customize-your-model.md)
