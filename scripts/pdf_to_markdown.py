#!/usr/bin/env python3
"""Convert a PDF to Markdown with image extraction.

Usage:
    uv run python scripts/pdf_to_markdown.py <pdf_path> [--output-dir <dir>]

If --output-dir is not specified, outputs to the same directory as the PDF.

Output:
    <output-dir>/paper.md       Markdown text with embedded image references
    <output-dir>/figures/        Extracted images (PNG)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert PDF to Markdown with image extraction."
    )
    parser.add_argument("pdf_path", type=Path, help="Path to the input PDF file")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: same directory as PDF)",
    )
    parser.add_argument(
        "--output-name",
        type=str,
        default="paper.md",
        help="Output markdown filename (default: paper.md)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="DPI for image extraction (default: 200)",
    )
    return parser.parse_args(argv)


def _clean_paragraph_breaks(md_text: str) -> str:
    """Join intra-paragraph line breaks while preserving block-level structure.

    Processes blank-line-separated blocks. Within each block, joins lines
    that are plain paragraph text. Preserves headings, lists, code fences,
    images, tables, math blocks, and blockquotes.
    """
    lines = md_text.split("\n")
    result: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Pass through code fences verbatim
        if line.strip().startswith("```"):
            result.append(line)
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                result.append(lines[i])
                i += 1
            if i < len(lines):
                result.append(lines[i])
                i += 1
            continue

        # Pass through math blocks ($$...$$) verbatim
        if line.strip().startswith("$$"):
            result.append(line)
            # If $$ is on its own line, find closing $$
            if line.strip() == "$$":
                i += 1
                while i < len(lines) and lines[i].strip() != "$$":
                    result.append(lines[i])
                    i += 1
                if i < len(lines):
                    result.append(lines[i])
                    i += 1
            else:
                i += 1
            continue

        # Blank lines pass through
        if line.strip() == "":
            result.append(line)
            i += 1
            continue

        # Lines that should never be joined with subsequent lines
        if _is_block_element(line):
            result.append(line)
            i += 1
            continue

        # Collect consecutive paragraph lines for joining
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() != "" and not _is_block_element(lines[i]):
            # Stop if next line starts a code fence or math block
            if lines[i].strip().startswith("```") or lines[i].strip().startswith("$$"):
                break
            para_lines.append(lines[i])
            i += 1

        joined = _join_lines(para_lines)
        result.append(joined)

    return "\n".join(result)


def _is_block_element(line: str) -> bool:
    """Check if a line is a block-level Markdown element that should not be joined."""
    stripped = line.strip()
    if stripped.startswith("#"):
        return True
    if re.match(r"^[-*+]\s", stripped):
        return True
    if re.match(r"^\d+\.\s", stripped):
        return True
    if stripped.startswith("!["):
        return True
    if stripped.startswith("|"):
        return True
    if stripped.startswith(">"):
        return True
    if stripped.startswith("---") or stripped.startswith("***") or stripped.startswith("___"):
        return True
    return False


def _join_lines(lines: list[str]) -> str:
    """Join paragraph lines, repairing hyphenation at line breaks."""
    if len(lines) <= 1:
        return lines[0] if lines else ""

    parts: list[str] = []
    for j, line in enumerate(lines):
        text = line.strip()
        if j < len(lines) - 1:
            # Repair hyphenation: "word-" + "continuation" -> "wordcontinuation"
            if text.endswith("-") and not text.endswith("--"):
                next_line = lines[j + 1].strip()
                if next_line and next_line[0].islower():
                    text = text[:-1]
                    parts.append(text)
                    continue
            parts.append(text + " ")
        else:
            parts.append(text)

    return "".join(parts).rstrip()


def convert_pdf_to_markdown(
    pdf_path: Path,
    output_dir: Path,
    output_name: str = "paper.md",
    dpi: int = 200,
) -> Path:
    """Convert a PDF file to Markdown with extracted images.

    Uses pymupdf4llm for text extraction and applies post-processing
    to clean up paragraph breaks.

    Args:
        pdf_path: Path to the input PDF file.
        output_dir: Directory to write output files.
        output_name: Name of the output markdown file.
        dpi: Resolution for image extraction.

    Returns:
        Path to the generated markdown file.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        ImportError: If pymupdf4llm is not installed.
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    try:
        import pymupdf4llm
    except ImportError as e:
        raise ImportError(
            "pymupdf4llm is required. Install with: uv add pymupdf4llm"
        ) from e

    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    print(f"Converting: {pdf_path}")

    md_text: str = pymupdf4llm.to_markdown(
        str(pdf_path),
        write_images=True,
        image_path=str(figures_dir),
        dpi=dpi,
    )

    # Rewrite image paths to be relative to output_dir
    abs_figures = str(figures_dir)
    rel_figures = str(figures_dir.relative_to(output_dir))
    md_text = md_text.replace(abs_figures, rel_figures)

    md_text = _clean_paragraph_breaks(md_text)

    output_path = output_dir / output_name
    output_path.write_text(md_text, encoding="utf-8")

    image_count = len(list(figures_dir.glob("*.png"))) + len(
        list(figures_dir.glob("*.jpg"))
    )
    print(f"  Markdown: {output_path}")
    print(f"  Images:   {image_count} files in {figures_dir}/")

    return output_path


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    pdf_path: Path = args.pdf_path.resolve()
    output_dir: Path = (args.output_dir or pdf_path.parent).resolve()

    try:
        convert_pdf_to_markdown(
            pdf_path=pdf_path,
            output_dir=output_dir,
            output_name=args.output_name,
            dpi=args.dpi,
        )
    except (FileNotFoundError, ImportError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
