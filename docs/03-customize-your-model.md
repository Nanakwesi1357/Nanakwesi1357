# 03 — Make it YOUR model

Downloading Qwen or Llama gives you someone else's base model. A **Modelfile**
lets you wrap it with your own identity, rules and settings, then `ollama
create` builds a brand-new, privately-named model that exists only on your
laptop. This is the closest thing to "creating your own model" without
training one — and for most people it's exactly what they actually want.

An example is provided at [`app/Modelfile.my-assistant`](../app/Modelfile.my-assistant).

## The recipe, line by line

```
FROM qwen2.5:3b
```

The base model you're customising. It must already be installed
(`ollama pull qwen2.5:3b`).

```
SYSTEM """
You are My Assistant, a private AI that runs on the owner's laptop...
"""
```

The system prompt: instructions followed on **every** message. This is where
you define job, tone, boundaries and identity. Triple quotes let it span many
lines.

```
PARAMETER temperature 0.7
PARAMETER num_ctx 8192
```

Tuning knobs (full list below).

## Build and run it

From the project root:

```powershell
ollama create my-assistant -f app/Modelfile.my-assistant
ollama run my-assistant
```

Or with this project's client:

```powershell
py app\chat.py --model my-assistant
```

`ollama list` now shows `my-assistant` alongside the base models. It's yours —
no account, no registry, no one else can see or change it.

## Iterating

Edit the Modelfile, run the same `ollama create` command again (the name
overwrites), and test. This is a two-minute loop — experiment freely.

## Useful parameters

| Parameter | Range / example | Effect |
|---|---|---|
| `temperature` | 0.0 – 1.0 | Lower = focused, repeatable, factual; higher = varied, creative |
| `top_p` | 0.1 – 1.0 | Alternative creativity control; 0.9 is a safe default |
| `num_ctx` | 2048 – 32768 | Memory window in tokens; raise for long docs (costs RAM) |
| `repeat_penalty` | 1.0 – 1.3 | Penalises loops/repetition; 1.1 is typical |
| `stop` | e.g. `PARAMETER stop "###"` | Sequence that ends a generation |
| `num_predict` | e.g. 512 | Max tokens per answer |

## Three personas to steal

**Strict code reviewer**

```
SYSTEM """
You are a senior engineer. Review code for correctness, security and clarity.
Lead with the single most important issue, then minor points. No praise
sandwiches. Show corrected code in fenced blocks.
"""
PARAMETER temperature 0.2
```

**Writing partner**

```
SYSTEM """
You are an editor for a non-native English speaker. Keep the writer's own
voice and meaning; fix grammar and word choice; explain each change in one
short clause after the revised text.
"""
PARAMETER temperature 0.6
```

**Study tutor**

```
SYSTEM """
You are a patient tutor. Never just give the answer. Ask guiding questions,
then confirm understanding with a small exercise. Use West African everyday
analogies where helpful.
"""
PARAMETER temperature 0.4
```

Save any of these as `app/Modelfile.<name>`, then
`ollama create <name> -f app/Modelfile.<name>`.

## When a Modelfile isn't enough

A system prompt shapes *behaviour*, not *knowledge*. If you need the model to
know **your own documents** (contracts, notes, company info), that's a RAG
setup — covered next in [05-next-steps.md](05-next-steps.md). If you need it
to imitate a specific style from many examples, that's fine-tuning (LoRA),
also covered there, along with realistic hardware expectations.

Next: [04-troubleshooting.md](04-troubleshooting.md)
