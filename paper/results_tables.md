**Table 1. Mean blind-judge score by prompt pattern** (0 to 10, average of five dimensions; n = runs per pattern; objective pass = share of rubric checks passed).

| Pattern | n | Total | Correct | Complete | Adherence | Useful | Concise | Objective pass |
|---|---|---|---|---|---|---|---|---|
| P0 bare | 36 | **5.46** | 6.50 | 6.08 | 4.42 | 5.03 | 5.25 | 57% |
| P1 specific | 36 | **7.09** | 7.92 | 7.69 | 6.33 | 6.78 | 6.75 | 73% |
| P2 role | 36 | **6.94** | 7.83 | 7.97 | 5.97 | 6.61 | 6.31 | 69% |
| P3 context | 36 | **7.13** | 8.25 | 8.08 | 5.86 | 6.83 | 6.61 | 73% |
| P4 constraints | 36 | **7.88** | 8.25 | 8.33 | 7.50 | 7.58 | 7.75 | 83% |
| P5 format | 36 | **8.40** | 8.61 | 8.67 | 8.25 | 8.03 | 8.44 | 94% |
| P6 few-shot | 36 | **8.12** | 8.50 | 8.50 | 7.78 | 7.75 | 8.06 | 87% |
| P7 chain-of-thought | 36 | **6.99** | 8.53 | 8.33 | 6.14 | 6.89 | 5.06 | 74% |
| P8 full stack | 36 | **9.12** | 9.33 | 9.39 | 9.14 | 9.08 | 8.64 | 99% |
| P9 interview | 36 | **8.75** | 9.28 | 9.31 | 8.47 | 8.69 | 8.00 | 95% |

**Table 2. Pattern by domain** (mean total; each cell averages two tasks and three models).

| Pattern | agent | analysis | code | extract | reason | write |
|---|---|---|---|---|---|---|
| P0 bare | 5.13 | 6.10 | 6.67 | 1.80 | 8.30 | 4.73 |
| P1 specific | 6.87 | 6.60 | 5.47 | 9.13 | 8.60 | 5.90 |
| P2 role | 7.20 | 6.17 | 5.37 | 8.60 | 8.87 | 5.43 |
| P3 context | 6.37 | 6.70 | 5.80 | 7.70 | 8.73 | 7.47 |
| P4 constraints | 7.33 | 8.63 | 7.40 | 9.13 | 9.10 | 5.70 |
| P5 format | 8.10 | 8.13 | 9.17 | 9.43 | 8.50 | 7.07 |
| P6 few-shot | 8.40 | 8.13 | 7.43 | 8.93 | 9.40 | 6.40 |
| P7 chain-of-thought | 7.73 | 6.50 | 7.13 | 6.40 | 9.03 | 5.13 |
| P8 full stack | 8.60 | 9.13 | 9.37 | 9.53 | 9.43 | 8.63 |
| P9 interview | 7.97 | 8.77 | 8.37 | 9.47 | 9.27 | 8.67 |

**Table 3. Pattern by model** (mean total across all tasks).

| Pattern | Fable 5.1 | Opus 5 | Sonnet 5 |
|---|---|---|---|
| P0 bare | 6.07 | 5.20 | 5.10 |
| P1 specific | 7.75 | 6.68 | 6.85 |
| P2 role | 7.50 | 6.80 | 6.52 |
| P3 context | 7.35 | 7.25 | 6.78 |
| P4 constraints | 8.48 | 7.48 | 7.68 |
| P5 format | 8.52 | 8.43 | 8.25 |
| P6 few-shot | 8.17 | 7.83 | 8.35 |
| P7 chain-of-thought | 7.45 | 6.83 | 6.68 |
| P8 full stack | 9.18 | 9.05 | 9.12 |
| P9 interview | 9.00 | 8.88 | 8.37 |

**Table 4. Bare versus full stack per task** (mean over three models) and the best pattern on that task.

| Task | Bare (P0) | Full stack (P8) | Gain | Best pattern |
|---|---|---|---|---|
| agent-1 | 4.87 | 8.80 | +3.93 | P6 few-shot (8.80) |
| agent-2 | 5.40 | 8.40 | +3.00 | P9 interview (8.47) |
| analysis-1 | 5.40 | 8.80 | +3.40 | P8 full stack (8.80) |
| analysis-2 | 6.80 | 9.47 | +2.67 | P5 format (9.53) |
| code-1 | 4.40 | 8.93 | +4.53 | P8 full stack (8.93) |
| code-2 | 8.93 | 9.80 | +0.87 | P5 format (9.93) |
| extract-1 | 1.60 | 9.20 | +7.60 | P1 specific (9.47) |
| extract-2 | 2.00 | 9.87 | +7.87 | P5 format (10.00) |
| reason-1 | 8.13 | 9.60 | +1.47 | P8 full stack (9.60) |
| reason-2 | 8.47 | 9.27 | +0.80 | P9 interview (9.47) |
| write-1 | 1.93 | 8.60 | +6.67 | P8 full stack (8.60) |
| write-2 | 7.53 | 8.67 | +1.13 | P9 interview (8.73) |

