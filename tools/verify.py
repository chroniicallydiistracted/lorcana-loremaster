#!/usr/bin/env python3
"""Run the complete local milestone validation without refreshing live policy."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    commands = [
        [sys.executable, "tools/lorcana.py", "build"],
        [sys.executable, "tools/knowledge.py", "build"],
        [sys.executable, "tools/lorcana.py", "check"],
        [sys.executable, "tools/knowledge.py", "benchmark"],
        [sys.executable, "-m", "pytest", "-q"],
        [sys.executable, "-m", "ruff", "check"],
        [sys.executable, "-m", "ruff", "format", "--check"],
    ]
    results = []
    for command in commands:
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        results.append(
            {
                "command": command[1:],
                "exit_code": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            }
        )
        print(
            " ".join(command[1:]) + ": " + ("passed" if completed.returncode == 0 else "failed"), flush=True
        )
        if completed.returncode:
            print(completed.stdout + completed.stderr)
            break
    report = {
        "passed": len(results) == len(commands) and all(r["exit_code"] == 0 for r in results),
        "checks": results,
    }
    (ROOT / "reports/milestone-verification.json").write_text(json.dumps(report, indent=2) + "\n")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
