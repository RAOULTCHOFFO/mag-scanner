from __future__ import annotations

import argparse

from .config import load_config
from .pipeline import plan_week, run_once


def _cmd_run_once(config_path: str) -> int:
    config = load_config(config_path)
    draft, results = run_once(config)

    print("=== Contenu généré ===")
    print(draft.title)
    print()
    print(draft.body)
    print("\nHashtags:", " ".join(draft.hashtags))

    print("\n=== Résultats de publication ===")
    for result in results:
        status = "OK" if result.ok else "KO"
        print(f"- [{status}] {result.platform}: {result.message}")

    return 0


def _cmd_plan_week(config_path: str) -> int:
    config = load_config(config_path)
    drafts = plan_week(config)

    print("=== Planning éditorial 7 jours ===")
    for i, draft in enumerate(drafts, start=1):
        print(f"{i}. {draft.title}")
        print(f"   Angle: {draft.angle}")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Automatisation de contenus finance/compta")
    sub = parser.add_subparsers(dest="command", required=True)

    run_once_parser = sub.add_parser("run-once", help="Génère et publie un contenu")
    run_once_parser.add_argument("--config", default="config.json", help="Chemin du fichier config JSON")

    plan_parser = sub.add_parser("plan-week", help="Construit le planning de contenu sur 7 jours")
    plan_parser.add_argument("--config", default="config.json", help="Chemin du fichier config JSON")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run-once":
        return _cmd_run_once(args.config)
    if args.command == "plan-week":
        return _cmd_plan_week(args.config)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
