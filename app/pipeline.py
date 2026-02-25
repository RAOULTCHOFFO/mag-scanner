from __future__ import annotations

from datetime import date, timedelta
from typing import List

from .config import AppConfig
from .content_engine import build_practical_story, choose_topic
from .financial_news import fetch_financial_news
from .models import ContentDraft, PublicationResult
from .social_publishers import DryRunPublisher, Publisher, WebhookPublisher
from .storage import Storage


def _build_publisher(config: AppConfig) -> Publisher:
    if config.publishing_mode == "webhook":
        return WebhookPublisher(config.webhooks)
    return DryRunPublisher()


def run_once(config: AppConfig) -> tuple[ContentDraft, List[PublicationResult]]:
    news = fetch_financial_news(config.rss_feeds)
    topic = choose_topic(date.today().toordinal())
    draft = build_practical_story(topic=topic, news=news)

    storage = Storage(config.database_path)
    draft_id = storage.save_draft(draft)

    publisher = _build_publisher(config)
    results: List[PublicationResult] = []
    for platform in config.target_platforms:
        result = publisher.publish(platform, draft)
        storage.save_publication_result(draft_id, result)
        results.append(result)

    return draft, results


def plan_week(config: AppConfig) -> List[ContentDraft]:
    news = fetch_financial_news(config.rss_feeds)
    drafts: List[ContentDraft] = []
    for i in range(7):
        day = date.today() + timedelta(days=i)
        topic = choose_topic(day.toordinal())
        drafts.append(build_practical_story(topic=topic, news=news))
    return drafts
