"""Regression checks for the GitHub SARIF adapter (stdlib only)."""

from copy import deepcopy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "adapter", Path(__file__).with_name("prepare-skillspector-sarif.py")
)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


def finding(uri, suppressions=None):
    result = {
        "ruleId": "PE2",
        "locations": [{"physicalLocation": {"artifactLocation": {"uri": uri}}}],
    }
    if suppressions is not None:
        result["suppressions"] = suppressions
    return result


class PrepareTests(unittest.TestCase):
    def test_only_accepted_external_suppressions_are_removed(self):
        active = [
            finding("new/SKILL.md"),
            finding("rejected/SKILL.md", [{"kind": "external", "status": "rejected"}]),
            finding("pending/SKILL.md", [{"kind": "external", "status": "underReview"}]),
            finding("source/SKILL.md", [{"kind": "inSource"}]),
        ]
        suppressed = [
            finding("known/SKILL.md", [{"kind": "external"}]),
            finding("known/SKILL.md", [{"kind": "external", "status": "accepted"}]),
        ]
        report = {"runs": [{"results": deepcopy(active + suppressed)}, {"results": []}]}
        self.assertEqual(adapter.prepare(report), 2)
        self.assertEqual(len(report["runs"][0]["results"]), len(active))
        self.assertEqual(report["runs"][1]["results"], [])
        for result in report["runs"][0]["results"]:
            self.assertTrue(result["locations"][0]["physicalLocation"]["artifactLocation"]["uri"].startswith("skills/"))

    def test_existing_repository_and_absolute_uris_are_preserved(self):
        results = [finding(uri) for uri in ("skills/x/SKILL.md", "file:///tmp/SKILL.md", "https://example.com/SKILL.md", "/tmp/SKILL.md")]
        report = {"runs": [{"results": deepcopy(results)}]}
        self.assertEqual(adapter.prepare(report), 0)
        self.assertEqual(report["runs"][0]["results"], results)


if __name__ == "__main__":
    unittest.main()
