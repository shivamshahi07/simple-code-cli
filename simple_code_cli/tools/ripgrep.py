from __future__ import annotations

import subprocess

from .base import ToolResult, resolve_workspace_path, workspace_root


def ripgrep(pattern: str, path: str = ".") -> ToolResult:
    try:
        target = resolve_workspace_path(path)
        completed = subprocess.run(
            ["rg", "--line-number", "--color", "never", pattern, str(target)],
            cwd=workspace_root(),
            text=True,
            capture_output=True,
            timeout=30,
        )
        output = completed.stdout
        if completed.stderr:
            output += f"\n[stderr]\n{completed.stderr}"
        ok = completed.returncode in (0, 1)
        return ToolResult(ok, output.strip() or "(no matches)")
    except FileNotFoundError:
        return ToolResult(False, "ripgrep is not installed. Install `rg` and try again.")
    except Exception as exc:
        return ToolResult(False, str(exc))
