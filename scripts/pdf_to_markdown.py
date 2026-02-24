#!/usr/bin/env python3
"""Convert a PDF to Markdown with image extraction using Docling.

Usage:
    uv run python scripts/pdf_to_markdown.py <pdf_path> [--output-dir <dir>]

If --output-dir is not specified, outputs to the same directory as the PDF.

Output:
    <output-dir>/paper.md              Markdown text with embedded image references
    <output-dir>/paper_artifacts/      Extracted images (PNG)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert PDF to Markdown with image extraction (Docling)."
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
        "--image-scale",
        type=float,
        default=2.0,
        help="Scale factor for extracted images (default: 2.0)",
    )
    return parser.parse_args(argv)


def convert_pdf_to_markdown(
    pdf_path: Path,
    output_dir: Path,
    output_name: str = "paper.md",
    image_scale: float = 2.0,
) -> Path:
    """Convert a PDF file to Markdown with extracted images using Docling.

    Uses Docling's DocumentConverter with ImageRefMode.REFERENCED to produce
    Markdown with image file references.

    Args:
        pdf_path: Path to the input PDF file.
        output_dir: Directory to write output files.
        output_name: Name of the output markdown file.
        image_scale: Scale factor for image extraction resolution.

    Returns:
        Path to the generated markdown file.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        ImportError: If docling is not installed.
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    try:
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        from docling.document_converter import DocumentConverter, PdfFormatOption
        from docling_core.types.doc import ImageRefMode
    except ImportError as e:
        raise ImportError(
            "docling is required. Install with: uv add docling"
        ) from e

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Converting: {pdf_path}")

    pipeline_opts = PdfPipelineOptions(
        generate_picture_images=True,
        images_scale=image_scale,
    )
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_opts
            )
        }
    )

    result = converter.convert(str(pdf_path))
    doc = result.document

    output_path = output_dir / output_name
    doc.save_as_markdown(
        output_path,
        image_mode=ImageRefMode.REFERENCED,
    )

    # Rewrite absolute image paths to relative
    md_text = output_path.read_text(encoding="utf-8")
    abs_output_dir = str(output_dir.resolve()) + "/"
    md_text = md_text.replace(abs_output_dir, "")
    output_path.write_text(md_text, encoding="utf-8")

    # Count extracted images
    stem = Path(output_name).stem
    artifacts_dir = output_dir / f"{stem}_artifacts"
    image_count = 0
    if artifacts_dir.exists():
        image_count = (
            len(list(artifacts_dir.glob("*.png")))
            + len(list(artifacts_dir.glob("*.jpg")))
        )

    print(f"  Markdown: {output_path}")
    print(f"  Images:   {image_count} files in {artifacts_dir}/")

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
            image_scale=args.image_scale,
        )
    except (FileNotFoundError, ImportError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
