# Generated artifact release policy

Normalized generated RTL may be published with SV-Gap. Raw provider transcripts
are excluded by default. Each released candidate bundle must contain its prompt,
task metadata, testbench, normalized RTL, portable manifest, normalized report,
generation metadata, and content hashes.

Model-labeled candidate bundles must not be published until independent blinded
review labels are locked, because reviewers could otherwise match packet RTL to
model identities. Before release, record the account context and confirm that
the person or organization releasing the outputs has authority to apply the
artifact license. Provider names describe provenance and do not imply
endorsement.

Build the release candidate locally with:

```bash
.venv/bin/python scripts/export_public_artifacts.py
```

The staging directory is excluded from Git until review lock and a final secret,
personal-path, and license scan are complete.

For the first public snapshot, "review lock" means completion of the blinded
four-configuration, two-repeat synthetic panel before generation identities are
published. That sequencing protects the recorded synthetic labels from identity
leakage; it does not satisfy the separate requirement for independent human
CDC/RDC expert adjudication of a claim-bearing defect rate.
