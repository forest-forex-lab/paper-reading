#!/usr/bin/env python3
"""Convert a PDF to Markdown with image extraction.

Usage:
    python scripts/pdf_to_markdown.py <pdf_path> [--output-dir <dir>]

If --output-dir is not specified, outputs to the same directory as the PDF.

Output:
    <output-dir>/paper.md       Markdown text with embedded image references
    <output-dir>/figures/        Extracted images (PNG)
"""

from __future__ import annotations

import argparse
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


def convert_pdf_to_markdown(
    pdf_path: Path,
    output_dir: Path,
    output_name: str = "paper.md",
    dpi: int = 200,
) -> Path:
    """Convert a PDF file to Markdown with extracted images.

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
        import pymupdf4llm  # noqa: F811
    except ImportError as e:
        raise ImportError(
            "pymupdf4llm is required. Install with: pip install pymupdf4llm"
        ) from e

    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    md_text: str = pymupdf4llm.to_markdown(
        str(pdf_path),
        write_images=True,
        image_path=str(figures_dir),
        dpi=dpi,
    )

    # Rewrite image paths to be relative to output_dir
    md_text = _rewrite_image_paths(md_text, figures_dir, output_dir)

    output_path = output_dir / output_name
    output_path.write_text(md_text, encoding="utf-8")

    image_count = len(list(figures_dir.glob("*.png"))) + len(
        list(figures_dir.glob("*.jpg"))
    )
    print(f"Converted: {pdf_path}")
    print(f"  Markdown: {output_path}")
    print(f"  Images:   {image_count} files in {figures_dir}/")

    return output_path


def _rewrite_image_paths(
    md_text: str, figures_dir: Path, output_dir: Path
) -> str:
    """Rewrite absolute image paths to relative paths from output_dir."""
    abs_figures = str(figures_dir)
    rel_figures = str(figures_dir.relative_to(output_dir))
    return md_text.replace(abs_figures, rel_figures)


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
    except (FileNotFoundError, ImportError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
