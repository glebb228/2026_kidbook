#!/usr/bin/env python3

import json
import os
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONCEPTS_PATH = ROOT / "concepts.json"
OUTPUT_DIR = ROOT / "generated_drafts"


def build_prompt(concept: dict) -> str:
    return f"""Напиши статью для детской энциклопедии KidBook.
Объясни для десятилетнего ребенка понятие: {concept['name']}.
Описание: {concept['description']}
Используй понятные примеры, короткие разделы и GitHub Flavored Markdown.
Не выдумывай факты. В конце добавь три вопроса для самопроверки.
"""


def request_draft(prompt: str) -> str:
    api_url = os.environ["LLM_API_URL"].rstrip("/") + "/chat/completions"
    payload = {
        "model": os.environ["LLM_MODEL"],
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
    }
    request = urllib.request.Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {os.environ['LLM_API_KEY']}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def main() -> None:
    data = json.loads(CONCEPTS_PATH.read_text(encoding="utf-8"))
    OUTPUT_DIR.mkdir(exist_ok=True)
    for index, concept in enumerate(data["concepts"], start=1):
        draft = request_draft(build_prompt(concept))
        output = OUTPUT_DIR / f"{index:02d}_{concept['id'].split('/')[-1]}.md"
        output.write_text(draft.rstrip() + "\n", encoding="utf-8")
        print(f"Saved {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

