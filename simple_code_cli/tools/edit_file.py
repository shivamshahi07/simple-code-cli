from __future__ import annotations

from .base import ToolResult, resolve_workspace_path, workspace_root


def edit_file(path: str, content: str) -> ToolResult:
    try:
        target = resolve_workspace_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return ToolResult(True, f"Wrote {target.relative_to(workspace_root())}")
    except Exception as exc:
        return ToolResult(False, str(exc))
