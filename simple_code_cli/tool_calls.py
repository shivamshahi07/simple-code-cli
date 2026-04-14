from __future__ import annotations

import json
from typing import Any


def parse_tool_call(text: str) -> tuple[str, dict[str, Any]] | None:
    stripped = text.strip()
    if not stripped.startswith("{"):
        return None
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    if payload.get("type") != "tool_call":
        return None
    name = payload.get("name")
    args = payload.get("args", {})
    if not isinstance(name, str) or not isinstance(args, dict):
        return None
    return name, args
