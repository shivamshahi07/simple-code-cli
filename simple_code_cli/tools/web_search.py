from __future__ import annotations

import os

import httpx

from .base import ToolResult


def web_search(query: str, api_key: str | None = None, max_results: int = 5) -> ToolResult:
    key = api_key or os.getenv("TAVILY_API_KEY")
    if not key:
        return ToolResult(False, "Missing Tavily API key. Set TAVILY_API_KEY or pass api_key.")
    try:
        response = httpx.post(
            "https://api.tavily.com/search",
            headers={"Authorization": f"Bearer {key}"},
            json={"query": query, "max_results": max_results},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        lines = []
        for item in results:
            title = item.get("title", "Untitled")
            url = item.get("url", "")
            content = item.get("content", "")
            lines.append(f"- {title}\n  {url}\n  {content}")
        return ToolResult(True, "\n\n".join(lines) or "(no results)")
    except Exception as exc:
        return ToolResult(False, str(exc))
