# Simple Code CLI

A very small Claude Code-style terminal coding agent written in Python. It uses
Google Vertex AI for the model and has a few basic tools:

- edit file
- list files
- read file
- web search through Tavily
- bash
- ripgrep

It is intentionally simple. The model asks for tool calls as JSON, the CLI runs
the tool, and then the result is sent back to the model.

## Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

## Google Vertex AI Auth

Configuration lives in `.env`. Copy `.env.example` and fill in your local
values:

```bash
cp .env.example .env
```

Vertex AI auth needs:

1. A Google Cloud project ID with billing enabled.
2. The Vertex AI API enabled in that project.
3. A principal with permissions to call Vertex AI models.
4. Application Default Credentials, either from local user login or a service
   account key.

The API usage is billed to the Google Cloud project passed with `--project` or
`GOOGLE_CLOUD_PROJECT`. The service account is the identity authorized to call
Vertex AI, and the quota/spend are attached to the selected project.

## Tavily Search

Set a Tavily API key when you want web search:

```bash
TAVILY_API_KEY=tvly-your-key
```

The Tavily usage is billed to the Tavily account for that API key.

## Run

```bash
simple-code chat
```

Try:

```text
list the files
read README.md
create hello.py that prints hello
run python hello.py
```

## TODO

- Add a unified provider layer for OpenRouter or similar providers.
- Replace JSON text tool calls with native model function calling.
- Add confirmation prompts before bash and file edits.
- Add patch-based editing instead of full-file overwrite.
