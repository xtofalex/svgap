import io
import shutil
from contextlib import redirect_stdout
from pathlib import Path
from unittest import TestCase, skipUnless

from svgap.cli import main


ROOT = Path(__file__).resolve().parents[1]
HAS_TOOLS = all(shutil.which(tool) for tool in ("yosys", "iverilog", "vvp"))
SAFE = str(ROOT / "examples/level_crossing/safe/manifest.toml")
UNSAFE = str(ROOT / "examples/level_crossing/unsafe/manifest.toml")


@skipUnless(HAS_TOOLS, "Yosys and Icarus Verilog are required")
class CheckFailOnTests(TestCase):
    def run_check(self, *argv: str) -> int:
        with redirect_stdout(io.StringIO()):
            return main(["check", *argv])

    def test_default_gates_on_structural_fail(self) -> None:
        self.assertEqual(self.run_check(UNSAFE), 1)
        self.assertEqual(self.run_check(SAFE), 0)

    def test_gap_gates_only_gap_members(self) -> None:
        self.assertEqual(self.run_check(UNSAFE, "--fail-on", "gap"), 1)
        self.assertEqual(self.run_check(SAFE, "--fail-on", "gap"), 0)

    def test_gap_does_not_gate_skipped_functional(self) -> None:
        # not_run functional status means the candidate cannot be a gap member
        self.assertEqual(
            self.run_check(UNSAFE, "--skip-functional", "--fail-on", "gap"), 0
        )
        # the default policy still gates on the structural fail alone
        self.assertEqual(self.run_check(UNSAFE, "--skip-functional"), 1)

    def test_report_only_always_exits_zero(self) -> None:
        self.assertEqual(self.run_check(UNSAFE, "--fail-on", "report-only"), 0)
        self.assertEqual(self.run_check(SAFE, "--fail-on", "report-only"), 0)
