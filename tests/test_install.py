"""install.sh: installs the skill into a (fake) home, writes the launcher, keeps the user's
own files on a second run, clears the old setup pages of a pre-1.2.0 copy, never copies
.cursor, and refuses to overwrite a different skill. Offline: it installs from this copy
of the repo, or from a local archive."""
import os
import pathlib
import shutil
import subprocess
import tarfile
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parent.parent
NAME = "solnest-three-brain"
BASH = shutil.which("bash")


def skip_private(t):
    return None if ("__pycache__" in t.name or ".cursor" in t.name) else t


@unittest.skipUnless(BASH, "needs bash")
class InstallTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = pathlib.Path(self.tmp.name) / "home"
        self.home.mkdir()
        self.dest = self.home / ".claude" / "skills" / NAME

    def run_install(self, script=None, stdin=None, **extra):
        env = dict(os.environ, HOME=str(self.home), **extra)
        args = [BASH, str(script)] if script else [BASH]
        return subprocess.run(args, env=env, capture_output=True, text=True, timeout=300,
                              stdin=stdin or subprocess.DEVNULL, cwd=self.tmp.name)

    def test_installs_and_a_second_run_keeps_user_files(self):
        r = self.run_install(REPO / "install.sh")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("[ok] updater", r.stdout)
        for rel in ("SKILL.md", "SETUP.md", "VERSION", "bin/py", "scripts/update.py",
                    "scripts/solnest_autoupdate.py", "scripts/grok-consult.sh", "scripts/gemini-key.sh"):
            self.assertTrue((self.dest / rel).is_file(), rel)
        self.assertEqual((self.dest / "VERSION").read_text(), (REPO / "VERSION").read_text())
        self.assertFalse(list(self.dest.rglob(".cursor")))
        h = subprocess.run([str(self.dest / "bin" / "py"), str(self.dest / "scripts" / "update.py"), "--help"],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(h.returncode, 0, h.stderr)

        (self.dest / "my-notes.md").write_text("mine\n", encoding="utf-8")
        r = self.run_install(REPO / "install.sh")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual((self.dest / "my-notes.md").read_text(), "mine\n")

    def test_private_editor_rules_in_the_source_are_never_installed(self):
        """A sync job on the author's machine drops .cursor/ into folders. It must not ship."""
        src = pathlib.Path(self.tmp.name) / "repo"
        shutil.copytree(REPO / "skill", src / "skill", ignore=shutil.ignore_patterns("__pycache__", ".cursor"))
        shutil.copy(REPO / "VERSION", src / "VERSION")
        shutil.copy(REPO / "install.sh", src / "install.sh")
        planted = src / "skill" / NAME / ".cursor" / "rules"
        planted.mkdir(parents=True)
        (planted / "private.mdc").write_text("private\n", encoding="utf-8")
        r = self.run_install(src / "install.sh")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue((self.dest / "SKILL.md").is_file())
        self.assertFalse((self.dest / ".cursor").exists())

    def test_an_older_copy_loses_its_old_setup_pages_only(self):
        """Before 1.2.0 the whole repo sat in the skill folder, setup pages included."""
        self.dest.mkdir(parents=True)
        (self.dest / "SKILL.md").write_text("---\nname: solnest-three-brain\n---\nOLD COPY\n", encoding="utf-8")
        (self.dest / "VERSION").write_text("1.1.0\n", encoding="utf-8")
        for old in ("START-HERE.md", "UPDATE.md", "README.md"):
            (self.dest / old).write_text("# Solnest Three-Brain old page\n", encoding="utf-8")
        (self.dest / "NOTES.md").write_text("mine\n", encoding="utf-8")
        r = self.run_install(REPO / "install.sh")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        for old in ("START-HERE.md", "UPDATE.md", "README.md"):
            self.assertFalse((self.dest / old).exists(), old)
        self.assertEqual((self.dest / "NOTES.md").read_text(), "mine\n")
        self.assertEqual((self.dest / "VERSION").read_text(), (REPO / "VERSION").read_text())
        self.assertNotIn("OLD COPY", (self.dest / "SKILL.md").read_text())

    def test_piped_install_from_an_archive(self):
        """The `curl ... | bash` path: no local repo, the skill comes from an archive."""
        archive = pathlib.Path(self.tmp.name) / "main.tar.gz"
        with tarfile.open(archive, "w:gz") as tar:
            tar.add(REPO / "VERSION", "solnest-three-brain-main/VERSION")
            tar.add(REPO / "skill", "solnest-three-brain-main/skill", filter=skip_private)
        with open(REPO / "install.sh", "rb") as script:
            r = self.run_install(stdin=script, THREE_BRAIN_ARCHIVE_URL=archive.as_uri())
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("downloading the skill", r.stdout)
        self.assertTrue((self.dest / "SKILL.md").is_file())
        self.assertEqual((self.dest / "VERSION").read_text(), (REPO / "VERSION").read_text())

    def test_refuses_a_different_skill(self):
        self.dest.mkdir(parents=True)
        (self.dest / "SKILL.md").write_text("---\nname: something-else\n---\n", encoding="utf-8")
        r = self.run_install(REPO / "install.sh")
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertEqual((self.dest / "SKILL.md").read_text(), "---\nname: something-else\n---\n")
        self.assertFalse((self.dest / "scripts").exists())


if __name__ == "__main__":
    unittest.main()
