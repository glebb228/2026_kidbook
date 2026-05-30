#!/usr/bin/env python3

import argparse
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CONCEPTS_PATH = ROOT / "WORK/5.1_technology_and_digital_literacy/artificial_intelligence_simple/concepts.json"
PROTECTED = re.compile(
    r"```[\s\S]*?```"
    r"|`[^`\n]+`"
    r"|!\[[^\]]*\]\([^)]*\)"
    r"|\[[^\]]*\]\([^)]*\)"
    r"|^#+[^\n]*$",
    re.MULTILINE,
)


def relative_link(source: Path, target: Path) -> str:
    return os.path.relpath(target, source.parent).replace("\\", "/")


def linkify(text: str, source: Path, concepts: list[dict]) -> tuple[str, int]:
    inserted = 0
    targets: list[tuple[Path, list[str]]] = []
    for concept in concepts:
        target = ROOT / concept["file"]
        link = relative_link(source, target)
        if target != source and f"]({link})" not in text:
            targets.append((target, concept["lemmas"]))

    chunks: list[str] = []
    last = 0
    for protected in PROTECTED.finditer(text):
        chunks.append(text[last:protected.start()])
        chunks.append(protected.group(0))
        last = protected.end()
    chunks.append(text[last:])

    linked: set[Path] = set()
    for index in range(0, len(chunks), 2):
        updated = chunks[index]
        for target, lemmas in targets:
            if target in linked:
                continue
            for lemma in sorted(lemmas, key=len, reverse=True):
                pattern = rf"(?<![\w-])({re.escape(lemma)})(?![\w-])"
                updated, count = re.subn(
                    pattern,
                    lambda match: f"[{match.group(1)}]({relative_link(source, target)})",
                    updated,
                    count=1,
                    flags=re.IGNORECASE,
                )
                inserted += count
                if count:
                    linked.add(target)
                    break
        chunks[index] = updated

    return "".join(chunks), inserted


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    data = json.loads(CONCEPTS_PATH.read_text(encoding="utf-8"))
    for concept in data["concepts"]:
        path = ROOT / concept["file"]
        original = path.read_text(encoding="utf-8")
        updated, count = linkify(original, path, data["concepts"])
        if count:
            print(f"{path.relative_to(ROOT)}: +{count} links")
            if not args.dry_run:
                path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
