# Prior art and novelty positioning

Search date: 2026-07-02. Two structured search sweeps covered (1) the
LLM-for-RTL benchmark landscape through mid-2026, (2) the ML evaluation-science,
code-benchmark-critique, and software-test-oracle literature. This file records
what survives as novel, what must be cited, and how to word the claims.

## Novelty verdict: what survives

Across the RTL-generation benchmarks located in this search, none was found to
score CDC/RDC or reset-synchronization structural safety. Four contributions
remain plausible novelty claims and should be worded as search-bounded until
peer review:

1. **First application of CDC/RDC structural signoff-style analysis to
   LLM-generated RTL.** No prior instance found anywhere, including no
   published run of any commercial CDC tool on LLM output.
2. **First quantified reset-synchronization defect count among functionally
   passing LLM outputs.** The 14/57 lower-bound detection count has no
   published precedent of any kind.
3. **First paired safe/unsafe CDC/RDC witness corpus** where both members pass
   the same functional testbench. No public CDC/RDC pair suite exists at all,
   LLM-related or otherwise.
4. **First cross-benchmark, task-granular census of clock/reset intent and
   CDC/RDC scorability** (508 tasks, multi-clock percentage, native-scoring
   audit). Prior audits of RTL benchmarks exist, but on other axes
   (contamination, scale, broken goldens).

### The sharpest defensible thesis

The gap is **in kind, not in degree**. EvalPlus-style critiques show functional
test suites are too weak *in degree* — fixable with more tests. CDC/RDC hazards
are invisible *in kind* to RTL-level functional simulation: four-state digital
simulation does not model metastability, and reset recovery/removal violations
require timing-annotated analysis. No number of additional test vectors closes
the gap, and stronger functional oracles (formal equivalence, as in VeriThoughts
and RealBench) inherit the same blindness because they operate on the same
synchronous semantics. The property lies outside the oracle class, not
under-sampled within it.

### The deeper, fully unexplored angle: structural unidentifiability of the tasks themselves

The audit's strongest finding is not "benchmarks lack a CDC metric" but that
**most benchmark tasks lack the declared intent required for any oracle to score
structural safety** (11/508 with usable structural intent). You cannot bolt a
CDC checker onto VerilogEval: the tasks do not carry clock-group, asynchrony, or
reset-semantics declarations, so structural safety is unidentifiable from the
benchmark artifact regardless of checker strength. The fix is therefore not
another metric but **intent-carrying task contracts** (SV-Gap's manifest). This
reframing — evaluation validity limited by artifact metadata, not by oracle
effort — appears novel and is the natural standardization pitch for Si2.

Secondary novel elements worth keeping explicit:

- **Abstention-aware scoring** (`pass`/`fail`/`unknown`/`tool_error`, with
  `unknown` never counted as pass) as a first-class benchmark contract; public
  benchmarks force binary outcomes.
- The **"knows the idiom, not the obligation"** recurrence: in the pilot, every
  configuration built a two-stage reset synchronizer and still wired the raw
  asynchronous reset to operational state.

## Must-cite prior art (ranked by threat)

1. **Veri-Sure** (arXiv:2601.19747, 2026) — verified in full text to state
   "Most tasks assume a single clock domain, ignoring reset-domain reasoning and
   CDC safety" in a 9-category taxonomy of VerilogEval-v2's 156 tasks. The
   qualitative version of the audit finding, published first. Differentiate on:
   cross-benchmark breadth (508 vs 156), quantification, scorability analysis,
   and the executable oracle + witness corpus.
2. **Rethinking LLM-Based RTL Code Optimization via Timing Logic Metamorphosis**
   (ICCAD 2025, arXiv:2507.16808) — the only prior paper combining LLM
   evaluation with CDC structures (stress-tests LLM *optimizers* on
   clock-domain logic; does not check generated RTL for CDC safety).
3. **[RTLBench](https://github.com/fangzhigang32/RTLBench)** (ICCD 2025) —
   lint/readability-scored LLM RTL with synchronizer, CDC-transfer, Gray-code,
   handshake, and asynchronous-reset/synchronous-release tasks. Its public
   evaluator invokes `verilator --lint-only -Wall`; repository inspection on
   2026-07-02 found no dedicated CDC/RDC constraints, structural oracle, or
   signoff-style rule configuration. The tasks therefore narrow the novelty
   claim to structural *scoring*, rather than CDC task presence.
4. **CVDP** (arXiv:2506.14074) — its cid07 category scores Verilator lint +
   Yosys QoR. This falsifies any "benchmarks score only compilation and
   simulation" wording (see rewording below). Zero CDC/RDC content verified.
5. **CWEval** (arXiv:2501.08200), **HardSecBench** (arXiv:2601.13864), **SecV**
   (IJCAI 2025), Pearce et al. "Asleep at the Keyboard" (S&P 2022) — the
   security-domain analog: paired functional/security oracles showing
   functionally-passing-but-unsafe code. Frame SV-Gap as extending the paired-
   oracle construction to a new property class with a different mechanism
   (semantics outside the simulator, not policy outside the spec).
6. **Synthesis-in-the-Loop Evaluation** (GLSVLSI 2026, arXiv:2603.11287) — owns
   the "testbench-passing ≠ production-ready" rhetoric via synthesis QoR;
   distinguish PPA quality from silicon safety.
7. **[RTL-BenchLS](https://arxiv.org/abs/2606.08976)** (June 2026) — more than
   10,000 designs evaluated through formal equivalence over reasoning,
   completion, and repository-issue tasks. It strengthens the distinction
   between functional equivalence and CDC/RDC structural safety; it does not
   report intent-carrying CDC/RDC scoring.
8. **US Patent 9,990,453** — CDC-specific design mutations to measure
   verification robustness; nearest conceptual hardware precedent for witness
   pairs.
9. Software-engineering oracle literature — **Barr et al., "The Oracle Problem
   in Software Testing" (IEEE TSE 2015)**; **Jia & Harman mutation-testing
   survey (TSE 2011)**; **pseudo-tested methods** (Vera-Pérez et al., EMSE
   2019); the formalized **"oracle gap"** (arXiv:2309.02395). The witness-pair
   method is mutation-testing-shaped; position inside this literature or an SE
   reviewer will. Distinguish: SV-Gap pairs are functionally equivalent by
   construction with a labeled orthogonal safety property; surviving mutants
   change function.
10. ML evaluation science (for the review paper) — **D'Amour et al.,
   Underspecification (JMLR 2022)** (closest formal analogue: observational
   equivalence under the evaluation with divergent deployment behavior, at
   model level; SV-Gap is the artifact-level, mechanistically explained
   instance); **Raji et al., "Everything in the Whole Wide World Benchmark"
   (NeurIPS D&B 2021)**; **Jacobs & Wallach, "Measurement and Fairness" (FAccT
   2021)** (construct/operationalization vocabulary); **Weidinger et al.,
   "Toward an Evaluation Science for Generative AI" (arXiv:2503.05336)**;
   **Kapoor et al., "AI Agents That Matter" (TMLR 2025)** and **Rabanser et
   al., "Towards a Science of AI Agent Reliability" (arXiv:2602.16666)** for
   capability-vs-reliability; **EvalPlus (NeurIPS 2023)** and **SWE-Bench+
   (arXiv:2410.06992)** for test-suite weakness; **Eriksson et al.,
   "Can We Trust AI Benchmarks?" (arXiv:2502.06559)** as the survey of the
   critique literature.

## Terminology risks

- **"Structural observability gap"** collides with established control-theory
  usage (structural observability of networks, Lin 1974 onward). In a
  Nature-family venue this will prime the graph-theoretic meaning. Also:
  **"The Observability Gap"** (Wang & Wang, CHI 2026 workshop,
  arXiv:2603.26942) already uses the exact phrase in the LLM-coding context.
- No exact prior use of "structural validity gap" in ML/EDA evaluation was
  found (one search was filter-blocked; treat as unverified rather than clear).
- Recommendation: keep **structural validity gap** as the metric name; describe
  the phenomenon as **oracle-blind structural properties** or "structurally
  unidentifiable under the benchmark contract"; explicitly disambiguate from
  control-theoretic structural observability if the term is retained anywhere.

## Required claim rewordings

- Avoid: "benchmarks score only compilation + functional simulation" (falsified
  by CVDP cid07 lint/QoR, TuRTLe/GenBen PPA, VeriThoughts/RealBench formal
  equivalence, RTLBench lint/style, HardSecBench security).
- Safe form: *"Existing benchmarks score compile/synthesis, sampled or formal
  functional equivalence, lint/style, PPA, and security policy; none scores
  CDC/RDC or reset-synchronization structural safety, and few tasks carry the
  declared intent required to do so."*
- Avoid: "first to audit RTL benchmarks" (prior audits exist on other axes).
  Safe: "first cross-benchmark task-level census of clock/reset-domain
  properties and CDC/RDC scorability."
- The technical-note abstract now uses the safe form above.

## Software-test oracle positioning

SV-Gap is mutation-testing-shaped but not conventional mutation testing. A
surviving software mutant normally approximates a functional test-suite
weakness: the program's behavior changed and the tests missed it. Here, each
paired witness is deliberately equivalent under the supplied functional oracle
while carrying an independently declared structural-safety label. The oracle is
therefore incomplete across *property classes*, not merely sparse in input
coverage. Barr et al.'s oracle-problem framing supplies the general vocabulary;
Jia and Harman supply the mutation-testing comparison; the key distinction is
that CDC/RDC validity requires intent plus a structural oracle.

## June 2026 search update

A targeted May–June 2026 arXiv sweep found RTL-BenchLS (formal-equivalence
evaluation at much larger scale), LLM4RTL (tool-assisted generation and data
refinement), and VHDLSuite (executable VHDL validation). None of their abstracts
or available evaluation descriptions reports CDC/RDC or reset-release
structural scoring. Indexing lag remains possible, so this is evidence for a
bounded prior-art statement, not proof of global priority.

## Venue positioning

**DAC (conversations).** Lead with the concrete artifact: paired witnesses that
pass identical testbenches, and the 14/57 author-confirmed lower bound. The
one-breath version: *"Functional pass is non-identifying for silicon safety —
and 497 of 508 public benchmark tasks can't even express the question, because
they don't carry clock/reset intent."* Since CVDP is an NVIDIA benchmark, frame
the audit as constructive: CVDP is the only suite with any multi-clock tasks
and the natural first home for intent manifests.

**Si2 talk (evals/benchmarking critique).** Two hooks. (1) The
unidentifiability reframe: the missing piece is not another checker but a
standardized intent contract (clock groups, reset semantics, crossing intent)
attached to benchmark tasks — a standards problem, which is Si2's mandate and
directly relevant to its LLM Benchmarking Coalition. (2) The claim-discipline
story: pass/fail/unknown/tool_error, lower-bound detection counts vs defect
rates, blinded adjudication, frozen taskpacks — a worked example of what honest
eval claims look like in EDA.

**Nature Machine Intelligence review.** Follow `review-case-study.md`: SV-Gap
is a compact boxed example, not primary evidence; use the conceptual witness
result without 14/57 until independent adjudication locks. Write the box in
construct-validity vocabulary (Jacobs & Wallach; Raji et al.) and position
against D'Amour underspecification as the artifact-level analogue. The
research-to-production thesis the example serves: production signoff consumes
declared intent that research benchmarks never carry, so offline metrics leave
deployment-relevant properties unmeasured *and unmeasurable* — layered oracles
plus intent-carrying evaluation contracts are the remedy.

## Pre-publication checklist (novelty-specific, beyond release-readiness.md)

- [x] Cite and distinguish Veri-Sure, Timing Logic Metamorphosis, RTLBench,
      CWEval/HardSecBench, Synthesis-in-the-Loop.
- [x] Inspect RTLBench's public Verilator lint command and rule configuration.
- [x] Reword the "only compilation + simulation" phrasing everywhere it appears.
- [x] Decide the term (keep "structural validity gap"; disambiguate or drop
      "observability").
- [x] Add the SE oracle-problem/mutation-testing positioning paragraph.
- [x] Re-run a search for May–June 2026 arXiv postings before submission
      (indexing lag).
