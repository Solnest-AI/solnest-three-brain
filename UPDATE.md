# UPDATE — Solnest Three-Brain (Claude reads this)

**You are Claude. The user pasted this repo's link and asked you to update their Solnest Three-Brain. Do it FOR them, in plain language. Never paste a raw error at them.**

---

## Step 0 — Find their install

- macOS / Linux: `~/.claude/skills/solnest-three-brain/`
- Windows: `%USERPROFILE%\.claude\skills\solnest-three-brain\`

If that folder isn't there, they never installed it. Tell them to grab the zip from the Skool community and drag it in for a fresh install, and stop here.

## Step 1 — Check if they even need this

Compare `VERSION` in their install to `VERSION` in this repo. If they match, say so and stop:

> You're already on the latest version (`X.Y.Z`) — nothing to update. You're good.

## Step 2 — What to preserve

**Nothing inside the skill folder.** This skill stores no configuration of its own — it's pure routing policy.

But their **two brains live outside it**, and you must not disturb either:

- Their **`GEMINI_API_KEY`** lives in their shell profile (`~/.zshrc`, `~/.bashrc`, or Windows environment variables). **Never read it, print it, rewrite it, or ask them to set it again.** It's already there and it still works.
- Their **Codex login** lives in the Codex CLI's own credential store. Don't touch it and don't make them log in again.
- The **`codex@openai-codex` and `gemini@google-gemini` plugins** are installed separately. An update to this skill does not touch them, and they do not need reinstalling.

⚠️ Do **not** re-run the setup from `START-HERE.md` after updating. Everything is already wired — re-running it risks walking them through a Gemini key they already have.

## Step 3 — Pull the latest

```bash
git clone --depth 1 https://github.com/Solnest-AI/solnest-three-brain.git /tmp/solnest-three-brain-update
```

No `git`? Download `https://github.com/Solnest-AI/solnest-three-brain/archive/refs/heads/main.zip` instead.

## Step 4 — Copy the new files over

Copy the fresh files into their skill folder, **file over file**. Don't delete the folder first — just overwrite what's changed.

## Step 5 — Confirm it landed

Check `SKILL.md` is still at the install path and `VERSION` now shows the new number.

## Step 6 — Quick health check on the two brains

Since this skill is useless without them, confirm both are still up:

```
/codex:status
/gemini:status
```

If **Gemini** reports unauthenticated, do **not** tell them to sign in with a Google account — that path no longer exists. It means their `GEMINI_API_KEY` isn't reaching Claude Code. Almost always the fix is to fully quit and reopen Claude Code. If it's genuinely missing, point them at `SETUP.md` to get a free key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

## Step 7 — Tell them what changed

Read `CHANGELOG.md` from the fresh copy and give them two or three plain-English bullets for the **new version only** — not the whole file. Then:

> Updated to `X.Y.Z`. Your Gemini key and Codex login are untouched — nothing to redo.

## If something goes wrong

Tell them in one friendly sentence. Nothing here is destructive — they can always reinstall from the Skool zip, and their keys live outside the skill so they survive anything that happens to this folder.
