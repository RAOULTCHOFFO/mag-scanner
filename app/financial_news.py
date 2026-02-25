from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import List
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from .models import NewsItem


def _read_text(parent: ET.Element, tag_name: str) -> str:
    node = parent.find(tag_name)
    return (node.text or "").strip() if node is not None else ""


def _parse_pub_date(raw: str) -> datetime:
    if not raw:
        return datetime.now(timezone.utc)
    try:
        return parsedate_to_datetime(raw)
    except Exception:
        return datetime.now(timezone.utc)


def fetch_financial_news(rss_urls: List[str], max_items: int = 12) -> List[NewsItem]:
    collected: List[NewsItem] = []

    for url in rss_urls:
        try:
            with urlopen(url, timeout=8) as response:
                body = response.read()
            root = ET.fromstring(body)
        except Exception:
            continue

        for item in root.findall(".//item"):
            title = _read_text(item, "title")
            summary = _read_text(item, "description")
            link = _read_text(item, "link")
            pub_date = _parse_pub_date(_read_text(item, "pubDate"))
            if title:
                collected.append(
                    NewsItem(
                        title=title,
                        summary=summary,
                        link=link,
                        source=url,
                        published_at=pub_date,
                    )
                )

    collected.sort(key=lambda n: n.published_at, reverse=True)
    return collected[:max_items]
