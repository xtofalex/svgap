# Independent RTL designer review: result

Review window: 2026-07-16 to 2026-07-19. Imported 2026-07-20.

This page records the outcome of the project's single comprehensive
independent human-expert review, run under the frozen
[RTL designer review protocol](rtl-designer-review-protocol.md). The
reviewer packet was hash-locked before the review
(SHA-256 `df961c824be3f7a48ec22312e7449a9ef57b6e523107d5b6a67197925042f83e`)
and the returned files were hash-locked on receipt, before import, in
[issue #3](https://github.com/shsridhar-beep/svgap/issues/3). The returned
files are committed verbatim under `artifacts/independent-review-v0.1/`.

## Reviewer

Seshu Kumar Paravastu (named, per his attestation). Attested experience:
10 years RTL design/verification; 0 years dedicated CDC/RDC, reset, ASIC,
FPGA, or signoff experience. Commercial tools available during review
(VCS, Spyglass, Verdi); the SV-Gap checker was not used. No prior exposure
to the repository or to any packet candidate. The attestation answers
"not sure" on packet SHA-256 verification; the returned answers
structurally match the locked packet, and the returns themselves are
hash-locked.

## Controlled witness pairs: 5 of 5 supported

For every implemented rule family the reviewer judged that the safe/unsafe
pair supports the stated rule distinction, at high confidence, with
rule-specific technical reasoning. His qualifiers are as valuable as the
verdicts and are preserved verbatim in the artifact:

| Rule | Judgment | Reviewer's qualifier |
|---|---|---|
| REF-CDC-001 | Supported, high | two-stage synchronizer sufficiency is context-dependent (three stages or feedback may be required) |
| REF-CDC-002 | Supported, high | assumes co-operands are timed synchronously |
| REF-CDC-003 | Supported, high | Gray coding gives coherency, not completeness; the destination may skip values |
| REF-RDC-001 | Supported, high | judgment depends on where the reset comes from; a reset distribution tree could change the conclusion |
| REF-XPROP-001 | Supported, high | the unsafe case can also be caught by X-pessimistic simulation |

## Blinded candidates: 3 of 3 concordant with the frozen oracle

The reviewer labeled all three blinded candidates `violation` at high
confidence. All three match the frozen structural verdicts. On two
candidates the agreement extends to the root cause:

- On the candidate drawn from the frozen reset-release study, the reviewer
  independently identified the synchronizer-bypass pattern: a reset
  synchronizer is present, but the flagged register's asynchronous reset
  remains on the raw net. This is the same mechanism documented in the
  [reset-release result](reset-replication-result.md).
- On one selective-reset candidate, the reviewer identified the exact
  defect recorded in the frozen functional log (a multi-driven signal),
  down to the signal name, from source inspection alone.
- On the other selective-reset candidate, the reviewer identified the
  spec-versus-RTL contradiction on reset connectivity that the declared
  intent prohibits.

Per protocol, model and configuration identities stay in the private case
mapping and are not disclosed here.

## Repository-level answers

The reviewer's answers endorse the evidence contract's core positions in
his own words: a clean result should claim no more than "for the requested
intent, the checker found no instance of violation of the specific rule
patterns it inspects"; "CDC/RDC clean" or "no hardware issues" would be
overstated; the evaluator should return `unknown` when intent is unclear,
because assumed intent plus a bare pass is the most dangerous failure
mode; and preserving the functional result while listing answered, failed,
and unanswered production questions improves the research-to-production
handoff. He additionally names hard macros (for example SRAMs) as
structures likely to fool a small netlist recognizer, and identifies
intent the current manifest does not carry: reset source and distribution
context, MTBF targets, and tolerance for skipped values in multi-bit
crossings. Those feed the
[intent contract RFC](https://github.com/shsridhar-beep/svgap/discussions/20).

## Mid-review clarification (disclosed)

On 2026-07-18 the reviewer asked which controlled-witness folder
corresponds to which rule row in the review sheet; the packet omitted that
mapping. An indexing-only mapping was provided, with no judging guidance
and no candidate information. Details in the
[issue #3 lock comment](https://github.com/shsridhar-beep/svgap/issues/3).

## What this establishes, and what it does not

It establishes that an independent RTL engineer, reviewing blind and
without the checker, judged every controlled witness pair to demonstrate
its stated rule distinction and independently confirmed the violations in
all three blinded candidates, including the synchronizer-bypass mechanism
on a real study case.

It does not establish a defect rate, a model ranking, reviewer-population
statistics (one reviewer, three candidates, chosen for diagnostic breadth
rather than representativeness), or signoff-grade coverage. The reviewer's
attested experience profile (10 years RTL, none dedicated to CDC/RDC
signoff) is part of the record and should be weighed accordingly.
