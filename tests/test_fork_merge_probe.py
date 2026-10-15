"""No-network unit tests for read-only fork comparison semantics."""
from pathlib import Path
import subprocess
import tempfile
import unittest

from tools.fork_merge_probe import probe


def git(root: Path, *args: str) -> str:
    r = subprocess.run(["git", *args], cwd=root, capture_output=True,
                       check=True, text=True)
    return r.stdout.strip()


class ProbeContract(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        git(self.root, "init", "-b", "main")
        git(self.root, "config", "user.email", "probe@example.invalid")
        git(self.root, "config", "user.name", "Fork Probe")
        (self.root / "common.txt").write_text("baseline\n")
        git(self.root, "add", "common.txt")
        git(self.root, "commit", "-m", "base")
        git(self.root, "branch", "upstream")

    def _commit(self, branch: str, name: str, content: str):
        git(self.root, "checkout", branch)
        (self.root / name).write_text(content)
        git(self.root, "add", name)
        git(self.root, "commit", "-m", name)

    def test_nonoverlap_merge_is_clean_and_does_not_mutate_checkout(self):
        self._commit("upstream", "upstream.txt", "new official feature\n")
        self._commit("main", "local.txt", "local override\n")
        before = git(self.root, "status", "--porcelain")
        report, _log = probe("main", "upstream", self.root)
        self.assertEqual((report["ahead"], report["behind"]), (1, 1))
        self.assertEqual(report["overlap_count"], 0)
        self.assertEqual(report["merge_tree_status"], "CLEAN")
        self.assertFalse(report["safe_to_auto_merge"])
        self.assertEqual(git(self.root, "status", "--porcelain"), before)

    def test_overlapping_change_reports_conflict_and_no_worktree_mutation(self):
        self._commit("upstream", "common.txt", "upstream change\n")
        self._commit("main", "common.txt", "local change\n")
        before = (self.root / "common.txt").read_text()
        report, _log = probe("main", "upstream", self.root)
        self.assertEqual(report["overlap_paths"], ["common.txt"])
        self.assertEqual(report["merge_tree_status"], "CONFLICTED")
        self.assertEqual((self.root / "common.txt").read_text(), before)
        self.assertEqual(git(self.root, "status", "--porcelain"), "")

    def test_identical_histories_do_not_invent_merge_progress(self):
        report, _log = probe("main", "upstream", self.root)
        self.assertEqual(report["ahead"], 0)
        self.assertEqual(report["behind"], 0)
        self.assertEqual(report["merge_tree_status"], "CLEAN")
        self.assertFalse(report["runtime_qualified"])


if __name__ == "__main__":
    unittest.main()
