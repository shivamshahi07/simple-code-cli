from __future__ import annotations

from .base import ToolResult, resolve_workspace_path, workspace_root


def list_files(path: str = ".") -> ToolResult:
    try:
        target = resolve_workspace_path(path)
        if not target.exists():
            return ToolResult(False, f"No such path: {path}")
        if target.is_file():
            return ToolResult(True, str(target.relative_to(workspace_root())))
        entries = []
        for item in sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
            suffix = "/" if item.is_dir() else ""
            entries.append(f"{item.relative_to(workspace_root())}{suffix}")
        return ToolResult(True, "\n".join(entries) or "(empty)")
    except Exception as exc:
        return ToolResult(False, str(exc))
