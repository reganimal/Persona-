import io
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import checkpersona  # noqa: E402

PROFILE = """# Ada — Research Dossier

## 4. Frameworks
Ada says "small steps compound into big results" ✅ [S1]. Also [S2].
She adds: "start before you feel ready, then adjust as you go" [S1].

## 9. Sources
- **[S1]** Interview — https://example.com/1
- **[S2]** Book — https://example.com/2
"""

PROMPT = """# Ada

## Verified lines you may quote (attribute them to Ada)
- "Small steps compound into big results."
- "Start before you feel ready… adjust as you go."

## Hard boundaries
- "This line is not a quote check target at all."
"""

AGENT = """---
name: ada
description: Advisor modeled on Ada.
---

Read `personas/ada/system-prompt.md` first.
"""

README = "| **Ada** | Ada | Things | [`personas/ada/`](personas/ada/) |\n"


class CheckPersonaTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)
        self.write("personas/ada/profile.md", PROFILE)
        self.write("personas/ada/system-prompt.md", PROMPT)
        self.write("personas/_template/profile.md", "## 9. Sources\n")
        self.write(".claude/agents/ada.md", AGENT)
        self.write("README.md", README)

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def edit(self, rel, old, new):
        path = self.root / rel
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding="utf-8")

    def problems(self, name="ada"):
        return [(p.level, p.check, p.message) for p in checkpersona.check_persona(name, self.root)]

    def run_main(self, *args):
        out = io.StringIO()
        with redirect_stdout(out):
            code = checkpersona.main(["--root", str(self.root), *args])
        return code, out.getvalue()

    def test_clean_persona_passes(self):
        self.assertEqual(self.problems(), [])
        code, out = self.run_main()
        self.assertEqual(code, 0)
        self.assertIn("Checked 1 persona(s): 0 error(s), 0 warning(s).", out)

    def test_template_is_skipped(self):
        self.assertEqual(checkpersona.find_personas(self.root), ["ada"])

    def test_missing_files(self):
        (self.root / "personas/ada/system-prompt.md").unlink()
        self.assertIn(("ERROR", "files", "missing personas/ada/system-prompt.md"), self.problems())

    def test_unknown_persona(self):
        self.assertEqual(self.problems("bob"), [("ERROR", "files", "no folder personas/bob/")])

    def test_cited_but_undefined_source(self):
        self.edit("personas/ada/profile.md", "Also [S2].", "Also [S2] and [S7].")
        self.assertIn(("ERROR", "sources", "[S7] is cited but not defined in Sources"), self.problems())

    def test_defined_but_uncited_source_is_warning(self):
        self.edit("personas/ada/profile.md", "Also [S2].", "Also nothing.")
        self.assertEqual(self.problems(), [("WARN", "sources", "[S2] is defined but never cited")])
        self.assertEqual(self.run_main()[0], 0)
        self.assertEqual(self.run_main("--strict")[0], 1)

    def test_duplicate_source_definition(self):
        self.edit("personas/ada/profile.md", "- **[S2]** Book", "- **[S1]** Again\n- **[S2]** Book")
        self.assertIn(("ERROR", "sources", "[S1] is defined 2 times"), self.problems())

    def test_citation_inside_sources_does_not_count(self):
        self.edit("personas/ada/profile.md", "Also [S2].", "Also nothing.")
        self.edit("personas/ada/profile.md", "Book —", "Book, see also [S2] —")
        self.assertIn(("WARN", "sources", "[S2] is defined but never cited"), self.problems())

    def test_missing_sources_section(self):
        self.edit("personas/ada/profile.md", "## 9. Sources", "## 9. Reading list")
        self.assertIn(("ERROR", "sources", "profile.md has no Sources section"), self.problems())

    def test_drifted_quote_is_an_error(self):
        self.edit("personas/ada/system-prompt.md", "big results", "huge results")
        problems = self.problems()
        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0][:2], ("ERROR", "quotes"))
        self.assertIn("huge results", problems[0][2])
        self.assertEqual(self.run_main()[0], 1)

    def test_quote_with_ellipsis_checks_each_fragment(self):
        self.edit("personas/ada/system-prompt.md", "adjust as you go", "change course often")
        problems = self.problems()
        self.assertEqual(len(problems), 1)
        self.assertIn("change course often", problems[0][2])

    def test_quotes_outside_verified_section_are_ignored(self):
        self.assertFalse(any(check == "quotes" for _, check, _ in self.problems()))

    def test_missing_verified_section_is_warning(self):
        self.edit("personas/ada/system-prompt.md", "## Verified lines you may quote", "## Lines")
        self.assertIn(("WARN", "quotes", "system-prompt.md has no \"Verified lines\" section"), self.problems())

    def test_missing_agent(self):
        (self.root / ".claude/agents/ada.md").unlink()
        self.assertIn(("ERROR", "agent", "missing .claude/agents/ada.md"), self.problems())

    def test_agent_name_mismatch(self):
        self.edit(".claude/agents/ada.md", "name: ada", "name: bob")
        self.assertIn(("ERROR", "agent", "front matter says name: bob, expected ada"), self.problems())

    def test_agent_does_not_load_prompt(self):
        self.edit(".claude/agents/ada.md", "personas/ada/system-prompt.md", "somewhere else")
        self.assertIn(("ERROR", "agent", "does not load personas/ada/system-prompt.md"), self.problems())

    def test_missing_readme_row(self):
        self.write("README.md", "# Persona\n")
        self.assertIn(("ERROR", "readme", "README.md does not link to personas/ada/"), self.problems())

    def test_no_personas(self):
        shutil.rmtree(self.root / "personas/ada")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("No personas found.", out)


class RealRepoTest(unittest.TestCase):
    def test_repository_personas_have_no_errors(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = checkpersona.main(["--root", str(REPO)])
        self.assertEqual(code, 0, out.getvalue())


if __name__ == "__main__":
    unittest.main()
