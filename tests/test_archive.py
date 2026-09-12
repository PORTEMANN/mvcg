#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.archive import read_traces  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402


class TestArchive(unittest.TestCase):
    def test_append_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "traces.jsonl"
            run_registers(archive=p)
            n1 = len(read_traces(p))
            run_registers(archive=p)
            n2 = len(read_traces(p))
            self.assertGreater(n1, 0)
            self.assertEqual(n2, 2 * n1)
            row = read_traces(p)[0]
            self.assertIn("trace_sha256", row)
            self.assertIn("verdict", row)


if __name__ == "__main__":
    unittest.main(verbosity=2)
