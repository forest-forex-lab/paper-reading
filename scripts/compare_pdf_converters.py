#!/usr/bin/env python3
"""Compare PDF-to-Markdown conversion across multiple tools.

Usage:
    uv run python scripts/compare_pdf_converters.py <pdf_path> [--output-dir <dir>]

Compares:
    1. pymupdf4llm  (current default)
    2. markitdown   (Microsoft)
    3. docling       (Docling Project)

Output:
    <output-dir>/pymupdf4llm/       paper.md + figures/
    <output-dir>/markitdown/        paper.md
    <output-dir>/docling/           paper.md + figures/
    <output-dir>/comparison.md      Timing & stats summary
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ConversionResult:
    """Immutable result of a single PDF conversion."""

    method: str
    elapsed_seconds: float
    output_path: Path
    char_count: int
    line_count: int
    image_count: int
    success: bool
    error: str | None = None


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare PDF-to-Markdown converters."
    )
    parser.add_argument("pdf_path", type=Path, help="Path to the input PDF file")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: <pdf_dir>/comparison/)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="DPI for image extraction (default: 200)",
    )
    parser.add_argument(
        "--methods",
        nargs="+",
        choices=["pymupdf4llm", "markitdown", "docling"],
        default=["pymupdf4llm", "markitdown", "docling"],
        help="Methods to compare (default: all three)",
    )
    return parser.parse_args(argv)


def _count_images(directory: Path) -> int:
    """Count image files in a directory."""
    if not directory.exists():
        return 0
    extensions = ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif")
    return sum(len(list(directory.glob(ext))) for ext in extensions)


def convert_with_pymupdf4llm(
    pdf_path: Path, output_dir: Path, dpi: int
) -> ConversionResult:
    """Convert PDF using pymupdf4llm."""
    method = "pymupdf4llm"
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    try:
        import pymupdf4llm
    except ImportError:
        return ConversionResult(
            method=method,
            elapsed_seconds=0.0,
            output_path=output_dir / "paper.md",
            char_count=0,
            line_count=0,
            image_count=0,
            success=False,
            error="pymupdf4llm not installed. Install with: uv add pymupdf4llm",
        )

    start = time.perf_counter()
    try:
        md_text: str = pymupdf4llm.to_markdown(
            str(pdf_path),
            write_images=True,
            image_path=str(figures_dir),
            dpi=dpi,
        )
        # Rewrite image paths to relative
        md_text = md_text.replace(str(figures_dir), "figures")

        elapsed = time.perf_counter() - start

        output_path = output_dir / "paper.md"
        output_path.write_text(md_text, encoding="utf-8")

        return ConversionResult(
            method=method,
            elapsed_seconds=elapsed,
            output_path=output_path,
            char_count=len(md_text),
            line_count=md_text.count("\n") + 1,
            image_count=_count_images(figures_dir),
            success=True,
        )
    except Exception as e:
        elapsed = time.perf_counter() - start
        return ConversionResult(
            method=method,
            elapsed_seconds=elapsed,
            output_path=output_dir / "paper.md",
            char_count=0,
            line_count=0,
            image_count=0,
            success=False,
            error=str(e),
        )


def convert_with_markitdown(
    pdf_path: Path, output_dir: Path
) -> ConversionResult:
    """Convert PDF using Microsoft markitdown."""
    method = "markitdown"
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        from markitdown import MarkItDown
    except ImportError:
        return ConversionResult(
            method=method,
            elapsed_seconds=0.0,
            output_path=output_dir / "paper.md",
            char_count=0,
            line_count=0,
            image_count=0,
            success=False,
            error="markitdown not installed. Install with: uv add 'markitdown[pdf]'",
        )

    start = time.perf_counter()
    try:
        md = MarkItDown()
        result = md.convert(str(pdf_path))
        md_text = result.text_content

        elapsed = time.perf_counter() - start

        output_path = output_dir / "paper.md"
        output_path.write_text(md_text, encoding="utf-8")

        return ConversionResult(
            method=method,
            elapsed_seconds=elapsed,
            output_path=output_path,
            char_count=len(md_text),
            line_count=md_text.count("\n") + 1,
            image_count=0,  # markitdown does not extract images
            success=True,
        )
    except Exception as e:
        elapsed = time.perf_counter() - start
        return ConversionResult(
            method=method,
            elapsed_seconds=elapsed,
            output_path=output_dir / "paper.md",
            char_count=0,
            line_count=0,
            image_count=0,
            success=False,
            error=str(e),
        )


def convert_with_docling(
    pdf_path: Path, output_dir: Path
) -> ConversionResult:
    """Convert PDF using Docling."""
    method = "docling"
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    try:
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        from docling.document_converter import DocumentConverter, PdfFormatOption
    except ImportError:
        return ConversionResult(
            method=method,
            elapsed_seconds=0.0,
            output_path=output_dir / "paper.md",
            char_count=0,
            line_count=0,
            image_count=0,
            success=False,
            error="docling not installed. Install with: uv add docling",
        )

    start = time.perf_counter()
    try:
        pipeline_opts = PdfPipelineOptions(
            generate_picture_images=True,
            images_scale=2.0,
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

        md_text = doc.export_to_markdown()

        # Extract images
        img_index = 0
        for item, _level in doc.iterate_items():
            if hasattr(item, "image") and item.image is not None:
                try:
                    pil_img = item.image.pil_image
                    if pil_img is not None:
                        img_path = figures_dir / f"img_{img_index:04d}.png"
                        pil_img.save(str(img_path))
                        img_index += 1
                except Exception:
                    pass

        elapsed = time.perf_counter() - start

        output_path = output_dir / "paper.md"
        output_path.write_text(md_text, encoding="utf-8")

        return ConversionResult(
            method=method,
            elapsed_seconds=elapsed,
            output_path=output_path,
            char_count=len(md_text),
            line_count=md_text.count("\n") + 1,
            image_count=_count_images(figures_dir),
            success=True,
        )
    except Exception as e:
        elapsed = time.perf_counter() - start
        return ConversionResult(
            method=method,
            elapsed_seconds=elapsed,
            output_path=output_dir / "paper.md",
            char_count=0,
            line_count=0,
            image_count=0,
            success=False,
            error=str(e),
        )


def generate_comparison_report(
    results: list[ConversionResult], pdf_path: Path
) -> str:
    """Generate a Markdown comparison report."""
    lines = [
        f"# PDF-to-Markdown Conversion Comparison",
        "",
        f"**Source PDF**: `{pdf_path.name}`  ",
        f"**File size**: {pdf_path.stat().st_size / 1024:.1f} KB  ",
        f"**Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Results Summary",
        "",
        "| Method | Time (s) | Characters | Lines | Images | Status |",
        "|--------|----------|------------|-------|--------|--------|",
    ]

    for r in results:
        status = "OK" if r.success else f"ERROR: {r.error}"
        lines.append(
            f"| {r.method} | {r.elapsed_seconds:.2f} | "
            f"{r.char_count:,} | {r.line_count:,} | "
            f"{r.image_count} | {status} |"
        )

    lines.extend([
        "",
        "## Details",
        "",
    ])

    for r in results:
        lines.append(f"### {r.method}")
        lines.append("")
        if r.success:
            lines.append(f"- **Output**: `{r.output_path}`")
            lines.append(f"- **Conversion time**: {r.elapsed_seconds:.2f} seconds")
            lines.append(f"- **Output size**: {r.char_count:,} characters, {r.line_count:,} lines")
            lines.append(f"- **Extracted images**: {r.image_count}")
        else:
            lines.append(f"- **Status**: FAILED")
            lines.append(f"- **Error**: {r.error}")
        lines.append("")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    pdf_path: Path = args.pdf_path.resolve()
    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}", file=sys.stderr)
        return 1

    output_dir: Path = (args.output_dir or pdf_path.parent / "comparison").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    converters: dict[str, callable] = {
        "pymupdf4llm": lambda: convert_with_pymupdf4llm(
            pdf_path, output_dir / "pymupdf4llm", args.dpi
        ),
        "markitdown": lambda: convert_with_markitdown(
            pdf_path, output_dir / "markitdown"
        ),
        "docling": lambda: convert_with_docling(
            pdf_path, output_dir / "docling"
        ),
    }

    results: list[ConversionResult] = []

    for method_name in args.methods:
        print(f"\n{'='*60}")
        print(f"Converting with: {method_name}")
        print(f"{'='*60}")

        convert_fn = converters[method_name]
        result = convert_fn()
        results.append(result)

        if result.success:
            print(f"  Time:   {result.elapsed_seconds:.2f}s")
            print(f"  Size:   {result.char_count:,} chars, {result.line_count:,} lines")
            print(f"  Images: {result.image_count}")
            print(f"  Output: {result.output_path}")
        else:
            print(f"  FAILED: {result.error}")

    # Generate comparison report
    report = generate_comparison_report(results, pdf_path)
    report_path = output_dir / "comparison.md"
    report_path.write_text(report, encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"Comparison report: {report_path}")
    print(f"{'='*60}")
    print()
    print(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
