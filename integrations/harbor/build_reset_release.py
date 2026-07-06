#!/usr/bin/env python3
from __future__ import annotations

import shutil
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = ROOT / "taskpacks" / "reset-replication-v0.2" / "tasks"
DATASET_ROOT = ROOT / "integrations" / "harbor" / "svgap-reset-release"
TEMPLATE_TASK = DATASET_ROOT / "reset-counter"
IMAGE = (
    "ghcr.io/shsridhar-beep/svgap@"
    "sha256:d800fe08199be70963965c7a0674c5f010f4bbc9bfdc129efce7bb95218ae621"
)


def main() -> int:
    shared = {
        "score.py": (TEMPLATE_TASK / "tests" / "score.py").read_text(),
        "test.sh": (TEMPLATE_TASK / "tests" / "test.sh").read_text(),
    }
    for source in sorted(path for path in SOURCE_ROOT.iterdir() if path.is_dir()):
        generate_task(source, shared)
    return 0


def generate_task(source: Path, shared: dict[str, str]) -> None:
    source_config = tomllib.loads((source / "task.toml").read_text())
    source_id = str(source_config["id"])
    harbor_id = source_id.replace("_", "-")
    target = DATASET_ROOT / harbor_id
    tests = target / "tests"
    solution = target / "solution"
    environment = target / "environment"
    for directory in (tests, solution, environment):
        directory.mkdir(parents=True, exist_ok=True)

    prompt = (source / "prompt.md").read_text().rstrip()
    instruction = (
        f"{prompt}\n\n"
        "Write the complete module to `/app/design.sv`. Do not create or modify "
        "other files.\n"
    )
    (target / "instruction.md").write_text(instruction)
    (target / "README.md").write_text(
        f"# svgap/{harbor_id}\n\n"
        "Generate one SystemVerilog design, then evaluate functional acceptance "
        "and the declared synchronous reset-release requirement on the same "
        "artifact.\n"
    )
    (target / "task.toml").write_text(task_toml(source_id, harbor_id))
    (environment / "Dockerfile").write_text(dockerfile())
    (solution / "solve.sh").write_text(solve_script())
    shutil.copyfile(source / "reference-safe.sv", solution / "reference-safe.sv")
    shutil.copyfile(source / "reference-unsafe.sv", tests / "reference-unsafe.sv")
    shutil.copyfile(source / "tb.sv", tests / "tb.sv")
    (tests / "manifest.toml").write_text(manifest_toml(source_config))
    (tests / "score.py").write_text(shared["score.py"])
    (tests / "test.sh").write_text(shared["test.sh"])
    (solution / "solve.sh").chmod(0o755)
    (tests / "test.sh").chmod(0o755)
    (tests / "score.py").chmod(0o755)


def task_toml(source_id: str, harbor_id: str) -> str:
    return f'''schema_version = "1.3"
artifacts = [
  {{ source = "/app/design.sv", destination = "design.sv" }},
]

[task]
name = "svgap/{harbor_id}"
description = "Generate reset-safe RTL and expose paired functional and structural evidence."
keywords = ["systemverilog", "rtl", "reset", "rdc", "structural-validity"]
[[task.authors]]
name = "Shraddha Sridhar"
email = "shsridhar@nvidia.com"

[metadata]
source = "SV-Gap"
source_taskpack = "reset-replication-v0.2"
source_task = "{source_id}"
svgap_version = "0.3.0a6"
category = "hardware-evaluation"
difficulty = "focused"

[verifier]
timeout_sec = 180.0
network_mode = "no-network"

[verifier.env]

[agent]
timeout_sec = 900.0
network_mode = "public"

[environment]
network_mode = "public"
build_timeout_sec = 900.0
os = "linux"
cpus = 2
memory_mb = 4096
storage_mb = 10240
gpus = 0
mcp_servers = []

[environment.env]

[solution.env]
'''


def manifest_toml(config: dict[str, object]) -> str:
    candidate_id = str(config["id"]).replace("_", "-")
    clocks = "".join(
        "[[intent.clocks]]\n"
        f'name = "{clock["name"]}"\n'
        f'port = "{clock["port"]}"\n\n'
        for clock in config["clocks"]
    )
    resets = "".join(
        "[[intent.resets]]\n"
        f'name = "{reset["name"]}"\n'
        f'port = "{reset["port"]}"\n'
        f'active = "{reset["active"]}"\n'
        f'assertion = "{reset["assertion"]}"\n'
        f'deassertion = "{reset["deassertion"]}"\n\n'
        for reset in config["resets"]
    )
    groups = ", ".join(f'"{group}"' for group in config["asynchronous_groups"])
    return f'''schema_version = "1.0"
candidate_id = "harbor-{candidate_id}"

[design]
top = "{config["top"]}"
sources = ["design.sv"]

[functional]
commands = [
  ["iverilog", "-g2012", "-o", "${{SVGAP_BUILD}}/sim.vvp", "design.sv", "/tests/tb.sv"],
  ["vvp", "${{SVGAP_BUILD}}/sim.vvp"],
]

[structural]
backend = "reference-yosys"

[intent]
asynchronous_groups = [{groups}]

{clocks}{resets}[output]
report = "svgap-report.json"
'''


def dockerfile() -> str:
    return f'''FROM {IMAGE}

# Harbor supplies its own keepalive command. Clear the SV-Gap CLI entrypoint so
# the container can accept that command and later execute agent and verifier
# processes normally.
ENTRYPOINT []
CMD ["/bin/sh"]
WORKDIR /app
'''


def solve_script() -> str:
    return '''#!/bin/bash
set -eu
install -m 0644 /solution/reference-safe.sv /app/design.sv
'''


if __name__ == "__main__":
    raise SystemExit(main())
