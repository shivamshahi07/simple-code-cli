from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ToolResult:
    ok: bool
    output: str

    def as_text(self) -> str:
        status = "ok" if self.ok else "error"
        return f"[tool_result status={status}]\n{self.output}"


def workspace_root() -> Path:
    return Path.cwd().resolve()


def resolve_workspace_path(path: str) -> Path:
    root = workspace_root()
    target = (root / path).resolve()
    if root != target and root not in target.parents:
        raise ValueError(f"Path escapes workspace: {path}")
    return target
