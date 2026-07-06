# SV-Gap v0.3.0-alpha.6

This prerelease shortens the path from a functional pass to an interpretable
production-evidence profile.

## Evidence-first onboarding

- `svgap study quickstart` evaluates a clearly labelled, known-unsafe bundled
  fixture and creates a local evidence profile without a model adapter.
- The CLI prints the exact profile and first report to inspect before any
  submission or publication step.
- HTML profiles separate answered, failed, and unanswered production questions,
  identify useful next evidence, and preserve the claim boundary.
- First-visit documentation distinguishes fast local execution from the large
  cold container pull and gives a measured path to model integration.

## Portability and privacy

- Intermediate Yosys JSON uses candidate-relative source locations rather than
  retaining the evaluator's absolute workspace path.
- Study failures remain explicit, and an empty or failed run is not presented
  as a model result.
- Quickstart is consistently described as a workflow fixture, not a benchmark,
  baseline, model output, certification result, or safety proof.

SV-Gap remains early digital-RTL research software. Its configured evidence
profiles are not certification, a population estimate, a general model
ranking, or silicon signoff.

The version-specific archival DOI and immutable container digest will be added
after publication and independent verification.
