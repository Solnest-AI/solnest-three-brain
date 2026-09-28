# UPDATE: Solnest Three-Brain (Claude reads this)

**You are Claude. The user pasted this repo's link and asked you to update their Solnest Three-Brain. Do it FOR them, in plain language. Never paste a raw error at them.**

---

## Step 0: find their install

- macOS / Linux: `~/.claude/skills/solnest-three-brain/`
- Windows: `%USERPROFILE%\.claude\skills\solnest-three-brain\`

If that folder isn't there, they never installed it. Tell them to grab the zip from the Skool community and drag it in for a fresh install, and stop here.

## Step 1: check if they even need this

Compare `VERSION` in their install to `VERSION` in this repo. If they match, say so and stop:

> You're already on the latest version (`X.Y.Z`). Nothing to update. You're good.

## Step 2: what to preserve

**Nothing inside the skill folder.** This skill stores no configuration of its own. It's pure routing policy plus one helper script.

But their **brains live outside it**, and you must not disturb any of them:

- Their **`GEMINI_API_KEY`** lives in their shell profile (`~/.zshrc`, `~/.bashrc`, or Windows environment variables). **Never read it, print it, rewrite it, or ask them to set it again.** It's already there and it still works.
- Their **Codex login** lives in the Codex CLI's own credential store. Don't touch it and don't make them log in again.
- Their **Grok login**, if they have one, lives in the Grok CLI's own store (`~/.grok/`). Same rule: don't touch it.
- The **`codex@openai-codex`, `gemini@google-gemini`, and `grok-build@xai-grok-build` plugins** are installed separately. An update to this skill does not touch them, and they do not need reinstalling.

⚠️ Do **not** re-run the setup from `START-HERE.md` after updating. Everything is already wired. Re-running it risks walking them through a Gemini key they already have.

## Step 3: pull the latest

```bash
git clone --depth 1 https://github.com/Solnest-AI/solnest-three-brain.git /tmp/solnest-three-brain-update
```

No `git`? Download `https://github.com/Solnest-AI/solnest-three-brain/archive/refs/heads/main.zip` instead.

## Step 4: copy the new files over

Copy the fresh files into their skill folder, **file over file**, including the `scripts/` folder (new in 1.2.0). Don't delete the folder first. Just overwrite what's changed.

On macOS / Linux, make the helper executable afterwards:

```bash
chmod +x ~/.claude/skills/solnest-three-brain/scripts/grok-consult.sh
```

## Step 5: confirm it landed

Check `SKILL.md` is still at the install path, `scripts/grok-consult.sh` is there, and `VERSION` now shows the new number.

## Step 6: quick health check on the brains

Since this skill is useless without them, confirm the required two are still up:

```
/codex:status
/gemini:status
```

If they have Grok installed, also run `/grok-build:check`. If they don't, don't install it for them. Mention once that Grok is now supported as an optional fourth brain and that `SETUP.md` has the steps, then move on.

If **Gemini** reports unauthenticated, do **not** tell them to sign in with a Google account. That path no longer exists. It means their `GEMINI_API_KEY` isn't reaching Claude Code. Almost always the fix is to fully quit and reopen Claude Code. If it's genuinely missing, point them at `SETUP.md` to get a free key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

## Step 7: tell them what changed

Read `CHANGELOG.md` from the fresh copy and give them two or three plain-English bullets for the **new version only**, not the whole file. Then:

> Updated to `X.Y.Z`. Your Gemini key, Codex login, and Grok login are untouched. Nothing to redo.

## If something goes wrong

Tell them in one friendly sentence. Nothing here is destructive. They can always reinstall from the Skool zip, and their keys live outside the skill so they survive anything that happens to this folder.
