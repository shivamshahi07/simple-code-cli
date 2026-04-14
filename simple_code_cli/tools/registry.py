from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .base import ToolResult
from .bash import bash
from .edit_file import edit_file
from .list_files import list_files
from .read_file import read_file
from .ripgrep import ripgrep
from .web_search import web_search

Tool = Callable[..., ToolResult]

TOOL_NAMES: dict[str, Tool] = {
    "list_files": list_files,
    "read_file": read_file,
    "edit_file": edit_file,
    "web_search": web_search,
    "bash": bash,
    "ripgrep": ripgrep,
}


def run_tool(name: str, args: dict[str, Any]) -> ToolResult:
    tool = TOOL_NAMES.get(name)
    if tool is None:
        return ToolResult(False, f"Unknown tool: {name}")
    try:
        return tool(**args)
    except TypeError as exc:
        return ToolResult(False, f"Invalid arguments for {name}: {exc}")
