#!/usr/bin/env python3
"""Build a blind judging bundle for a task: anonymise + shuffle the 30 outputs.

Usage: python3 make_bundle.py write-1  -> judge/write-1/bundle.md + key.json
"""
import json, pathlib, random, sys, re

ROOT = pathlib.Path(__file__).parent
MODELS = ["fable", "opus", "sonnet"]
PATTERNS = [f"P{i}" for i in range(10)]

def main(task):
    spec = (ROOT / "tasks" / f"{task}.md").read_text()
    rubric = spec.split("## Hidden rubric", 1)[1].split("## Shared material", 1)[0].strip()
    shared = spec.split("## Shared material", 1)[1].split("## Variants", 1)[0].strip()
    items = []
    for m in MODELS:
        for p in PATTERNS:
            f = ROOT / "results" / task / m / f"{p}.md"
            if f.exists():
                items.append({"model": m, "pattern": p, "text": f.read_text()})
    rnd = random.Random(f"{task}-seed")
    rnd.shuffle(items)
    out = ROOT / "judge" / task
    out.mkdir(parents=True, exist_ok=True)
    key = {}
    parts = [f"# Blind judging bundle: {task}\n",
             "## Task as the prompt-writer understood it, and hidden rubric\n", rubric, "\n",
             "## Shared material\n", shared, "\n", "## Outputs (order randomised, labels anonymous)\n"]
    for i, it in enumerate(items, 1):
        oid = f"O{i:02d}"
        key[oid] = {"model": it["model"], "pattern": it["pattern"]}
        # strip any obvious self-identification of the pattern
        txt = it["text"].strip()
        parts.append(f"\n### {oid}\n\n<output id=\"{oid}\">\n{txt}\n</output>\n")
    (out / "bundle.md").write_text("\n".join(parts))
    (out / "key.json").write_text(json.dumps(key, indent=1))
    print(task, len(items), "outputs bundled ->", out / "bundle.md")

if __name__ == "__main__":
    for t in sys.argv[1:]:
        main(t)
