# FinContent AutoPilot

FinContent AutoPilot est un logiciel Python qui automatise :

1. la collecte d'actualités financières récentes,
2. la génération de contenus pédagogiques à forte valeur,
3. la planification éditoriale,
4. la publication (mode simulation ou webhook) sur des réseaux sociaux.

Le système est orienté vers les thèmes :
- gestion financière et comptable,
- contrôle de gestion,
- fiscalité des entreprises,
- audit.

## Fonctionnalités clés

- **Veille automatique** via flux RSS financiers configurables.
- **Génération d'un récit pratique** : contexte, impact terrain, actions recommandées, call-to-action.
- **Multiples plateformes** : LinkedIn, X/Twitter, Facebook (extensible).
- **Mode simulation (safe)** pour valider sans publier réellement.
- **Persistance SQLite** des contenus et logs de publication.
- **Planification hebdomadaire** avec rotation des thématiques.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Copier puis adapter :

```bash
cp config.example.json config.json
```

Points importants :
- `publishing.mode = "dry_run"` pour tester sans risque.
- `publishing.mode = "webhook"` pour envoyer le payload à un outil tiers (Zapier, Make, n8n, etc.).

## Exécution

### Générer et publier un contenu maintenant

```bash
python -m app.main run-once --config config.json
```

### Générer un calendrier sur 7 jours

```bash
python -m app.main plan-week --config config.json
```

## Exemple d'intégration publication réelle

En mode `webhook`, l'application envoie un JSON par plateforme vers l'URL définie dans `publishing.webhooks`.
Vous pouvez brancher cette URL sur votre outil d'automatisation pour publier via API officielles (LinkedIn, Meta, X API).

## Structure

- `app/models.py` : modèles de données.
- `app/financial_news.py` : extraction des actualités.
- `app/content_engine.py` : génération narrative orientée valeur.
- `app/social_publishers.py` : publication dry-run / webhook.
- `app/pipeline.py` : orchestration end-to-end.
- `app/storage.py` : base SQLite.
- `app/main.py` : CLI.

## Limites et bonnes pratiques

- Vérifiez manuellement les faits avant diffusion publique.
- Ajoutez une validation humaine sur les sujets sensibles (fiscalité/audit).
- Personnalisez le ton et la charte éditoriale pour votre audience.
