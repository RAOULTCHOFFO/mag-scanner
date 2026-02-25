from datetime import datetime, timezone
import unittest

from app.content_engine import build_practical_story
from app.models import NewsItem


class ContentEngineTests(unittest.TestCase):
    def test_build_practical_story_contains_action_plan(self):
        news = [
            NewsItem(
                title="Banque centrale: maintien des taux",
                summary="Les analystes anticipent un impact sur le coût du financement des PME.",
                link="https://example.com/news/1",
                source="https://example.com/rss",
                published_at=datetime.now(timezone.utc),
            )
        ]

        draft = build_practical_story("contrôle de gestion", news)

        self.assertIn("Plan d'action", draft.body)
        self.assertTrue(draft.sources)
        self.assertIn("#Finance", draft.hashtags)


if __name__ == "__main__":
    unittest.main()
