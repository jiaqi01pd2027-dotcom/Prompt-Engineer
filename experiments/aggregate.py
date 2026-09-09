#!/usr/bin/env python3
"""Merge judge scores with keys across tasks -> results/summary.json + summary.md"""
import json, pathlib, statistics as st, collections

ROOT = pathlib.Path(__file__).parent
DIMS = ["correctness", "completeness", "adherence", "usefulness", "concision"]
NAMES = {"P0":"bare","P1":"specific","P2":"role","P3":"context","P4":"constraints",
         "P5":"format","P6":"fewshot","P7":"cot","P8":"fullstack","P9":"interview"}
DOMAIN = lambda t: t.split("-")[0]

rows = []
for jd in sorted((ROOT/"judge").glob("*/scores.json")):
    task = jd.parent.name
    key = json.loads((jd.parent/"key.json").read_text())
    sc = json.loads(jd.read_text())
    for oid, meta in key.items():
        s = sc.get(oid)
        if not s: continue
        total = sum(s[d] for d in DIMS) / len(DIMS)
        obj = s.get("objective") or {}
        objrate = (sum(1 for v in obj.values() if v is True) / len(obj)) if obj else None
        rows.append({"task": task, "domain": DOMAIN(task), **meta, "total": round(total,2),
                     **{d: s[d] for d in DIMS}, "objective_rate": objrate, "notes": s.get("notes","")})

def group(keyf):
    g = collections.defaultdict(list)
    for r in rows: g[keyf(r)].append(r)
    out = {}
    for k, rs in g.items():
        out[k] = {"n": len(rs), "mean_total": round(st.mean(r["total"] for r in rs),2),
                  **{d: round(st.mean(r[d] for r in rs),2) for d in DIMS},
                  "objective_rate": round(st.mean(r["objective_rate"] for r in rs if r["objective_rate"] is not None),2)
                     if any(r["objective_rate"] is not None for r in rs) else None}
    return out

summary = {
  "n_runs": len(rows),
  "by_pattern": group(lambda r: r["pattern"]),
  "by_model": group(lambda r: r["model"]),
  "by_domain": group(lambda r: r["domain"]),
  "by_pattern_model": group(lambda r: f'{r["pattern"]}|{r["model"]}'),
  "by_pattern_domain": group(lambda r: f'{r["pattern"]}|{r["domain"]}'),
  "by_task_pattern": group(lambda r: f'{r["task"]}|{r["pattern"]}'),
  "rows": rows,
}
(ROOT/"results"/"summary.json").write_text(json.dumps(summary, indent=1))

lines = [f"# Results summary ({len(rows)} scored runs)\n", "## By pattern (mean of 5 dims, 0-10)\n",
         "| pattern | name | n | total | corr | compl | adher | useful | concise | obj pass |", "|---|---|---|---|---|---|---|---|---|---|"]
for p in sorted(summary["by_pattern"]):
    v = summary["by_pattern"][p]
    lines.append(f"| {p} | {NAMES[p]} | {v['n']} | {v['mean_total']} | {v['correctness']} | {v['completeness']} | {v['adherence']} | {v['usefulness']} | {v['concision']} | {v['objective_rate']} |")
lines += ["\n## By model\n", "| model | n | total | corr | compl | adher | useful | concise |", "|---|---|---|---|---|---|---|---|"]
for m, v in summary["by_model"].items():
    lines.append(f"| {m} | {v['n']} | {v['mean_total']} | {v['correctness']} | {v['completeness']} | {v['adherence']} | {v['usefulness']} | {v['concision']} |")
lines += ["\n## Pattern x domain (mean total)\n"]
doms = sorted({r["domain"] for r in rows})
lines.append("| pattern | " + " | ".join(doms) + " |"); lines.append("|---|" + "---|"*len(doms))
for p in sorted(NAMES):
    cells = [str(summary["by_pattern_domain"].get(f"{p}|{d}", {}).get("mean_total","")) for d in doms]
    lines.append(f"| {p} {NAMES[p]} | " + " | ".join(cells) + " |")
lines += ["\n## Pattern x model (mean total)\n", "| pattern | fable | opus | sonnet |", "|---|---|---|---|"]
for p in sorted(NAMES):
    cells = [str(summary["by_pattern_model"].get(f"{p}|{m}", {}).get("mean_total","")) for m in ["fable","opus","sonnet"]]
    lines.append(f"| {p} {NAMES[p]} | " + " | ".join(cells) + " |")
(ROOT/"results"/"summary.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
