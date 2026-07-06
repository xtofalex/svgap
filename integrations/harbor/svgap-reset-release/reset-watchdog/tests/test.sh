#!/bin/bash
set -u

mkdir -p /logs/verifier
mkdir -p /logs/artifacts
rm -f /logs/verifier/reward.txt /logs/verifier/reward.json

cp /tests/manifest.toml /app/manifest.toml

if [ -s /app/design.sv ]; then
  svgap check /app/manifest.toml \
    > /logs/verifier/svgap-check.txt \
    2> /logs/verifier/svgap-check-stderr.txt
  check_status=$?
else
  check_status=4
  printf '%s\n' "candidate did not create /app/design.sv" \
    > /logs/verifier/svgap-check-stderr.txt
fi

if [ -s /app/svgap-report.json ]; then
  cp /app/svgap-report.json /logs/artifacts/svgap-report.json
  svgap export /app/svgap-report.json --html /logs/artifacts/evidence-profile.html \
    > /logs/verifier/svgap-export.txt \
    2> /logs/verifier/svgap-export-stderr.txt
fi

python3 /tests/score.py \
  --report /app/svgap-report.json \
  --reward /logs/verifier/reward.json \
  --verdict /logs/artifacts/harbor-verdict.json

printf '%s\n' "$check_status" > /logs/verifier/svgap-check-exit-code.txt
exit 0
