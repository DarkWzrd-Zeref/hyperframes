"""The wrapper never builds a cloud, publish, lambda, or credit command."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from hf import PIN, PIN_VERSION
from hf.guard import GuardError, assert_local
from hf.local import check_cmd, doctor_cmd, render_cmd

ROOT = Path(__file__).resolve().parents[1]


class GuardTests(unittest.TestCase):
    def test_local_commands_pass(self):
        self.assertEqual(assert_local(["doctor"]), "doctor")
        self.assertEqual(assert_local(["check", "/tmp/comp"]), "check")
        self.assertEqual(
            assert_local(["render", "/tmp/comp", "--output", "out.mp4", "--fps", "30"]),
            "render",
        )

    def test_cloud_and_credit_commands_are_refused(self):
        for argv in (
            ["cloud", "render", "comp"],
            ["publish"],
            ["lambda"],
            ["credits"],
            ["render", "comp", "--cloud"],
            ["render", "comp", "--lambda=us-east-1"],
            ["render", "comp", "--publish"],
            ["heygen"],
        ):
            with self.assertRaises(GuardError):
                assert_local(argv)

    def test_built_commands_are_the_pinned_local_cli(self):
        built = [
            doctor_cmd(),
            check_cmd(Path("composition")),
            render_cmd(Path("composition"), Path("out.mp4"), 30),
        ]
        for cmd in built:
            self.assertEqual(cmd[:3], ["npx", "--yes", PIN])
            self.assertIn(cmd[3], {"doctor", "check", "render"})
            blob = " ".join(cmd).lower()
            for banned in ("cloud", "publish", "lambda", "credit", "heygen"):
                self.assertNotIn(banned, blob)

    def test_pin_matches_package_json(self):
        meta = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        self.assertEqual(meta["hyperframesPin"], PIN_VERSION)
        self.assertEqual(PIN, f"hyperframes@{PIN_VERSION}")
        self.assertNotIn("scripts", meta)

    def test_cli_refuses_without_spawning_npx(self):
        proc = subprocess.run(
            [sys.executable, "-m", "hf", "cloud", "render", "comp"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("refusing", proc.stderr.lower())
        self.assertNotIn("npx", proc.stderr)
        self.assertNotIn("npx", proc.stdout)


if __name__ == "__main__":
    unittest.main()
