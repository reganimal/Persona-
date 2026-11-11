import io
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import quotecheck  # noqa: E402


class NormTest(unittest.TestCase):
    def test_ignores_case_punctuation_and_whitespace(self):
        self.assertEqual(quotecheck.norm("Hello,   WORLD!\n How's it?"), "hello world how's it")

    def test_curly_apostrophe_matches_straight(self):
        self.assertEqual(quotecheck.norm("you’re"), quotecheck.norm("you're"))


class MainTest(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.dir)
        (self.dir / "t1.txt").write_text("so we deal in likelihood, that is all\n", encoding="utf-8")
        (self.dir / "t2.txt").write_text("anything novel hijacks our brain\n", encoding="utf-8")

    def run_main(self, quotes):
        qfile = self.dir / "quotes.txt"
        qfile.write_text(quotes, encoding="utf-8")
        argv = ["quotecheck.py", str(qfile), str(self.dir / "t1.txt"), str(self.dir / "t2.txt")]
        out = io.StringIO()
        with mock.patch.object(sys, "argv", argv), redirect_stdout(out):
            code = quotecheck.main()
        return code, out.getvalue().splitlines()

    def test_all_found(self):
        code, lines = self.run_main("We deal in likelihood.\n\n\"Anything novel hijacks our brain.\"\n")
        self.assertEqual(code, 0)
        self.assertEqual(lines, [
            "OK   ['t1.txt'] We deal in likelihood.",
            "OK   ['t2.txt'] \"Anything novel hijacks our brain.\"",
        ])

    def test_missing_quote_fails(self):
        code, lines = self.run_main("We deal in certainty.\n")
        self.assertEqual(code, 1)
        self.assertEqual(lines, ["MISS [] We deal in certainty."])

    def test_usage_without_arguments(self):
        out = io.StringIO()
        with mock.patch.object(sys, "argv", ["quotecheck.py"]), redirect_stdout(out):
            self.assertEqual(quotecheck.main(), 2)
        self.assertIn("Usage:", out.getvalue())


if __name__ == "__main__":
    unittest.main()
