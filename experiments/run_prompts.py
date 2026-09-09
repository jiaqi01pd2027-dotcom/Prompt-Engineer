#!/usr/bin/env python3
"""Expand a task spec into the 10 concrete prompts (placeholder substitution).

Usage: python3 run_prompts.py tasks/write-1.md  -> writes prompts/<task>/P0.txt ... P9.txt
"""
import re, sys, pathlib

def expand(path: pathlib.Path):
    text = path.read_text()
    task = path.stem
    # shared material: every <tag>...</tag> block in the Shared material section
    shared_sec = text.split("## Shared material", 1)[1].split("## Variants", 1)[0]
    blocks = {}
    for m in re.finditer(r"<(\w[\w-]*)>\n(.*?)\n</\1>", shared_sec, re.S):
        blocks[m.group(1)] = m.group(0)
    variants_sec = text.split("## Variants", 1)[1]
    out_dir = path.parent.parent / "prompts" / task
    out_dir.mkdir(parents=True, exist_ok=True)
    parts = re.split(r"^### (P\d) [^\n]*\n", variants_sec, flags=re.M)
    # parts: ['', 'P0', body, 'P1', body, ...]
    written = []
    for i in range(1, len(parts), 2):
        pid, body = parts[i], parts[i + 1].strip()
        for tag, full in blocks.items():
            body = body.replace(f"<{tag}>...</{tag}>", full)
        if "...</" in body:
            print(f"WARN {task} {pid}: unresolved placeholder", file=sys.stderr)
        (out_dir / f"{pid}.txt").write_text(body + "\n")
        written.append(pid)
    print(task, " ".join(written))

if __name__ == "__main__":
    for p in sys.argv[1:]:
        expand(pathlib.Path(p))
