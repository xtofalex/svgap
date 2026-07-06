# SV-Gap Harbor reset-release dataset

This adapter packages the eight frozen `reset-replication-v0.2` tasks for
Harbor. It is a distribution layer, not a new benchmark definition or results
registry. SV-Gap remains the source of the functional and structural verdicts.

Each task asks an agent to write `/app/design.sv`. The verifier evaluates that
single candidate once and publishes paired numeric Harbor rewards:

- `reward`: 1 only when both configured layers pass;
- `functional_accept`: 1 when the supplied simulation oracle passes;
- `structural_accept`: 1 when the configured structural backend passes;
- `gap_member`: 1 when functional evidence passes and structural evidence
  fails;
- `unknown`: 1 when a configured question remains unanswered; and
- `tool_error`: 1 when either evidence layer reports a tool failure.

Every task includes a safe Oracle solution and an unsafe verifier-calibration
witness. The unsafe witness is test evidence and is never installed by the
Oracle agent. The full `svgap-report.json`, `harbor-verdict.json`, candidate
RTL, and HTML evidence profile are retained as trial artifacts. A numeric
Harbor reward does not replace the four-state SV-Gap evidence record.

## Tasks

- `svgap/reset-config`
- `svgap/reset-counter`
- `svgap/reset-credits`
- `svgap/reset-events`
- `svgap/reset-fsm`
- `svgap/reset-status`
- `svgap/reset-timer`
- `svgap/reset-watchdog`

## Prerequisites

- Docker Desktop or another running Docker daemon;
- Harbor 0.17.1 or a compatible later version; and
- enough local storage for the digest-pinned SV-Gap evaluator image.

Install Harbor with:

```bash
uv tool install harbor
```

Keep job output on a host path shared with the Docker daemon. The examples use
the repository-local, ignored `.harbor-jobs` directory so Colima and Docker
Desktop can expose verifier logs back to Harbor.

For the Colima configuration used during development, prefix Harbor and Docker
commands with:

```bash
DOCKER_CONFIG=/tmp/svgap-docker-config \
DOCKER_HOST=unix://$HOME/.colima/default/docker.sock
```

## Rebuild the adapters

The adapters are generated from the frozen taskpack:

```bash
python3 integrations/harbor/build_reset_release.py
harbor sync integrations/harbor/svgap-reset-release
```

## Validate witness calibration

The calibration gate requires every safe witness to pass both layers and every
unsafe witness to pass the functional layer while failing the structural layer:

```bash
integrations/harbor/validate_reset_release_witnesses.sh
```

## Validate all Oracle solutions

From the repository root:

```bash
harbor run \
  -p integrations/harbor/svgap-reset-release \
  -a oracle \
  -o .harbor-jobs/oracle-reset-release \
  --n-concurrent 1
```

All eight tasks must receive `reward = 1`, `functional_accept = 1`, and
`structural_accept = 1`.

## Run Codex

With file-backed Codex authentication already configured on the host:

```bash
harbor run \
  -p integrations/harbor/svgap-reset-release \
  -a codex \
  -m gpt-5.5 \
  --ae CODEX_FORCE_AUTH_JSON=1 \
  -o .harbor-jobs/codex-reset-release \
  --n-concurrent 1 \
  --n-attempts 1 \
  --yes
```

Treat generated RTL as untrusted input and use an isolated evaluation host.
The first run can be slow because Harbor installs the selected agent in each
task environment.

## View and analyze results

The viewer process must inherit the Docker configuration and agent credential
selector used by any analysis job it launches:

```bash
CODEX_FORCE_AUTH_JSON=1 \
harbor view .harbor-jobs/codex-reset-release
```

Select `codex` and `gpt-5.5` when generating analysis. Analysis is optional and
consumes additional model quota. It does not affect the SV-Gap verdict.

## Create a canonical SV-Gap submission

Harbor Hub uploads are optional and informal. The SV-Gap repository remains
the canonical, claim-disciplined results record. Convert a complete Harbor job
into a normal contribution directory with:

```bash
svgap submission from-harbor \
  .harbor-jobs/codex-reset-release/JOB_TIMESTAMP \
  --dataset integrations/harbor/svgap-reset-release \
  --id codex-gpt-5.5-reset-v02-01 \
  --title "Codex gpt-5.5 reset-release generation profile" \
  --provenance-level public \
  --provider openai \
  --contributor "YOUR NAME" \
  --output results/submissions/codex-gpt-5.5-reset-v02-01
```

The importer rejects partial jobs, task digest drift, an evaluator image or
SV-Gap version that disagrees with release provenance, mixed agent
configurations, and any disagreement among the Harbor rewards, Harbor verdict,
and full SV-Gap report. The resulting directory uses the same validation and
deterministic bundle workflow as every other SV-Gap submission.

## Publication gate

Do not publish the dataset until:

1. all safe and unsafe witness pairs pass calibration;
2. all eight Oracle solutions earn 100 percent reward;
3. at least one non-Oracle Harbor agent completes all eight tasks;
4. the collected SV-Gap reports and Harbor metrics agree;
5. `unknown` and `tool_error` are verified as non-passing; and
6. task descriptions, image digest, and package version match the cited
   SV-Gap release.
