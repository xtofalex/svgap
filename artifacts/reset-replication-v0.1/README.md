# Reset-release replication artifacts v0.1

This directory contains 72 publicly redistributable generated-RTL candidates:
eight frozen tasks, three generation configurations, and three independent
calls per configuration. Each candidate bundle includes the exact prompt,
normalized RTL, portable manifest, testbench, evaluation report, generation
metadata, and content hashes. Raw provider transcripts and private blinded-case
mappings are intentionally excluded.

The reports record 57 functional passes. The reference structural oracle flags
14 of those 57 for direct raw asynchronous reset on operational state. Treat
that value as an author-confirmed lower-bound detection count, not a validated
defect rate, model ranking, or silicon-failure estimate. Synthetic reviewer
analysis is reported separately and is not a substitute for independent human
CDC/RDC adjudication.

From the repository root, replay any candidate with:

```bash
svgap check artifacts/reset-replication-v0.1/candidates/<run>/<task>/manifest.toml
```

Verify all published hashes and indexed outcomes with:

```bash
.venv/bin/python scripts/verify_public_artifacts.py
```

Generated RTL is covered by `LICENSE.generated-rtl` to the extent stated there;
the evaluator itself is Apache-2.0.
