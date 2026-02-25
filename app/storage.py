from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .models import ContentDraft, PublicationResult


class Storage:
    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS drafts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                topic TEXT NOT NULL,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                hashtags TEXT NOT NULL,
                sources TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS publications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                draft_id INTEGER NOT NULL,
                platform TEXT NOT NULL,
                ok INTEGER NOT NULL,
                message TEXT NOT NULL,
                FOREIGN KEY(draft_id) REFERENCES drafts(id)
            )
            """
        )
        self.conn.commit()

    def save_draft(self, draft: ContentDraft) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO drafts(created_at, topic, title, body, hashtags, sources)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                draft.created_at.isoformat(),
                draft.topic,
                draft.title,
                draft.body,
                json.dumps(draft.hashtags, ensure_ascii=False),
                json.dumps(draft.sources, ensure_ascii=False),
            ),
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def save_publication_result(self, draft_id: int, result: PublicationResult) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO publications(draft_id, platform, ok, message)
            VALUES (?, ?, ?, ?)
            """,
            (draft_id, result.platform, 1 if result.ok else 0, result.message),
        )
        self.conn.commit()
