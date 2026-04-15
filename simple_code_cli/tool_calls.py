from __future__ import annotations

import json
from typing import Any

TOOL_TYPES = {"list_files", "read_file", "edit_file", "web_search", "bash", "ripgrep"}


def parse_tool_call(text: str) -> tuple[str, dict[str, Any]] | None:
    stripped = text.strip()
    if not stripped.startswith("{"):
        return None
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    payload_type = payload.get("type")
    name = payload.get("name")
    if payload_type != "tool_call":
        if isinstance(payload_type, str) and payload_type in TOOL_TYPES:
            name = payload_type
        else:
            return None
    args = payload.get("args", {})
    if not isinstance(name, str) or not isinstance(args, dict):
        return None
    return name, args
