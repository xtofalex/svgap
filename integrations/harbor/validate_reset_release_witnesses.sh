#!/bin/bash
set -euo pipefail

root=$(cd "$(dirname "$0")/../.." && pwd)
dataset="$root/integrations/harbor/svgap-reset-release"
image="ghcr.io/shsridhar-beep/svgap@sha256:d800fe08199be70963965c7a0674c5f010f4bbc9bfdc129efce7bb95218ae621"

for task in "$dataset"/reset-*; do
  [ -d "$task/tests" ] || continue
  name=$(basename "$task")
  for variant in safe unsafe; do
    if [ "$variant" = safe ]; then
      source_path=/solution/reference-safe.sv
    else
      source_path=/tests/reference-unsafe.sv
    fi
    docker run --rm --entrypoint /bin/bash \
      -v "$task/tests:/tests:ro" \
      -v "$task/solution:/solution:ro" \
      "$image" -lc "
        set -e
        export PATH=/opt/oss-cad-suite/bin:\$PATH
        mkdir -p /app
        cp '$source_path' /app/design.sv
        cp /tests/manifest.toml /app/manifest.toml
        svgap check /app/manifest.toml >/tmp/svgap-check.txt || true
        python3 -c \"import json; r=json.load(open('/app/svgap-report.json')); assert r['functional']['status']=='pass', r; expected='pass' if '$variant'=='safe' else 'fail'; assert r['structural']['status']==expected, r; assert bool(r['gap_member']) == ('$variant'=='unsafe'), r\"
      "
    printf '%s %s: calibrated\n' "$name" "$variant"
  done
done
