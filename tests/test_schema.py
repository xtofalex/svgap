from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import shutil
from unittest import TestCase, skipUnless

from jsonschema import Draft202012Validator, FormatChecker

from svgap.cli import check


ROOT = Path(__file__).resolve().parents[1]
HAS_TOOLS = all(shutil.which(tool) for tool in ("yosys", "iverilog", "vvp"))


@skipUnless(HAS_TOOLS, "Yosys and Icarus Verilog are required")
class SchemaTests(TestCase):
    def test_all_controlled_reports_validate(self) -> None:
        schema = json.loads((ROOT / "schemas/report-v1.json").read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        manifests = sorted(ROOT.glob("examples/*/*/manifest.toml"))
        self.assertEqual(len(manifests), 8)
        for path in manifests:
            with self.subTest(manifest=path):
                with redirect_stdout(io.StringIO()):
                    exit_code = check(path, False, False)
                self.assertIn(exit_code, (0, 1))
        reports = sorted(ROOT.glob("examples/*/*/build/report.json"))
        self.assertEqual(len(reports), 8)
        for path in reports:
            with self.subTest(path=path):
                validator.validate(json.loads(path.read_text(encoding="utf-8")))
