from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "chatdev_factory_scout.py"
SPEC = importlib.util.spec_from_file_location("chatdev_factory_scout", MODULE_PATH)
assert SPEC and SPEC.loader
scout = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = scout
SPEC.loader.exec_module(scout)


class FactoryScoutTests(unittest.TestCase):
    def _manifest(self, root: Path) -> Path:
        path = root / "portfolio.json"
        path.write_text(json.dumps({
            "schema": "kilo.chatdev.game-portfolio/v1",
            "projects": [{
                "id": "demo", "repo": "KiloMusician/demo", "engine": "python",
                "local_candidates": [str(root / "demo")],
                "native_checks": ["python -m unittest"], "chatdev_roles": ["tester"]
            }]
        }), encoding="utf-8")
        return path

    def test_manifest_rejects_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "bad.json"
            path.write_text(json.dumps({
                "schema": "kilo.chatdev.game-portfolio/v1",
                "projects": [{"id": "x", "repo": "a/b"}, {"id": "x", "repo": "a/c"}]
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                scout.load_manifest(path)

    def test_tool_detection_is_observational(self):
        def fake_which(name: str):
            return f"/bin/{name}" if name in {"git", "python"} else None
        report = scout.detect_tools(which=fake_which)
        self.assertTrue(report["source"]["git"]["detected"])
        self.assertTrue(report["python"]["python"]["detected"])
        self.assertFalse(report["agents"]["claude"]["detected"])

    def test_local_project_contracts_are_reported(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            demo = root / "demo"
            demo.mkdir()
            (demo / "pyproject.toml").write_text("", encoding="utf-8")
            (demo / "AGENTS.md").write_text("", encoding="utf-8")
            manifest = self._manifest(root)
            with mock.patch.object(scout, "detect_tools", return_value={}):
                report = scout.build_report(manifest)
            project = report["projects"][0]
            self.assertTrue(project["local"]["detected"])
            self.assertEqual({item["kind"] for item in project["contracts"]}, {"python", "agent_guidance"})
            self.assertFalse(report["authority_granted"])

    def test_missing_local_project_stays_unknown_not_absent(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifest = self._manifest(root)
            with mock.patch.object(scout, "detect_tools", return_value={}):
                report = scout.build_report(manifest)
            self.assertFalse(report["projects"][0]["local"]["detected"])
            self.assertIn("not detected on this host != absent from the fleet", report["notes"])

    def test_env_path_wins_when_present(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            candidate = root / "special"
            candidate.mkdir()
            project = {"id": "demo", "repo": "a/b", "path_env": "DEMO_PROJECT_ROOT",
                       "local_candidates": [str(root / "other")]}
            with mock.patch.dict(os.environ, {"DEMO_PROJECT_ROOT": str(candidate)}):
                resolved, checked = scout.resolve_project_path(project)
            self.assertEqual(resolved, candidate)
            self.assertEqual(checked, [str(candidate)])


if __name__ == "__main__":
    unittest.main()
