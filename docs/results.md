# Evidence profiles

SV-Gap publishes multidimensional evidence profiles, not a scalar
leaderboard. Functional failures, structural failures, unknowns, and tool
errors remain visible. Every profile is bounded by its taskpack, evaluator,
and provenance level.

## Frozen generation baseline

| Configuration | Candidates | Functional pass | Functional-pass / structural-fail |
|---|---:|---:|---:|
| `claude-opus-4-8` | 24 | 17 | 1 |
| `claude-sonnet-5` | 24 | 19 | 7 |
| `openai-frontier-a` | 24 | 21 | 6 |

## Exploratory diagnosis profiles

| Configuration | Overall | Passed checks | Total checks |
|---|---|---:|---:|
| `gpt-5.4` | `fail` | 8 | 9 |
| `openai-frontier-a` | `pass` | 9 | 9 |

## Exploratory repair profiles

| Configuration | Overall | Passed checks | Total checks |
|---|---|---:|---:|
| `gpt-5.4` | `pass` | 7 | 7 |
| `openai-frontier-a` | `fail` | 5 | 7 |

## Community submissions

No community submission has been accepted yet. The first validated
generation, diagnosis, repair, failure, or abstention profile is
welcome; see [Submit a result](submitting-results.md).

## Interpretation boundary

Profiles describe submitted digital RTL evidence under configured open-source checks. They are not silicon signoff, population estimates, or model rankings.
