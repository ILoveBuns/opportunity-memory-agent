#!/usr/bin/env python3
"""Render the GOAI Markdown proposal as a reproducible 11-page landscape PDF."""

from __future__ import annotations

import html
import os
import re
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "GOAI_PROPOSAL.md"
OUTPUT = ROOT / "GOAI_PROPOSAL.pdf"
FONT = Path(
    os.environ.get(
        "GOAI_CJK_FONT", "/root/.local/share/fonts/NotoSansCJKsc-Regular.otf"
    )
)
MONO = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")


def inline_markup(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"`(.+?)`", r'<font name="GoaiMono">\1</font>', escaped)
    return escaped


def page_number(canvas, document) -> None:
    canvas.saveState()
    canvas.setFillColor(HexColor("#6f879f"))
    canvas.setFont("GoaiSans", 8)
    canvas.drawRightString(landscape(A4)[0] - 18 * mm, 10 * mm, str(document.page))
    canvas.restoreState()


def main() -> None:
    if not FONT.is_file() or not MONO.is_file():
        raise SystemExit("required Noto Sans CJK and DejaVu Sans Mono fonts are missing")
    pdfmetrics.registerFont(TTFont("GoaiSans", FONT))
    pdfmetrics.registerFont(TTFont("GoaiMono", MONO))

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "GoaiTitle",
        parent=styles["Title"],
        fontName="GoaiSans",
        fontSize=30,
        leading=40,
        textColor=HexColor("#07111f"),
        alignment=TA_CENTER,
        spaceAfter=12,
    )
    subtitle = ParagraphStyle(
        "GoaiSubtitle",
        parent=styles["Normal"],
        fontName="GoaiSans",
        fontSize=16,
        leading=24,
        textColor=HexColor("#28435f"),
        alignment=TA_CENTER,
    )
    heading = ParagraphStyle(
        "GoaiHeading",
        parent=styles["Heading1"],
        fontName="GoaiSans",
        fontSize=24,
        leading=32,
        textColor=HexColor("#0a8f80"),
        spaceAfter=18,
    )
    body = ParagraphStyle(
        "GoaiBody",
        parent=styles["BodyText"],
        fontName="GoaiSans",
        fontSize=12,
        leading=20,
        textColor=HexColor("#102238"),
        spaceAfter=9,
    )
    bullet = ParagraphStyle(
        "GoaiBullet",
        parent=body,
        leftIndent=14,
        firstLineIndent=-10,
        bulletIndent=0,
    )
    code = ParagraphStyle(
        "GoaiCode",
        parent=body,
        fontName="GoaiMono",
        fontSize=9,
        leading=13,
        backColor=HexColor("#eef5f7"),
        borderPadding=8,
    )

    segments = SOURCE.read_text(encoding="utf-8").split("\n---\n")
    if len(segments) != 11:
        raise SystemExit(f"expected cover plus 10 proposal sections, found {len(segments)}")

    story = []
    for page_index, segment in enumerate(segments):
        lines = segment.strip().splitlines()
        in_code = False
        code_lines: list[str] = []
        if page_index == 0:
            story.extend([Spacer(1, 48 * mm)])
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("```"):
                if in_code:
                    story.append(Preformatted("\n".join(code_lines), code))
                    code_lines = []
                    in_code = False
                else:
                    in_code = True
                continue
            if in_code:
                code_lines.append(line)
            elif stripped.startswith("# "):
                story.append(Paragraph(inline_markup(stripped[2:]), title))
            elif stripped.startswith("## "):
                story.append(Paragraph(inline_markup(stripped[3:]), heading))
            elif stripped.startswith("- "):
                story.append(Paragraph("• " + inline_markup(stripped[2:]), bullet))
            elif stripped:
                style = subtitle if page_index == 0 else body
                story.append(Paragraph(inline_markup(stripped), style))
        if in_code:
            raise SystemExit(f"unclosed code block in segment {page_index + 1}")
        if page_index < len(segments) - 1:
            story.append(PageBreak())

    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=landscape(A4),
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=16 * mm,
        title="Opportunity Memory Agent — GOAI 2026",
        author="ILoveBuns",
    )
    document.build(story, onFirstPage=page_number, onLaterPages=page_number)
    print(OUTPUT)


if __name__ == "__main__":
    main()
