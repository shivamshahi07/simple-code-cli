from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def load_env() -> None:
    package_root = Path(__file__).resolve().parent.parent
    _load_env_file(package_root / ".env")
    _load_env_file(Path.cwd() / ".env")


@dataclass(frozen=True)
class Settings:
    project: str | None
    location: str | None
    credentials: str | None
    model: str | None


def get_settings() -> Settings:
    load_env()
    return Settings(
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
        credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        model=os.getenv("GOOGLE_VERTEX_MODEL"),
    )
