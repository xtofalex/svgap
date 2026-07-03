# Reset-release replication v0.1

Run date: 2026-07-02

## Result

The locally frozen study generated 72 candidates from eight reset-sensitive tasks,
three exact model configurations, and three separate calls per model-task
cell. No candidate was repaired. Model tools were disabled.

| Outcome | Count |
|---|---:|
| Planned and generated | 72 |
| Functional pass | 57 |
| Functional compile/elaboration error | 6 |
| Functional behavioral-test fail | 9 |
| Structural pass | 57 |
| Structural fail | 15 |
| Structural tool error | 0 |
| Functional pass + structural fail | 14 |

The configured detector marked `14/57 = 24.6%` of functionally accepted,
structurally determinate candidates. This is an automated detection fraction,
not a validated defect rate: the authoring-session inspection confirmed every
flagged candidate, but no independent reviewer has yet labeled the 43 detected
passes for false negatives.

Fifteen structural-fail candidates were manually inspected. All 15 contain the
reported pattern; 14 are in the functional-pass denominator. One additional
structural failure belongs to a candidate that did not elaborate under Icarus.
This first review is recorded, but independent expert adjudication remains
required before submission.

## Blinded synthetic robustness check

Four reviewer configurations not used for candidate generation independently
labeled all 72 cases twice under secret-keyed identifiers, alongside 12 hidden
calibration controls per repeat. Seven repeat panels scored 12/12 calibration;
one scored 11/12. Exact within-configuration target agreement was 72/72 for
three configurations and 71/72 for the fourth. Nominal Krippendorff alpha over
all eight repeat panels was `0.989`.

Under the prespecified conservative consensus rule, the panel labeled 15/72
targets `yes` and 57/72 `no`, with zero unresolved. Among the 57 functional
passes, consensus was 14 `yes` and 43 `no`. This matches the reference oracle on
all 72 cases. It is a strong reproducibility check on the structural distinction,
but synthetic reviewers are not independent human CDC/RDC experts and cannot
establish false-negative recall outside this frozen taskpack. See the full
[synthetic result](synthetic-adjudication-result.md).

## Task replication

Detected cases appeared in five of eight hand-authored tasks:

| Task | Functional passes | Gap members |
|---|---:|---:|
| Counter | 9 | 6 |
| Credit counter | 9 | 3 |
| FSM | 3 | 1 |
| Status latch | 8 | 2 |
| Watchdog | 9 | 2 |
| Configuration register | 9 | 0 |
| Event counter | 9 | 0 |
| Timer | 1 | 0 |

This grouping is more informative than treating 72 calls as independent
replications. The result demonstrates recurrence across several interfaces, but
eight hand-authored tasks are not a representative population.

## Measurement caveats

Six functional nonpasses are Icarus elaboration errors on enum-valued ternary
expressions. Eight are timer-test failures. After generation, review found that
the timer prompt did not define the reset value of `expired`, while its testbench
assumed zero. The frozen result is preserved above; a transparent sensitivity
analysis excluding the whole timer task gives `14/56 = 25.0%`, leaving the
conclusion unchanged. The remaining functional failure correctly detects a
status register that does not assert reset asynchronously.

Per-model descriptive fractions range from `1/17` to `7/19`, but this study is
not powered or balanced for model ranking: functional denominators differ,
samples share tasks, and only two model vendors are represented.

## Defensible claim

> In the locally archived 72-call reset taskpack, 57 outputs passed the supplied
> Icarus testbenches, and at least 14 of those 57 contain a directly inspectable
> raw asynchronous-reset connection to ordinary operational state despite the
> prompt requesting synchronized release.

This is a taskpack-conditional lower-bound detection count. It is not an estimate
of all generated RTL, proof of silicon failure, a validated 24.6% defect rate,
or evidence that the reference oracle is signoff-grade.
