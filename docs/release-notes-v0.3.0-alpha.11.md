# SV-Gap v0.3.0-alpha.11

This is the first tagged release to carry SV-Gap's three current evidence
layers together: the independent RTL designer review imported in alpha.10, the
second open structural backend merged in PR #21, and the frozen power-on
prevalence-study protocol.

The opt-in `reference-naja` backend now covers all five reference rule families,
including `REF-XPROP-001`. Install it with `pip install "svgap[naja]"`; the
default installation remains unchanged. The backend runs in-process with no
separately installed Yosys executable, but najaeda is not pure Python: it ships
platform-specific compiled wheels containing the slang frontend and SNL
netlist engine. Unsupported declared intent returns `unknown`, frontend
warnings are preserved, exact najaeda versions are recorded, and runs leave no
diagnostic files in the caller's working directory.

On the frozen 72-candidate reset-release artifact, `reference-naja` and
`reference-yosys` agree rule for rule on all 72 candidates. This is measured
compatibility on one reset-focused corpus, not independent ground truth or
signoff validation. The comparison history records the former 54/72 result and
the packed-vector synchronizer false-positive class whose correction produced
72/72 agreement. The contributor's Naja relationship and AI-assistance
disclosure are recorded in `CONTRIBUTORS.md`.

The power-on prevalence protocol was frozen before confirmatory generation. It
prespecifies balanced model-task sampling, pre-scoring output digests,
dual-backend confirmation, explicit `unknown` handling, duplicate-output
sensitivity analysis, and task-clustered uncertainty. It accepts conforming
community submissions while making no claim that a confirmatory run has
already occurred. Any resulting fraction is conditional on the declared
taskpack and configurations, not a universal defect rate or model ranking.

The release also carries the named independent review: five of five controlled
witness pairs supported and three of three blinded candidates concordant with
the frozen oracle, with the single-reviewer scope and experience profile
preserved. Together these artifacts support a reproducible research claim and
production-relevant questions; they do not claim production qualification or
silicon signoff.
