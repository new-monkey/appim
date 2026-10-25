"""Unit tests for the appim script.

Run with:  python -m unittest discover -s tests -v
"""

import importlib.machinery
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "appim"


def load_module():
    # The script has no .py suffix, so the loader must be given explicitly.
    loader = importlib.machinery.SourceFileLoader("appim", str(SCRIPT))
    spec = importlib.util.spec_from_loader("appim", loader)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


appim = load_module()


class SlugTests(unittest.TestCase):
    def test_lowercases_and_replaces_spaces(self):
        self.assertEqual(appim.slug("Foo Bar"), "foo-bar")

    def test_collapses_consecutive_spaces_into_one_dash(self):
        self.assertEqual(appim.slug("Foo   Bar"), "foo-bar")

    def test_replaces_slashes(self):
        self.assertEqual(appim.slug("A/B"), "a-b")

    def test_strips_surrounding_whitespace(self):
        self.assertEqual(appim.slug("  Foo  "), "foo")


class SanitizeTests(unittest.TestCase):
    def test_keeps_inner_spaces_and_case(self):
        self.assertEqual(appim._sanitize("Cherry Studio"), "Cherry Studio")


class QuoteExecArgTests(unittest.TestCase):
    def test_plain_path_is_quoted(self):
        self.assertEqual(appim.quote_exec_arg("/opt/My App.AppImage"), '"/opt/My App.AppImage"')

    def test_escapes_shell_metacharacters(self):
        got = appim.quote_exec_arg('a"b$c`d\\e')
        self.assertEqual(got, '"a\\"b\\$c\\`d\\\\e"')


class ParseDesktopTests(unittest.TestCase):
    def test_reads_name_icon_and_exec(self):
        text = (
            "[Desktop Entry]\n"
            "Type=Application\n"
            "Name=Cherry Studio\n"
            "Name[zh_CN]=樱桃工作室\n"
            "Icon=cherry-studio\n"
            "Exec=/tmp/app.AppImage --no-sandbox %U\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "app.desktop"
            path.write_text(text, encoding="utf-8")
            fields = appim.parse_desktop(path)
        self.assertEqual(fields["name"], "Cherry Studio")
        self.assertEqual(fields["icon"], "cherry-studio")
        self.assertEqual(fields["exec"], "/tmp/app.AppImage --no-sandbox %U")

    def test_ignores_localized_keys(self):
        text = "Name[de]=Deutsch\nIcon[de]=x\nExec[de]=y\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "app.desktop"
            path.write_text(text, encoding="utf-8")
            fields = appim.parse_desktop(path)
        self.assertIsNone(fields["name"])
        self.assertIsNone(fields["icon"])
        self.assertIsNone(fields["exec"])


class RewriteDesktopTests(unittest.TestCase):
    def _rewrite(self, src_text):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "app.desktop"
            appim.rewrite_desktop(src_text, dest, Path("/installed/App.AppImage"), "/icons/app.png", "App")
            return dest.read_text(encoding="utf-8")

    def test_generates_entry_when_template_missing(self):
        out = self._rewrite(None)
        self.assertIn("[Desktop Entry]", out)
        self.assertIn("Type=Application", out)
        self.assertIn('Exec="/installed/App.AppImage"', out)
        self.assertIn("Icon=/icons/app.png", out)
        self.assertIn("Terminal=false", out)

    def test_keeps_extra_exec_arguments(self):
        out = self._rewrite("Exec=/old/App.AppImage --no-sandbox %U\n")
        self.assertIn('Exec="/installed/App.AppImage" --no-sandbox %U', out)

    def test_replaces_icon_and_preserves_other_lines(self):
        out = self._rewrite("[Desktop Entry]\nExec=x\nIcon=old\nCategories=Utility;\n")
        self.assertIn("Icon=/icons/app.png", out)
        self.assertIn("Categories=Utility;", out)
        self.assertNotIn("Icon=old", out)

    def test_does_not_touch_action_specific_keys(self):
        out = self._rewrite("Exec=x\nExec[Editor]=other\n")
        self.assertIn("Exec[Editor]=other", out)

    def test_appends_missing_exec_and_icon(self):
        out = self._rewrite("[Desktop Entry]\nName=App\n")
        self.assertIn('Exec="/installed/App.AppImage"', out)
        self.assertIn("Icon=/icons/app.png", out)


class CliTests(unittest.TestCase):
    def _run(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

    def test_version(self):
        proc = self._run("--version")
        self.assertEqual(proc.returncode, 0)
        self.assertIn(appim.__version__, proc.stdout)

    def test_help_exits_zero(self):
        self.assertEqual(self._run("--help").returncode, 0)

    def test_no_arguments_fails(self):
        self.assertNotEqual(self._run().returncode, 0)

    def test_rejects_missing_file(self):
        proc = self._run("install", "/nonexistent/foo.AppImage")
        self.assertNotEqual(proc.returncode, 0)

    def test_rejects_non_appimage_file(self):
        with tempfile.NamedTemporaryFile(suffix=".txt") as tmp:
            proc = self._run("install", tmp.name)
        self.assertNotEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
