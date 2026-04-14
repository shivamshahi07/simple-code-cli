from __future__ import annotations

import subprocess

from .base import ToolResult, workspace_root


def bash(command: str, timeout: int = 30) -> ToolResult:
    try:
        completed = subprocess.run(
            command,
            cwd=workspace_root(),
            shell=True,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
        output = completed.stdout
        if completed.stderr:
            output += f"\n[stderr]\n{completed.stderr}"
        return ToolResult(completed.returncode == 0, output.strip() or "(no output)")
    except Exception as exc:
        return ToolResult(False, str(exc))
