import importlib.util
from pathlib import Path
from unittest import TestCase


ROOT = Path(__file__).resolve().parents[1]


def _load_builder():
    path = ROOT / "scripts" / "build_adoption_baseline.py"
    spec = importlib.util.spec_from_file_location("build_adoption_baseline", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ResultRegistryTests(TestCase):
    def test_registry_is_deterministic_and_current(self) -> None:
        module = _load_builder()
        first = module.build_registry()
        second = module.build_registry()
        self.assertEqual(first, second)
        self.assertEqual(
            sum(item["candidate_reports"] for item in first["generation"]), 72
        )
        self.assertEqual(
            {item["overall"] for item in first["diagnosis"]}, {"pass", "fail"}
        )
        self.assertEqual(
            {item["overall"] for item in first["repair"]}, {"pass", "fail"}
        )
