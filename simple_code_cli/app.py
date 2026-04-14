from __future__ import annotations

import os
from pathlib import Path

import typer
from google import genai
from google.genai import types
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from .config import get_settings
from .prompts import SYSTEM_PROMPT
from .tool_calls import parse_tool_call
from .tools import run_tool
# TODO: add a unified API provider layer such as OpenRouter.
app = typer.Typer(help="A tiny Claude Code-inspired terminal coding agent.")
console = Console()
SETTINGS = get_settings()


def _client(project: str | None, location: str, model: str) -> tuple[genai.Client, str]:
    if SETTINGS.credentials:
        os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", SETTINGS.credentials)
    resolved_project = project or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not resolved_project:
        raise typer.BadParameter("Set --project or GOOGLE_CLOUD_PROJECT in .env.")
    client = genai.Client(vertexai=True, project=resolved_project, location=location)
    return client, model


def _ask(client: genai.Client, model: str, messages: list[str]) -> str:
    response = client.models.generate_content(
        model=model,
        contents="\n\n".join(messages),
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    return response.text or ""


@app.command()
def chat(
    project: str | None = typer.Option(SETTINGS.project, "--project", "-p", help="Google Cloud project ID."),
    location: str = typer.Option(
        SETTINGS.location or "us-central1",
        "--location",
        "-l",
        help="Vertex AI location.",
    ),
    model: str = typer.Option(SETTINGS.model or "gemini-2.5-flash", "--model", "-m", help="Vertex AI model name."),
) -> None:
    """Start the interactive agent."""
    client, model_name = _client(project, location, model)
    console.print(
        Panel.fit(
            "[bold cyan]Simple Code[/bold cyan]\n"
            "[green]Vertex AI[/green] powered mini coding CLI\n"
            "Type [bold]exit[/bold] to quit.",
            border_style="cyan",
        )
    )
    messages: list[str] = []
    while True:
        user_text = Prompt.ask("[bold magenta]you[/bold magenta]")
        if user_text.strip().lower() in {"exit", "quit"}:
            console.print("[cyan]bye[/cyan]")
            return
        messages.append(f"User: {user_text}")

        for _ in range(8):
            answer = _ask(client, model_name, messages)
            tool_call = parse_tool_call(answer)
            if tool_call is None:
                messages.append(f"Assistant: {answer}")
                console.print(Panel(Markdown(answer), border_style="green", title="assistant"))
                break

            name, args = tool_call
            console.print(Panel(str(args), title=f"tool: {name}", border_style="yellow"))
            result = run_tool(name, args)
            messages.append(f"Assistant requested tool: {name} {args}")
            messages.append(result.as_text())
            console.print(Panel(result.output, title="result", border_style="blue" if result.ok else "red"))
        else:
            console.print("[red]Stopped after too many tool calls.[/red]")


@app.command()
def init_env() -> None:
    """Print the environment variables this CLI understands."""
    env_path = Path(".env.example")
    env_path.write_text(
        "GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/service-account.json\n"
        "GOOGLE_CLOUD_PROJECT=your-google-cloud-project-id\n"
        "GOOGLE_CLOUD_LOCATION=us-central1\n"
        "GOOGLE_VERTEX_MODEL=gemini-2.5-flash\n"
        "TAVILY_API_KEY=tvly-your-key\n",
        encoding="utf-8",
    )
    console.print(f"[green]Wrote[/green] {env_path}")


if __name__ == "__main__":
    app()
