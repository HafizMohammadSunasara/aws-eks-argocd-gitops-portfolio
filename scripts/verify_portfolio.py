#!/usr/bin/env python3
"""Offline structural checks for the public GitOps portfolio package."""

from __future__ import annotations

import hashlib
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "DEEP-DIVE.md",
    "SECURITY.md",
    "PUBLISHING.md",
    "assets/hero.svg",
    "assets/architecture.svg",
    "docs/index.html",
    "docs/site-assets/style.css",
    "docs/site-assets/app.js",
    "evidence/INDEX.md",
    "reference-source/SOURCE-PROVENANCE.md",
    "reference-source/.github/workflows/pipeline.yml",
]
LINK_RE = re.compile(r"!?\[[^\]\n]*\]\(([^)\s]+)")
SECRET_RE = re.compile(
    r"\bAKIA[0-9A-Z]{16}\b|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
)


class LocalLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.urls.append(value)


def local_target(base: Path, href: str) -> Path | None:
    if href.startswith("#") or href.startswith("//"):
        return None
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        return None
    return (base.parent / unquote(parsed.path)).resolve() if parsed.path else None


def check_links(file: Path, urls: list[str], errors: list[str]) -> None:
    for url in urls:
        target = local_target(file, url)
        if target is None:
            continue
        if not target.is_relative_to(ROOT):
            errors.append(f"{file.relative_to(ROOT)}: escapes project root: {url}")
        elif not target.exists():
            errors.append(f"{file.relative_to(ROOT)}: missing {url}")


def main() -> int:
    errors: list[str] = []
    for name in REQUIRED:
        if not (ROOT / name).is_file():
            errors.append(f"Missing required file: {name}")

    for source in ROOT.rglob("*.svg"):
        try:
            ET.parse(source)
        except ET.ParseError as exc:
            errors.append(f"Invalid SVG {source.relative_to(ROOT)}: {exc}")

    for source in ROOT.rglob("*.md"):
        text = source.read_text(encoding="utf-8")
        check_links(source, LINK_RE.findall(text), errors)
        if SECRET_RE.search(text):
            errors.append(f"Potential secret in {source.relative_to(ROOT)}")

    html_count = 0
    for source in ROOT.rglob("*.html"):
        if "reference-source" in source.parts:
            continue  # Jinja/Flask templates are not static website documents.
        html_count += 1
        parser = LocalLinks()
        parser.feed(source.read_text(encoding="utf-8"))
        check_links(source, parser.urls, errors)

    screenshots = sorted((ROOT / "evidence/screenshots").glob("*.png"))
    gallery = sorted((ROOT / "docs/site-assets/gallery").glob("*.png"))
    if len(screenshots) != 16:
        errors.append(f"Expected 16 curated evidence screenshots; found {len(screenshots)}")
    if len(gallery) != 8:
        errors.append(f"Expected 8 highlighted Pages images; found {len(gallery)}")

    checksums = ROOT / "evidence/SHA256SUMS.txt"
    if checksums.exists():
        for line in checksums.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            try:
                expected, rel = line.split("  ", maxsplit=1)
                target = (ROOT / "evidence" / rel).resolve()
                actual = hashlib.sha256(target.read_bytes()).hexdigest()
                if actual != expected:
                    errors.append(f"Evidence checksum mismatch: {rel}")
            except (ValueError, OSError):
                errors.append(f"Malformed evidence checksum line: {line[:90]}")

    git_blobs = ROOT / "reference-source/GIT-BLOBS.txt"
    if git_blobs.exists():
        for line in git_blobs.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            try:
                expected, rel = line.split("  ", maxsplit=1)
                source = (ROOT / "reference-source" / rel).resolve()
                data = source.read_bytes()
                payload = b"blob " + str(len(data)).encode("ascii") + b"\x00" + data
                actual = hashlib.sha1(payload).hexdigest()  # Git's blob object ID format
                if actual != expected:
                    errors.append(f"Reference source Git blob mismatch: {rel}")
            except (ValueError, OSError):
                errors.append(f"Malformed source provenance line: {line[:90]}")

    print(f"Portfolio checks: {len(screenshots)} evidence images; {len(gallery)} gallery images; {html_count} static HTML page(s).")
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print("PASS: Required files, local links, SVG parsing, evidence checksums and source Git blob hashes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
