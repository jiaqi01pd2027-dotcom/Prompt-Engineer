#!/usr/bin/env python3
"""Emit the results tables for the paper from experiments/results/summary.json."""
import json, pathlib, statistics as st, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent
S = json.loads((ROOT / "experiments/results/summary.json").read_text())
NAMES = {"P0":"bare","P1":"specific","P2":"role","P3":"context","P4":"constraints",
         "P5":"format","P6":"few-shot","P7":"chain-of-thought","P8":"full stack","P9":"interview"}
PAT = [f"P{i}" for i in range(10)]
rows = S["rows"]
out = []
bp = S["by_pattern"]
out.append("**Table 1. Mean blind-judge score by prompt pattern** (0 to 10, average of five dimensions; n = runs per pattern; objective pass = share of rubric checks passed).\n")
out.append("| Pattern | n | Total | Correct | Complete | Adherence | Useful | Concise | Objective pass |")
out.append("|---|---|---|---|---|---|---|---|---|")
for p in PAT:
    v = bp[p]
    out.append(f"| {p} {NAMES[p]} | {v['n']} | **{v['mean_total']:.2f}** | {v['correctness']:.2f} | {v['completeness']:.2f} | {v['adherence']:.2f} | {v['usefulness']:.2f} | {v['concision']:.2f} | {v['objective_rate']*100:.0f}% |")
out.append("")
doms = sorted({r["domain"] for r in rows})
out.append("**Table 2. Pattern by domain** (mean total; each cell averages two tasks and three models).\n")
out.append("| Pattern | " + " | ".join(doms) + " |"); out.append("|---|" + "---|"*len(doms))
for p in PAT:
    cells = [f"{S['by_pattern_domain'].get(p+'|'+d,{}).get('mean_total',float('nan')):.2f}" for d in doms]
    out.append(f"| {p} {NAMES[p]} | " + " | ".join(cells) + " |")
out.append("")
out.append("**Table 3. Pattern by model** (mean total across all tasks).\n")
out.append("| Pattern | Fable 5.1 | Opus 5 | Sonnet 5 |"); out.append("|---|---|---|---|")
for p in PAT:
    cells = [f"{S['by_pattern_model'].get(p+'|'+m,{}).get('mean_total',float('nan')):.2f}" for m in ["fable","opus","sonnet"]]
    out.append(f"| {p} {NAMES[p]} | " + " | ".join(cells) + " |")
out.append("")
bt = collections.defaultdict(lambda: collections.defaultdict(list))
for r in rows: bt[r["task"]][r["pattern"]].append(r["total"])
out.append("**Table 4. Bare versus full stack per task** (mean over three models) and the best pattern on that task.\n")
out.append("| Task | Bare (P0) | Full stack (P8) | Gain | Best pattern |"); out.append("|---|---|---|---|---|")
for t in sorted(bt):
    m = {p: st.mean(v) for p, v in bt[t].items()}
    best = max(m, key=m.get)
    out.append(f"| {t} | {m['P0']:.2f} | {m['P8']:.2f} | +{m['P8']-m['P0']:.2f} | {best} {NAMES[best]} ({m[best]:.2f}) |")
out.append("")
(ROOT / "paper/results_tables.md").write_text("\n".join(out) + "\n")
print("\n".join(out))
