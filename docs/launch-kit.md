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
> that differ on reset and crossing safety. If you build or review AI-generated
> RTL, share one public, non-confidential production question your current
> functional evaluation does not answer. No code or internal RTL is required.

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
5. **75–90s:** “Tell us one production question your functional result leaves
   unanswered. We will turn the smallest public version into an evidence profile
   or tell you what SV-Gap cannot yet measure.”

## Coordinated launch sequence

1. Publish the tagged prerelease, PyPI package, container, Pages documentation,
   and Zenodo version before announcing.
2. Pin the welcome, missing-evidence, and checker-backend discussions.
3. Publish the same visual and one-sentence claim on GitHub, LinkedIn, and the
   talk landing page; link to `svgap demo`, not to a long methodology document.
4. Follow each relevant connection with one role-specific question and the
   collaboration intake. Ask for a code contribution only after the question
   has been scoped.
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

## Connection follow-up

Do not send a generic repository link after someone connects. Use one question
that lets the recipient contribute expertise without exposing internal work.

For a model or capability researcher:

> Thanks for connecting. I am testing a narrow question: when generated RTL
> passes its functional test, which production-review questions are still
> unanswered? If you have a model harness, the smallest replication is one
> packaged task and produces a shareable evidence profile. Would a 30-minute
> research scoping call be useful? I will turn it into a one-page experiment
> contract before asking you to run or contribute anything.

For an RTL or verification practitioner:

> Thanks for connecting. I am collecting public, sanitized examples of one
> thing a passing RTL testbench does not establish for downstream review. No RTL
> or company details are needed. What is the first question your team would
> still ask before trusting the handoff?

For a chip-design AI builder:

> Thanks for connecting. SV-Gap now accepts an existing model output and
> functional result, then reports answered, failed, and unknown production
> questions. I would value one hard integration constraint from your workflow.
> If it fits the public scope, I can map it to the smallest experiment within two
> working days.

Send the collaboration-intake link only after the question, so the recipient
knows exactly why opening it is worth their time.

Track conversions as: substantive reply, intake opened, smoke profile produced,
and follow-on experiment agreed. Connections, page views, stars, and clones are
attention signals rather than conversions.

## Research-call agenda

1. **0–5 minutes:** What capability or handoff decision matters to the
   researcher?
2. **5–15 minutes:** What does the existing functional evaluation establish,
   and what production question remains unanswered?
3. **15–22 minutes:** Can a public or synthetic artifact represent the problem,
   and which SV-Gap track fits?
4. **22–27 minutes:** Agree on the smallest publishable evidence unit and its
   claim boundary.
5. **27–30 minutes:** Assign one next action each and choose go, revise, or stop.

Send a draft
[experiment contract](experiment-contract-template.md) within two working days.
Do not ask for a broad integration, public endorsement, or contributor listing
at the end of the first call.

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
