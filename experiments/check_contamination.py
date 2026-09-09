#!/usr/bin/env python3
"""Flag outputs that show signs of having seen the harness. Usage: check_contamination.py <task> ..."""
import pathlib, re, sys
ROOT = pathlib.Path(__file__).parent
PAT = re.compile(r"experiment|rubric|fixture|hidden|Prompt Engineer/|experiments/|P[0-9] (bare|specific|role|context|constraints|format|fewshot|cot|fullstack|interview)", re.I)
bad = 0
for task in sys.argv[1:]:
    for f in sorted((ROOT/"results"/task).glob("*/P*.md")):
        hits = sorted(set(m.group(0).lower() for m in PAT.finditer(f.read_text())))
        if hits:
            bad += 1; print("CONTAMINATED", f.relative_to(ROOT), hits)
print("contaminated:", bad)
