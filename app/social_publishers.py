from __future__ import annotations

import json
from urllib.request import Request, urlopen

from .models import ContentDraft, PublicationResult


class Publisher:
    def publish(self, platform: str, draft: ContentDraft) -> PublicationResult:
        raise NotImplementedError


class DryRunPublisher(Publisher):
    def publish(self, platform: str, draft: ContentDraft) -> PublicationResult:
        return PublicationResult(
            platform=platform,
            ok=True,
            message=f"[dry_run] Publication simulée sur {platform}: {draft.title}",
        )


class WebhookPublisher(Publisher):
    def __init__(self, webhooks: dict[str, str]):
        self.webhooks = webhooks

    def publish(self, platform: str, draft: ContentDraft) -> PublicationResult:
        url = self.webhooks.get(platform)
        if not url:
            return PublicationResult(platform=platform, ok=False, message="Webhook non configuré")

        payload = {
            "platform": platform,
            "title": draft.title,
            "body": draft.body,
            "hashtags": draft.hashtags,
            "sources": draft.sources,
            "topic": draft.topic,
            "angle": draft.angle,
        }
        data = json.dumps(payload).encode("utf-8")

        try:
            request = Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
            with urlopen(request, timeout=8) as resp:
                status = resp.status
            return PublicationResult(
                platform=platform,
                ok=200 <= status < 300,
                message=f"Webhook status={status}",
            )
        except Exception as exc:
            return PublicationResult(platform=platform, ok=False, message=f"Erreur webhook: {exc}")
