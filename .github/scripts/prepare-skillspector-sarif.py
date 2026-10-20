"""Export SkillSpector SARIF for GitHub without baseline-suppressed results.

GitHub ingests external suppressions as open alerts. Keep the scanner's original
report intact, and remove only accepted external suppressions from this export.
SkillSpector paths are relative to the scanned skills/ directory, whereas GitHub
requires repository-relative paths.
"""

import json
from pathlib import Path
import sys
from urllib.parse import urlsplit


def prepare(report):
    removed = 0
    for run in report["runs"]:
        active = []
        for result in run.get("results", []):
            if any(
                item.get("kind") == "external"
                and item.get("status", "accepted") == "accepted"
                for item in result.get("suppressions", [])
            ):
                removed += 1
                continue
            for location in result.get("locations", []):
                artifact = location.get("physicalLocation", {}).get("artifactLocation", {})
                uri = artifact.get("uri", "")
                if uri and not urlsplit(uri).scheme and not uri.startswith(("/", "skills/")):
                    artifact["uri"] = "skills/" + uri
            active.append(result)
        run["results"] = active
    return removed


if __name__ == "__main__":
    source, destination = map(Path, sys.argv[1:])
    if source.resolve() == destination.resolve():
        raise ValueError("Keep the original scanner report; use a separate output path")
    report = json.loads(source.read_text())
    removed = prepare(report)
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Excluded {removed} baseline-suppressed results from the GitHub export")
