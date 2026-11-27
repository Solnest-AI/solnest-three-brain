"""The two shell helpers. gemini-key.sh: the key goes from a file into the environment and
is never printed. grok-consult.sh: Grok only ever runs inside a throwaway copy, in its
workspace sandbox, and .env files are never copied. Both run against fakes: a fake home
and a fake `grok` on PATH. No real key, no real Grok call."""
import os
import pathlib
import shutil
import stat
import subprocess
import tempfile
import unittest

SCRIPTS = pathlib.Path(__file__).resolve().parent.parent / "skill" / "solnest-three-brain" / "scripts"
BASH = shutil.which("bash")
FAKE_KEY = "FAKE_test_key_" + "0" * 26   # made up, never a real key

FAKE_GROK = """#!/bin/sh
if [ "$1" = "models" ]; then echo "${FAKE_GROK_AUTH:-logged in with grok.com}" >&2; exit 0; fi
echo "ARGS: $*"
echo "CWD: $(pwd -P)"
echo "FILES: $(ls -A | tr '\\n' ' ')"
echo "scribble" > grok-wrote-this.txt
"""


@unittest.skipUnless(BASH, "needs bash")
class GeminiKeyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = pathlib.Path(self.tmp.name)
        self.file = self.home / ".solnest" / "three-brain" / ".env"

    def run_key(self, cmd, **extra):
        env = {k: v for k, v in os.environ.items() if k not in ("GEMINI_API_KEY", "SOLNEST_HOME")}
        env.update(HOME=str(self.home), SHELL="/bin/zsh", THREE_BRAIN_NO_OPEN="1", **extra)
        return subprocess.run([BASH, str(SCRIPTS / "gemini-key.sh"), cmd], env=env, capture_output=True,
                              text=True, timeout=60)

    def test_open_paste_apply_and_the_key_is_never_printed(self):
        self.assertIn("[--]", self.run_key("status").stdout)
        r = self.run_key("open")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("GEMINI_API_KEY=\n", self.file.read_text())
        r = self.run_key("apply")                      # nothing pasted yet
        self.assertEqual(r.returncode, 1)
        self.assertFalse((self.home / ".zshrc").exists())

        self.file.write_text(self.file.read_text().replace("GEMINI_API_KEY=", f'GEMINI_API_KEY="{FAKE_KEY}"'))
        outputs = [self.run_key("status"), self.run_key("apply"), self.run_key("apply"), self.run_key("open")]
        for r in outputs:
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertNotIn(FAKE_KEY, r.stdout + r.stderr)
        self.assertIn("[..]", outputs[0].stdout)
        rc = (self.home / ".zshrc").read_text()
        self.assertEqual(rc.count("Solnest Three-Brain"), 1)       # a second apply adds nothing
        self.assertNotIn(FAKE_KEY, rc)                               # the profile only points at the file
        self.assertIn(FAKE_KEY, self.file.read_text())               # open did not wipe the pasted key
        # a new shell that reads the profile now has the key
        got = subprocess.run([BASH, "-c", f'. "{self.home}/.zshrc"; [ "$GEMINI_API_KEY" = "{FAKE_KEY}" ] && echo same'],
                             env={"HOME": str(self.home), "PATH": os.environ["PATH"]}, capture_output=True, text=True)
        self.assertEqual(got.stdout.strip(), "same", got.stderr)

    def test_a_key_already_in_the_environment_is_enough(self):
        r = self.run_key("status", GEMINI_API_KEY=FAKE_KEY)
        self.assertIn("[ok]", r.stdout)
        self.assertNotIn(FAKE_KEY, r.stdout)

    def test_apply_refuses_something_that_is_not_a_key(self):
        self.run_key("open")
        self.file.write_text("GEMINI_API_KEY=$(touch pwned)\n")
        self.assertEqual(self.run_key("apply").returncode, 1)
        self.assertFalse((self.home / ".zshrc").exists())


@unittest.skipUnless(BASH and shutil.which("rsync"), "needs bash and rsync")
class GrokConsultTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = pathlib.Path(self.tmp.name)
        self.bin = base / "bin"
        self.bin.mkdir()
        grok = self.bin / "grok"
        grok.write_text(FAKE_GROK)
        grok.chmod(grok.stat().st_mode | stat.S_IEXEC)
        self.src = base / "project"
        (self.src / ".git").mkdir(parents=True)
        (self.src / "app.py").write_text("print(1)\n")
        (self.src / ".env").write_text(f"SECRET={FAKE_KEY}\n")

    def run_consult(self, *args, **extra):
        env = dict(os.environ, PATH=f"{self.bin}{os.pathsep}{os.environ['PATH']}", **extra)
        return subprocess.run([BASH, str(SCRIPTS / "grok-consult.sh"), *args], env=env, capture_output=True,
                              text=True, timeout=60)

    def test_runs_in_a_throwaway_copy_with_the_workspace_sandbox(self):
        r = self.run_consult(str(self.src), "is this right?")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("--sandbox workspace", r.stdout)
        cwd = r.stdout.split("CWD: ")[1].splitlines()[0]
        self.assertNotEqual(pathlib.Path(cwd).resolve(), self.src.resolve())
        self.assertFalse(pathlib.Path(cwd).exists())                 # the copy is deleted afterwards
        files = r.stdout.split("FILES: ")[1].splitlines()[0].split()
        self.assertEqual(files, ["app.py"])                          # no .env, no .git
        self.assertEqual(sorted(p.name for p in self.src.iterdir()), [".env", ".git", "app.py"])   # project untouched

    def test_not_signed_in_stops_before_grok_runs(self):
        r = self.run_consult(str(self.src), "q", FAKE_GROK_AUTH="You are not authenticated")
        self.assertEqual(r.returncode, 4)
        self.assertNotIn("ARGS:", r.stdout)


if __name__ == "__main__":
    unittest.main()
