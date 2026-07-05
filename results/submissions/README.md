# Public result submissions

Each accepted contribution lives in an immutable directory named by its
`submission_id`. Create and validate a candidate directory with:

```bash
svgap submission init reports/generated/my-study/*/*/report.json \
  --id lab-a-reset-v02-01 \
  --title "Lab A reset-release generation profile" \
  --track generation \
  --configuration-label lab-a-frontier-01 \
  --provenance-level attested_alias \
  --attestor "Researcher Name" \
  --attestation "Exact checkpoint and configuration retained privately." \
  --taskpack-id reset-replication \
  --taskpack-version 0.2 \
  --contributor "Researcher Name" \
  --output results/submissions/lab-a-reset-v02-01

svgap submission validate results/submissions/lab-a-reset-v02-01 \
  --denylist /private/path/publication-denylist.txt
```

The optional denylist stays outside Git and contains one case-insensitive
regular expression per line. Use it to prevent withheld model identifiers,
internal project names, or other submission-specific strings from entering a
public bundle.

Submissions are profiles, not leaderboard rows. Anonymous case studies remain
visible but are excluded from comparative interpretation. Acceptance confirms
schema, hash, safety-scan, and scope compliance; it does not endorse a model or
upgrade the configured checker to silicon signoff.

Generation submissions take evaluator `report.json` files. Diagnosis and
repair submissions take challenge `result.json` files; their track and model
label must match the declared submission metadata.
