#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
from urllib.request import urlopen

DEFAULT_REF = "main"
URL_TEMPLATE = (
    "https://raw.githubusercontent.com/anthropics/claude-plugins-official/"
    "{ref}/plugins/code-simplifier/agents/code-simplifier.md"
)

def fetch_text(url: str) -> str:
    try:
        with urlopen(url) as response:
            data = response.read()
    except Exception as exc:
        raise RuntimeError(f"Failed to download {url}: {exc}") from exc
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError("Downloaded content is not valid UTF-8") from exc


def split_frontmatter(text: str):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    frontmatter = []
    i = 1
    while i < len(lines):
        if lines[i].strip() == "---":
            break
        frontmatter.append(lines[i])
        i += 1
    if i == len(lines):
        return {}, text
    body = "\n".join(lines[i + 1 :]).lstrip("\n")
    parsed = {}
    for line in frontmatter:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip()
    return parsed, body


def build_skill_text(name: str, description: str, body: str) -> str:
    header = f"---\nname: {name}\ndescription: {description}\n---\n\n"
    return header + "# Code Simplifier\n\n" + body.rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync code-simplifier from anthropics/claude-plugins-official"
    )
    parser.add_argument("--ref", default=DEFAULT_REF, help="Git ref, default: main")
    parser.add_argument("--url", default="", help="Override raw URL")
    args = parser.parse_args()

    url = args.url or URL_TEMPLATE.format(ref=args.ref)

    try:
        text = fetch_text(url)
        frontmatter, body = split_frontmatter(text)
        name = frontmatter.get("name", "code-simplifier")
        description = frontmatter.get(
            "description",
            "Simplifies and refines code for clarity, consistency, and maintainability "
            "while preserving all functionality.",
        )
        if not body.strip():
            raise RuntimeError("Downloaded content has no body")
        skill_text = build_skill_text(name, description, body)
        skill_path = Path(__file__).resolve().parents[1] / "SKILL.md"
        skill_path.write_text(skill_text, encoding="utf-8")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Updated {skill_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
