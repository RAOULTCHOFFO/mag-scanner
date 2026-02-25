from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class NewsItem:
    title: str
    summary: str
    link: str
    source: str
    published_at: datetime


@dataclass
class ContentDraft:
    topic: str
    angle: str
    title: str
    body: str
    hashtags: List[str]
    sources: List[str]
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PublicationResult:
    platform: str
    ok: bool
    message: str
    external_id: str | None = None
