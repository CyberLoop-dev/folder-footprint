#!/usr/bin/env python3
"""Create a local HTML report of folder sizes and the largest files."""
from __future__ import annotations
import argparse, html, os, sys
from pathlib import Path

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__"}

def human_size(value: int) -> str:
    amount = float(value)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if amount < 1024 or unit == "TB": return f"{amount:.1f} {unit}"
        amount /= 1024
    return f"{amount:.1f} TB"

def scan(root: Path, output: Path, max_files: int):
    largest, top_level, errors = [], [], 0
    output_resolved = output.resolve()
    def visit(path: Path) -> int:
        nonlocal errors
        try:
            if path.is_symlink(): return 0
            if path.resolve() == output_resolved: return 0
            if path.is_file():
                size = path.stat().st_size
                largest.append((size, path))
                return size
            if not path.is_dir(): return 0
            total = 0
            with os.scandir(path) as entries:
                for entry in entries:
                    child = Path(entry.path)
                    if child.name in SKIP_DIRS: continue
                    total += visit(child)
            return total
        except (OSError, PermissionError):
            errors += 1
            return 0
    total = visit(root)
    try:
        with os.scandir(root) as entries:
            for entry in entries:
                child = Path(entry.path)
                if child.name in SKIP_DIRS: continue
                top_level.append((visit(child), child.name))
    except OSError:
        errors += 1
    largest.sort(key=lambda item: item[0], reverse=True)
    top_level.sort(reverse=True)
    return total, top_level, largest[:max_files], errors

def render(root: Path, total: int, folders, files, errors: int) -> str:
    max_folder = max((size for size, _ in folders), default=1) or 1
    folder_rows = "".join(
        f'<tr><td>{html.escape(name)}</td><td>{human_size(size)}</td><td><div class="track"><i style="width:{size/max_folder*100:.1f}%"></i></div></td></tr>'
        for size, name in folders
    )
    file_rows = "".join(
        f'<tr><td>{html.escape(str(path))}</td><td>{human_size(size)}</td></tr>'
        for size, path in files
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Folder Footprint</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#0b1220;color:#e5edf7;font:15px/1.5 system-ui,sans-serif;padding:32px}}
main{{max-width:1000px;margin:auto}}h1{{font-size:2.4rem;margin-bottom:4px}}.muted{{color:#94a3b8}}.hero,section{{background:#111c2e;border:1px solid #263b54;border-radius:18px;padding:22px;margin:18px 0}}
.big{{font-size:2.4rem;color:#5eead4;font-weight:700}}table{{width:100%;border-collapse:collapse}}th,td{{text-align:left;padding:12px;border-bottom:1px solid #263b54;overflow-wrap:anywhere}}th{{color:#a5f3fc}}.track{{height:9px;background:#263b54;border-radius:20px;overflow:hidden}}.track i{{display:block;height:100%;background:#2dd4bf;border-radius:20px}}
</style></head><body><main><h1>Folder Footprint</h1><p class="muted">Read-only size report for {html.escape(str(root))}</p>
<div class="hero"><div class="big">{human_size(total)}</div><div class="muted">Total readable file size · {errors} scan errors</div></div>
<section><h2>📁 Top-level folders and files</h2><table><thead><tr><th>Name</th><th>Size</th><th>Relative size</th></tr></thead><tbody>{folder_rows}</tbody></table></section>
<section><h2>📦 Largest files</h2><table><thead><tr><th>Path</th><th>Size</th></tr></thead><tbody>{file_rows}</tbody></table></section>
<p class="muted">Symlinks and common generated folders are skipped. This report does not delete or modify files.</p></main></body></html>"""

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("folder-footprint.html"))
    parser.add_argument("--max-files", type=int, default=30)
    args = parser.parse_args()
    root = args.folder.expanduser().resolve()
    if not root.is_dir(): parser.error(f"folder does not exist: {root}")
    if args.max_files < 1: parser.error("--max-files must be positive")
    try:
        total, folders, files, errors = scan(root, args.output, args.max_files)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(render(root, total, folders, files, errors), encoding="utf-8")
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr); return 2
    print(f"Report written to {args.output} ({human_size(total)}, {errors} scan errors)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
