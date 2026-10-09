#!/usr/bin/env python3
"""Generate a small animated neofetch-style SVG info card.

Run from the repository root:
    python scripts/make_info_card.py

Set STATIC=1 to disable animations for local previews:
    # PowerShell
    $env:STATIC = "1"; python scripts/make_info_card.py

    # macOS / Linux
    STATIC=1 python scripts/make_info_card.py
"""

from __future__ import annotations

import html
import os
from pathlib import Path

# Keep the short, human story here. Update these rows when your focus changes.
ROWS = [
    ("Now", "Outreach, growth & creative operations", "#8be9fd"),
    ("Prev", "Content, social media & fintech", "#bd93f9"),
    ("Stack", "Research · writing · coordination · design", "#50fa7b"),
    ("Highlights", "100+ prospects/week · ~30% less manual prospecting", "#ffb86c"),
]

OUTPUT = Path(__file__).resolve().parent.parent / "info-card.svg"
STATIC = os.getenv("STATIC", "").strip().lower() in {"1", "true", "yes", "on"}

WIDTH = 720
PADDING = 28
TITLE_HEIGHT = 54
ROW_HEIGHT = 48
HEIGHT = TITLE_HEIGHT + PADDING + ROW_HEIGHT * len(ROWS) + PADDING


def text_element(x: int, y: int, value: str, *, fill: str, size: int,
                 weight: int = 400, family: str = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace") -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-family="{family}" '
        f'font-size="{size}" font-weight="{weight}">{html.escape(value)}</text>'
    )


def build_svg() -> str:
    pieces = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="card-title card-desc">',
        '<title id="card-title">Rishika profile info card</title>',
        '<desc id="card-desc">A neofetch-inspired panel with current focus, previous experience, working stack, and selected highlights.</desc>',
        '<defs>',
        '<linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">',
        '<stop offset="0%" stop-color="#111827"/>',
        '<stop offset="100%" stop-color="#0b1020"/>',
        '</linearGradient>',
        '<style>',
        '.row { opacity: 1; transform: translateY(0); }',
    ]

    if not STATIC:
        pieces.extend([
            '@keyframes reveal { from { opacity: 0; transform: translateY(7px); } to { opacity: 1; transform: translateY(0); } }',
            '.row { opacity: 0; animation: reveal 420ms ease-out forwards; }',
            '@media (prefers-reduced-motion: reduce) { .row { opacity: 1; animation: none; transform: none; } }',
        ])

    pieces.extend([
        '</style>',
        '</defs>',
        '<rect x="1" y="1" width="718" height="{}" rx="14" fill="url(#panel)" stroke="#30394d" stroke-width="2"/>'.format(HEIGHT - 2),
        f'<path d="M15 1 H705 Q719 1 719 15 V{TITLE_HEIGHT} H1 V15 Q1 1 15 1Z" fill="#1b2435"/>',
    ])

    for index, color in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        pieces.append(f'<circle cx="{24 + index * 20}" cy="27" r="5" fill="{color}"/>')

    pieces.append(text_element(95, 32, "rishixpansion  /  profile", fill="#cbd5e1", size=14, weight=600))

    for index, (label, value, color) in enumerate(ROWS):
        y = TITLE_HEIGHT + PADDING + index * ROW_HEIGHT
        delay = index * 180
        pieces.append(f'<g class="row" style="animation-delay:{delay}ms">')
        pieces.append(text_element(PADDING, y + 10, label, fill=color, size=15, weight=700))
        pieces.append(text_element(170, y + 10, value, fill="#e5e7eb", size=14))
        pieces.append(f'<line x1="{PADDING}" y1="{y + 25}" x2="{WIDTH - PADDING}" y2="{y + 25}" stroke="#273246" stroke-width="1"/>')
        pieces.append('</g>')

    pieces.append('</svg>')
    return "\n".join(pieces) + "\n"


def main() -> None:
    OUTPUT.write_text(build_svg(), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(Path.cwd()) if OUTPUT.is_relative_to(Path.cwd()) else OUTPUT}")


if __name__ == "__main__":
    main()
