from __future__ import annotations

from datetime import datetime
from typing import List

from .models import ContentDraft, NewsItem

TOPIC_ANGLES = {
    "gestion financière et comptable": "transformer l'actualité en décisions budgétaires concrètes",
    "contrôle de gestion": "relier les signaux macro aux KPIs opérationnels",
    "fiscalité des entreprises": "anticiper les impacts fiscaux et sécuriser la conformité",
    "audit": "renforcer les contrôles internes face aux nouveaux risques",
}


def choose_topic(day_index: int) -> str:
    topics = list(TOPIC_ANGLES.keys())
    return topics[day_index % len(topics)]


def _extract_key_points(news: List[NewsItem], limit: int = 3) -> List[NewsItem]:
    return news[:limit]


def build_practical_story(topic: str, news: List[NewsItem]) -> ContentDraft:
    selected = _extract_key_points(news)
    angle = TOPIC_ANGLES.get(topic, "traduire l'information financière en actions métier")

    if selected:
        headline = selected[0].title
    else:
        headline = "Tendance financière du moment"

    opening = (
        f"📊 {topic.title()} — ce que l'actualité change dès maintenant\n\n"
        f"L'information dominante de la semaine : {headline}."
    )

    insights = []
    sources = []
    for idx, item in enumerate(selected, start=1):
        insights.append(
            f"{idx}) {item.title}\n"
            f"Impact pratique : {item.summary[:220] or 'analyser l’effet sur votre planification et votre trésorerie.'}"
        )
        if item.link:
            sources.append(item.link)

    insights_block = "\n\n".join(insights) if insights else "Aucune actualité récupérée, appliquez une revue mensuelle de risques et opportunités."

    body = (
        f"{opening}\n\n"
        f"🎯 Angle retenu : {angle}.\n\n"
        f"Voici les implications concrètes pour une équipe finance/compta :\n"
        f"{insights_block}\n\n"
        "✅ Plan d'action (48h) :\n"
        "- Revoir vos hypothèses de budget et de cash-flow.\n"
        "- Mettre à jour 2 indicateurs de pilotage (marge, BFR, taux de conformité).\n"
        "- Préparer une note courte pour la direction avec risques + décisions recommandées.\n\n"
        "💬 Question à votre communauté : quelle décision finance avez-vous accélérée cette semaine grâce à l'actualité ?"
    )

    hashtags = ["#Finance", "#Comptabilité", "#ContrôleDeGestion", "#Fiscalité", "#Audit"]

    return ContentDraft(
        topic=topic,
        angle=angle,
        title=f"{topic.title()} : exploiter l'actualité financière pour créer de la valeur ({datetime.utcnow().date()})",
        body=body,
        hashtags=hashtags,
        sources=sources,
    )
