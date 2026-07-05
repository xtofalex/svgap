# Community launch kit

## One-sentence description

SV-Gap makes explicit why an AI-generated artifact can pass an offline benchmark
yet remain untrusted by production: the benchmark may neither observe nor even
represent a required production property.

## Talk demonstration

1. Run the safe and unsafe reset witnesses; both pass the same functional test.
2. Show the structural result separating them.
3. Remove reset intent and show `unknown`, not `pass`.
4. Show one public generated candidate from the reset artifact.
5. End on the handoff record: functional result + intent + structural result +
   evidence.

The point is not that one checker makes RTL production-ready. The point is that
the reason for non-adoption becomes inspectable and actionable.

## Launch post

> Frontier research teams often hand production teams an artifact plus an
> offline pass rate. Production teams need a different object: the artifact,
> declared deployment intent, layered validity results, and evidence. We built
> SV-Gap to make that mismatch executable for AI-generated RTL. The first public
> case study starts with CDC/RDC, where functional simulation can accept designs
> that differ on reset and crossing safety. We are looking for contributors who
> can add intent-bearing taskpacks, independent checker backends, and real
> research-to-production handoff cases.

## Ninety-second demo script

1. **0–15s:** “Offline benchmarks tell us whether an observed test passed. A
   production handoff needs to say which deployment questions that evidence did
   and did not answer.”
2. **15–35s:** Run `svgap demo`. Point out that both candidates pass the same
   functional oracle.
3. **35–55s:** Reveal the structural columns. One passes; one fails
   `REF-RDC-001` under declared reset-release intent.
4. **55–75s:** Show the diagnosis/repair registry: one frontier model preserves
   uncertainty but misses the repair; another repairs the finding but overclaims
   the diagnosis. Do not call this a ranking.
5. **75–90s:** “Contribute a taskpack, checker backend, benchmark adapter, model
   run, or counterexample. The goal is a reviewable evidence ecosystem, not one
   universal oracle.”

## Coordinated launch sequence

1. Publish the tagged prerelease, PyPI package, container, Pages documentation,
   and Zenodo version before announcing.
2. Pin the welcome, missing-evidence, and checker-backend discussions.
3. Publish the same visual and one-sentence claim on GitHub, LinkedIn, and the
   talk landing page; link to `svgap demo`, not to a long methodology document.
4. Invite targeted contributors to one bounded issue each: benchmark adapter,
   taskpack, checker backend, model replication, or disputed finding.
5. After 48 hours, publish a short response note: installs, reproduced results,
   questions raised, and new unknowns. Do not substitute stars for research
   evidence.

## Contribution calls

Ask specifically for:

- a second open-source structural frontend or checker backend;
- a taskpack derived from a public production-style design requirement;
- an adapter that imports results from a public RTL benchmark;
- a false positive or false negative with a minimal regression fixture; and
- a CI integration from an applied research workflow.

Do not make independent human review, a model leaderboard, or agreement with the
current oracle a condition of participation.

## Maintainer demo commands

```bash
svgap check examples/reset_release/unsafe/manifest.toml
svgap check examples/reset_release/safe/manifest.toml
svgap check examples/imported_result/manifest.toml
svgap export examples/imported_result/build/report.json \
  --sarif /tmp/svgap.sarif --html /tmp/svgap.html
make calibrate-v02
```

## Release checklist

- CI, package, container, and artifact-verification jobs pass.
- Version agrees across package metadata, runtime, changelog, tag, and notes.
- v0.2 taskpack digest matches `freeze.json`.
- The result registry is schema-valid and reproducible from checked-in reports.
- The documentation site and `svgap demo` work from a clean install.
- GitHub release is marked prerelease and includes wheels, source archive,
  schemas, taskpack archive, result archive, and checksums.
- Zenodo has ingested the tag before the DOI is advertised as that version's
  archive.
- `main` requires passing CI and disallows force pushes and deletion.
