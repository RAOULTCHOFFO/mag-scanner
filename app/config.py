from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class AppConfig:
    rss_feeds: List[str]
    target_platforms: List[str]
    publishing_mode: str
    webhooks: Dict[str, str]
    database_path: str
    language: str


DEFAULT_FEEDS = [
    "https://www.imf.org/en/News/RSS",
    "https://www.ecb.europa.eu/rss/press.html",
    "https://www.oecd.org/finance/index.xml",
]


def load_config(path: str) -> AppConfig:
    config_path = Path(path)
    payload: Dict[str, Any] = {}

    if config_path.exists():
        payload = json.loads(config_path.read_text(encoding="utf-8"))

    publishing = payload.get("publishing", {})

    return AppConfig(
        rss_feeds=payload.get("rss_feeds", DEFAULT_FEEDS),
        target_platforms=payload.get("target_platforms", ["linkedin", "x", "facebook"]),
        publishing_mode=publishing.get("mode", "dry_run"),
        webhooks=publishing.get("webhooks", {}),
        database_path=payload.get("database_path", "fincontent.db"),
        language=payload.get("language", "fr"),
    )
