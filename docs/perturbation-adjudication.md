# Perturbation adjudication

Status: design, not yet implemented. Target: reset-release (`REF-RDC-001`) first.

## Purpose

Independent human adjudication validates the structural oracle's findings on
generated candidates. This document specifies a machine adjudicator that
produces per-candidate executable evidence instead of expert labels: for each
flagged candidate, a reproducible seed under which the functionally accepted
design misbehaves once reset-release timing nondeterminism is modeled.

It upgrades "author-confirmed detection" to "machine-demonstrated hazard under
a declared perturbation semantics." It does not eliminate human review; it
shrinks the human role to a small blinded sample audit and to failure modes the
model cannot observe (task-intent errors, output-unobservable state).

## Semantic model: reset-release skew

When an asynchronous reset deasserts near an active clock edge, each
asynchronously reset flop independently resolves whether it observed the
release before or after that edge. The model:

- Reset **assertion** is never perturbed. Asynchronous assertion is the
  declared-safe direction.
- At reset **deassertion**, each asynchronously reset flop `i` observes the
  release either at clock edge `k` or `k+1`, selected by one seed bit `b_i`.
- Skew is bounded to one destination-clock cycle per flop. This is a
  two-valued abstraction of recovery/removal resolution, comparable to
  commercial metastability-injection simulation modes. It does not model
  analog resolution, intermediate voltages, or multi-cycle settling.

A design with a synchronized release path tolerates this by construction: the
skew is absorbed by the reset synchronizer's own flops, shifting the internal
release globally by at most one cycle. A design with raw asynchronous reset on
operational state can come out of reset with internally inconsistent state that
no global time shift explains.

## Instrumentation

1. Elaborate the candidate with the existing reference-oracle Yosys flow
   (`proc; opt_clean; write_json`).
2. Identify every `$adff`/`$adffe`/`$sr`-class cell whose ARST cone traces to
   the manifest-declared external reset (same tracing as `REF-RDC-001`).
3. Rewrite the netlist JSON: replace each such cell's ARST input with a
   per-flop skewed release signal — deassertion extended by one cycle of that
   flop's own clock when `b_i` is set. No flop is exempt; synchronizer stages
   are injected too, because tolerating stage-level skew is exactly the safety
   property under test.
4. Emit instrumented Verilog with `write_verilog`. The functional testbench is
   unchanged.

Candidates that fail elaboration or netlist simulation are reported
`inconclusive`, never as adjudicated passes.

## Seeds and determinism

Seed `s` expands to the bit vector `b` via a PRNG keyed by
`(taskpack digest, case digest, s)`. Seed 0 is all-zeros and defines the golden
run. The seed budget `N` (default 256) and the early-stop-on-divergence policy
are frozen before the run. No wall-clock or nondeterministic inputs.

## Observer and verdicts

For each seed, sample all module outputs each destination-clock cycle,
beginning at external deassertion. A seed **diverges** when there is no global
shift `δ ∈ [0, S]` (S = declared synchronizer depth + 1) under which the
post-release output trace equals the golden trace. Shift tolerance is required
because a correct synchronized-release design legitimately shifts its entire
release by up to one internal cycle under stage-level skew; inconsistent
per-bit state cannot be repaired by any global shift.

The supplied functional testbench verdict is recorded as a secondary signal
only; the trace comparison is the adjudication observer, because testbench
checks may not observe the divergent state.

Per-candidate verdicts:

- `hazard_demonstrated`: at least one seed diverges. Store the seed, first
  divergent cycle, and signal — a minimal reproducer.
- `no_divergence_observed`: N seeds, no divergence. **Not** a safety claim.
- `inconclusive`: instrumentation or simulation failure.

## Calibration gate

Before any generated candidate is adjudicated, the adjudicator must, on the
controlled reset-release witnesses:

1. produce `hazard_demonstrated` on the unsafe member, and
2. produce `no_divergence_observed` on the safe member across the full seed
   budget.

A gate failure blocks use and is a bug in the adjudicator or its semantics,
never evidence about candidates. The gate is a CI test.

## Claim discipline

- `hazard_demonstrated` is conclusive that the accepted design misbehaves
  under the declared perturbation semantics. It is not a silicon failure
  probability.
- `no_divergence_observed` is bounded by the seed budget, the testbench
  stimulus window, and output observability. A raw-reset flop whose state
  never reaches an output within the stimulus window cannot diverge visibly.
  Therefore machine adjudication can confirm flagged candidates and can expose
  false negatives, but cannot certify detected passes as safe.
- The residual assurance on detected passes comes from (a) an independent
  second structural implementation (N-version cross-check) and (b) a blinded
  human sample audit (recommended ≥ 12 cases), replacing full-case human
  labeling.
- Language after adjudication: "machine-demonstrated under a declared
  perturbation model, sample-audited by independent reviewers" — not
  "validated defect rate" unless the human sample audit and cross-check agree.

## Generalization (not v0)

Each rule family needs its own perturbation semantics, and the semantic burden
differs sharply by family:

- **Power-on X (`REF-XPROP-001`):** randomize the power-on value of every
  un-reset state element per seed. A one-shot perturbation with the same
  golden-trace observer as reset release. Cheapest generalization.
- **Single-bit CDC (`REF-CDC-001`):** randomize destination capture latency by
  one cycle *at every source transition*, not once. The global-shift observer
  is no longer sound — each transition shifts independently — so divergence
  must be defined against the set of traces reachable under legitimate
  per-transition timing choices. This is the semantics used by commercial
  metastability-injection simulation; an open equivalent is design work, not
  a parameter change.
- **Multi-bit CDC (`REF-CDC-003`):** per-bit independent draws on top of the
  single-bit semantics. Gray coding tolerates them by construction; binary
  buses do not. Cheap once single-bit semantics exist.
- **Combinational crossings (`REF-CDC-002`):** the hazard is glitch capture,
  which delta-cycle simulation does not represent at all. Requires modeling
  transient intermediate values of the combinational cone under partial input
  arrival. The heaviest model and the hardest to defend; lowest priority.
- **Synchronizer depth (`REF-META-001`):** not injection-adjudicable in
  principle. Depth adequacy is a probabilistic settling property; a two-valued
  one-cycle skew model cannot distinguish a two-stage from a three-stage
  chain. This family stays parametric permanently.

v0 is reset-release only, because that is the category with a pending
adjudication obligation; power-on randomization follows as the second target.

## Adjudication classes

The evaluation contract requires every structural rule to declare how its
findings can be adjudicated. Three classes exist:

| Class | Meaning | Rules |
|---|---|---|
| Demonstrable, semantics specified | Findings have a proposed executable counterexample model, not yet implemented | `REF-RDC-001`; `REF-XPROP-001` planned |
| Demonstrable, pending semantics | An executable hazard semantics is definable but not yet built | `REF-CDC-001`, `REF-CDC-002`, `REF-CDC-003` |
| Parametric only | No digital perturbation model can demonstrate the hazard; the rule checks declared intent | `REF-META-001` |

A rule's class is part of its public definition. Findings from
parametric-only rules are never described as demonstrated hazards, and
pending-semantics rules retain expert adjudication obligations until their
perturbation semantics are implemented and calibration-gated.

## Prior art and patent boundary

Dynamic metastability-effect injection exists commercially (Questa CDC-FX and
its 0-In lineage, JasperGold MSI, Synopsys dynamic CDC jitter, Aldec
ALINT-PRO dynamic testbenches). No open-source dynamic implementation is
known from the bounded project search; open tools located so far cover static
structural checking only. The technique family has relevant patents (e.g., US
7,356,789 metastability-effects simulation; US 7,289,946
random flip-flop delay methodology; US 11,907,631 RDC jitter). The open-source
release review must include a patent assessment before implementing or
distributing the adjudicator; this document specifies research semantics, not
legal advice or a freedom-to-operate conclusion.

## Limitations

- Two-valued skew abstraction; no analog metastability, no X-state modeling.
- Netlist-level simulation may differ from source-level simulation for
  constructs Yosys transforms; the calibration gate and the golden run share
  the instrumented netlist to keep comparisons internal.
- Divergence detection is limited to declared module outputs.
- The perturbation model itself is part of the trusted base; it is published,
  versioned, and cited in every report it adjudicates.
