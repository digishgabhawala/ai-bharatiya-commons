#!/usr/bin/env python3
"""Validate the portable AI Bharatiyaa CSS token contract."""

from __future__ import annotations

import math
import re
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOKENS_PATH = ROOT / "design-tokens" / "tokens.css"
PREVIEW_CSS_PATH = ROOT / "preview" / "preview.css"
PREVIEW_HTML_PATH = ROOT / "preview" / "index.html"
TOKEN_PATTERN = re.compile(r"(--[a-z0-9-]+)\s*:\s*([^;]+);")
REFERENCE_PATTERN = re.compile(r"var\((--[a-z0-9-]+)")
HEX_PATTERN = re.compile(r"^#([0-9a-f]{6})$", re.IGNORECASE)

CONTRAST_PAIRS = (
    ("--color-text-strong", "--color-surface", 4.5),
    ("--color-text", "--color-surface", 4.5),
    ("--color-text-muted", "--color-surface", 4.5),
    ("--color-text-on-action", "--color-action", 4.5),
    ("--color-info", "--color-info-surface", 4.5),
    ("--color-success", "--color-success-surface", 4.5),
    ("--color-warning", "--color-warning-surface", 4.5),
    ("--color-danger", "--color-danger-surface", 4.5),
)


class PreviewParser(HTMLParser):
    """Collect ID relationships that can be checked without a browser."""

    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.references: list[tuple[str, str]] = []
        self.has_lang = False
        self.has_viewport = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        identifier = attributes.get("id")
        if identifier:
            if identifier in self.ids:
                self.duplicate_ids.add(identifier)
            self.ids.add(identifier)

        if tag == "html" and attributes.get("lang"):
            self.has_lang = True
        if tag == "meta" and attributes.get("name") == "viewport":
            self.has_viewport = True

        for attribute in ("for", "aria-describedby", "aria-labelledby"):
            for reference in (attributes.get(attribute) or "").split():
                self.references.append((attribute, reference))


def root_block(css: str) -> str:
    start = css.index(":root {") + len(":root {")
    depth = 1
    for index in range(start, len(css)):
        if css[index] == "{":
            depth += 1
        elif css[index] == "}":
            depth -= 1
            if depth == 0:
                return css[start:index]
    raise ValueError("The :root block is not closed")


def resolve_color(name: str, tokens: dict[str, str], seen: set[str] | None = None) -> str:
    seen = set() if seen is None else seen
    if name in seen:
        raise ValueError(f"Circular token reference involving {name}")
    seen.add(name)
    value = tokens[name].strip().lower()
    match = re.fullmatch(r"var\((--[a-z0-9-]+)\)", value)
    if match:
        return resolve_color(match.group(1), tokens, seen)
    if not HEX_PATTERN.fullmatch(value):
        raise ValueError(f"{name} does not resolve to a six-digit hex color")
    return value


def relative_luminance(color: str) -> float:
    channels = [int(color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else math.pow((value + 0.055) / 1.055, 2.4) for value in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(first: str, second: str) -> float:
    light, dark = sorted((relative_luminance(first), relative_luminance(second)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def main() -> int:
    css = TOKENS_PATH.read_text(encoding="utf-8")
    declarations = TOKEN_PATTERN.findall(root_block(css))
    tokens: dict[str, str] = {}
    errors: list[str] = []

    for name, value in declarations:
        if name in tokens:
            errors.append(f"Duplicate :root token: {name}")
        tokens[name] = value.strip()

    references = set(REFERENCE_PATTERN.findall(css))
    for reference in sorted(references - tokens.keys()):
        errors.append(f"Undefined token reference: {reference}")

    for foreground, background, minimum in CONTRAST_PAIRS:
        try:
            ratio = contrast(resolve_color(foreground, tokens), resolve_color(background, tokens))
        except (KeyError, ValueError) as error:
            errors.append(str(error))
            continue
        if ratio < minimum:
            errors.append(
                f"Contrast {foreground} on {background} is {ratio:.2f}:1; expected {minimum:.1f}:1"
            )
        else:
            print(f"PASS contrast {foreground} on {background}: {ratio:.2f}:1")

    preview_css = PREVIEW_CSS_PATH.read_text(encoding="utf-8")
    preview_declarations = {name for name, _ in TOKEN_PATTERN.findall(preview_css)}
    preview_references = set(REFERENCE_PATTERN.findall(preview_css))
    for reference in sorted(preview_references - tokens.keys() - preview_declarations):
        errors.append(f"Undefined preview token reference: {reference}")

    parser = PreviewParser()
    parser.feed(PREVIEW_HTML_PATH.read_text(encoding="utf-8"))
    for identifier in sorted(parser.duplicate_ids):
        errors.append(f"Duplicate preview ID: {identifier}")
    for attribute, reference in parser.references:
        if reference not in parser.ids:
            errors.append(f"Broken preview {attribute} reference: {reference}")
    if not parser.has_lang:
        errors.append("Preview document is missing a language")
    if not parser.has_viewport:
        errors.append("Preview document is missing the viewport meta tag")

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1

    print(f"PASS {len(tokens)} root tokens; all CSS references resolve")
    print(f"PASS {len(parser.ids)} unique preview IDs; all semantic references resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
