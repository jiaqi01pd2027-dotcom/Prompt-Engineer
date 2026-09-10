#!/usr/bin/env python3
"""Inject experiment data into the site template -> site/dist/index.html

Reads experiments/results/summary.json, the task specs (for rubrics and shared
material), and the raw outputs used on the page (hero pair, rating pairs).
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXP = ROOT / "experiments"
SITE = ROOT / "site"

NAMES = {"P0":"bare","P1":"specific","P2":"role","P3":"context","P4":"constraints",
         "P5":"format","P6":"fewshot","P7":"cot","P8":"fullstack","P9":"interview"}
TASKS = ["code-1","code-2","write-1","write-2","analysis-1","analysis-2",
         "extract-1","extract-2","reason-1","reason-2","agent-1","agent-2"]

def read(p):
    p = pathlib.Path(p)
    return p.read_text() if p.exists() else ""

def task_meta(t):
    spec = read(EXP / "tasks" / f"{t}.md")
    title = spec.splitlines()[0].lstrip("# ").strip() if spec else t
    return {"id": t, "title": title}

def output(t, model, p):
    return read(EXP / "results" / t / model / f"{p}.md").strip()

def prompt(t, p):
    return read(EXP / "prompts" / t / f"{p}.txt").strip()

summary = json.loads(read(EXP / "results" / "summary.json") or "{}")

pairs = []
for t in TASKS:
    a, b = output(t, "fable", "P0"), output(t, "fable", "P8")
    if a and b:
        pairs.append({"task": t, "title": task_meta(t)["title"],
                      "promptA": prompt(t, "P0"), "promptB": prompt(t, "P8"),
                      "A": a, "B": b})

data = {
    "names": NAMES,
    "summary": {k: v for k, v in summary.items() if k != "rows"},
    "rows": summary.get("rows", []),
    "tasks": [task_meta(t) for t in TASKS],
    "pairs": pairs,
}

tpl = read(SITE / "index.html")
out = tpl.replace("__DATA__", json.dumps(data).replace("</", "<\\/"))
(SITE / "dist").mkdir(exist_ok=True)
(SITE / "dist" / "index.html").write_text(out)
print("built", len(out)//1024, "KB;", len(pairs), "pairs;", len(data["rows"]), "scored rows")
