from __future__ import annotations

from .base import ToolResult, resolve_workspace_path

MAX_READ_CHARS = 20_000


def read_file(path: str) -> ToolResult:
    try:
        target = resolve_workspace_path(path)
        text = target.read_text(encoding="utf-8")
        if len(text) > MAX_READ_CHARS:
            text = text[:MAX_READ_CHARS] + "\n\n[truncated]"
        return ToolResult(True, text)
    except Exception as exc:
        return ToolResult(False, str(exc))
