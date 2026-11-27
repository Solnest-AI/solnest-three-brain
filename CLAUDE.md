If the user said "set this up", follow SETUP below.

# Three-Brain (Solnest AI)

This repo installs the `solnest-three-brain` skill: a set of rules that tells Claude when to bring in a second model. Claude stays the main driver. Codex (GPT) gets a bug that beat Claude twice and reviews finished work. Gemini gets very large files, long documents and video. Grok is an optional extra reviewer. "Ask all three" and "debate this" put the answers side by side.

The skill is text plus three small scripts. The other models come from three Claude Code plugins made by other people, which setup installs from their own marketplaces:

- Codex: `codex@openai-codex` (marketplace `openai/codex-plugin-cc`)
- Gemini: `gemini@google-gemini` (marketplace `sakibsadmanshajib/gemini-plugin-cc`)
- Grok (optional): `grok-build@xai-grok-build` (marketplace `xai-org/grok-build-plugin-cc`)

What is in here:
- `skill/solnest-three-brain/`: the skill (`SKILL.md`, `SETUP.md` for fixes, `scripts/`). It installs to `~/.claude/skills/solnest-three-brain`.
- `install.sh`: the installer. `VERSION` and `CHANGELOG.md`: what release this is.

## Your own changes (read first, every time)

Before anything else, read `~/.solnest/three-brain/my-instructions.md` if it exists and
follow it. It holds this user's own changes to how this tool works, and it wins over the
defaults in this file.

When the user asks to change how this tool works for them (wording, tone, topics, steps,
defaults, what to include or leave out), write the change into that file in plain words,
create it if needed, and read it back to them. **Never edit this tool's own files for
that.** This tool updates itself automatically and replaces its own files, so a change
made there is lost on the next update. Their sign-ins are never touched by an update
either: the Gemini key file (`~/.solnest/three-brain/.env`, or a key already in their
shell profile), the Codex and Grok logins, and the three plugins all live outside the
skill folder.

## Rules for you (Claude) during setup

- You run every command yourself with your Bash tool, except the two sign-ins that open a browser (Codex and Grok) and pasting the Gemini key. On Windows, Claude Code runs Bash commands in Git Bash, where these commands (including `~`) work.
- One step per message. Do not report success until you have seen real output.
- **Never ask for a key in chat, and never print one.** The Gemini key goes into a file the user pastes into themselves. Do not `cat` that file and do not `echo $GEMINI_API_KEY`.
- This is an update of an older copy if `~/.claude/skills/solnest-three-brain` already exists. Do the same steps. Every step skips what is already done, so nobody signs in twice.
- Never show a raw error. Fix it, or explain it in one plain sentence.

## SETUP

### Step 1: Check what is on this computer

```bash
node --version; command -v claude codex gemini grok; echo "shell: ${SHELL:-unknown}"
```

- Node must be 18.18 or newer (the Codex, Gemini and Grok tools are Node programs). No Node, or an older one: send the user to https://nodejs.org, the LTS installer. Go on when they say it is installed.
- Anything else missing is fine. The next steps install it.

### Step 2: Install the skill

Tell the user in one line: "Installing the Three-Brain skill. About a minute, nothing for you to do." Then run one of these:

- You are reading this from the GitHub page (no local copy of this repo):

  ```bash
  bash -o pipefail -c "curl -fsSL https://raw.githubusercontent.com/Solnest-AI/solnest-three-brain/main/install.sh | bash"
  ```

- You already have this repo as a folder on this computer: `bash "<this folder>/install.sh"`

Read the checklist it prints:

- Every line starts with `[ok]`: go on.
- `STOP: ... holds a different skill` or `... a link or a git checkout`: something else already lives at `~/.claude/skills/solnest-three-brain`. Nothing was changed. Tell the user what you found and ask what they want to do with it. Do not delete it yourself.
- `ERROR: could not download`: usually the network. Run it once more.
- `ERROR: no working Python`: send the user to https://www.python.org/downloads/ (on Windows they must tick "Add python.exe to PATH"). When they say it is installed, run it again. Python is only used by the automatic updates.
- `[!!] updater`: run it once more. If it repeats, send the full output to hello@solnestai.com.

### Step 3: Add the Codex and Gemini plugins

```bash
claude plugin marketplace add openai/codex-plugin-cc && claude plugin install codex@openai-codex
claude plugin marketplace add sakibsadmanshajib/gemini-plugin-cc && claude plugin install gemini@google-gemini
```

Both are safe to run again: they say "already installed" and change nothing.

If `claude` is not found (the user only has the desktop app), ask the user to type these four lines into the chat box, one at a time:

```
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/plugin marketplace add sakibsadmanshajib/gemini-plugin-cc
/plugin install gemini@google-gemini
```

Then install the two programs the plugins call, only the ones Step 1 did not find:

```bash
command -v codex >/dev/null || npm install -g @openai/codex
command -v gemini >/dev/null || npm install -g @google/gemini-cli
```

### Step 4: Sign in to Codex (the user, 1 minute)

```bash
codex login status
```

- It says logged in: go on.
- It does not: tell the user "Type `!codex login` in the chat box and press Enter. A browser page opens. Sign in with your ChatGPT account. A free account works." When they say done, run `codex login status` again.

### Step 5: Give Gemini its key (the user, 2 minutes)

Gemini needs a free API key. Signing in with a Google account does not work for this. Some older guides, and the Gemini plugin's own help text, still say to run `!gemini` and sign in. Ignore them.

```bash
bash ~/.claude/skills/solnest-three-brain/scripts/gemini-key.sh status
```

- `[ok] Gemini key: set`: they already have one. Skip to Step 6.
- Anything else: run

  ```bash
  bash ~/.claude/skills/solnest-three-brain/scripts/gemini-key.sh open
  ```

  A small text file opens on their screen. Tell the user:

  1. Go to https://aistudio.google.com/apikey and sign in with a Google account.
  2. Click **Create API key**. It is free and needs no credit card.
  3. Copy the key, paste it right after `GEMINI_API_KEY=` in the file that just opened, save the file and close it.
  4. Say "saved". Do not paste the key here in the chat.

  When they say saved:

  ```bash
  bash ~/.claude/skills/solnest-three-brain/scripts/gemini-key.sh apply
  ```

  It checks the file has a key (without showing it) and makes Claude Code see it the next time it starts. If it prints `[!!]`, read the line to the user in plain words and let them fix the file.

### Step 6: Grok (optional, ask first)

Ask one plain question: "Do you want Grok added too? It is optional, it needs a Grok account, and it takes about three more minutes. Codex and Gemini already give you the full tool." If they say no, go to Step 7. Never push it.

Grok's installer is for Mac and Linux. On Windows, say Grok is not available there yet and go to Step 7.

If yes:

```bash
command -v grok >/dev/null || [ -x "$HOME/.grok/bin/grok" ] || curl -fsSL https://x.ai/cli/install.sh | bash
claude plugin marketplace add xai-org/grok-build-plugin-cc && claude plugin install grok-build@xai-grok-build
```

(The first line is xAI's own installer. If `claude` is not found, the user types `/plugin marketplace add xai-org/grok-build-plugin-cc` and `/plugin install grok-build@xai-grok-build`.)

Then the sign-in. Tell the user: "Type `!~/.grok/bin/grok login --oauth` in the chat box and press Enter. A browser page opens. Sign in to your Grok account." When they say done, check it (it tries three times, because the first try right after a sign-in can miss):

```bash
ok=""; for i in 1 2 3; do "$HOME/.grok/bin/grok" models 2>&1 | grep -i "logged in" && { ok=1; break; }; sleep 2; done; [ -n "$ok" ] || echo "not signed in yet"
```

### Step 7: Real check (read-only)

```bash
codex login status; bash ~/.claude/skills/solnest-three-brain/scripts/gemini-key.sh status; claude plugin list 2>/dev/null | grep -E "codex@|gemini@|grok-build@"
```

Codex must say logged in, the Gemini line must start with `[ok]` or `[..]` (saved, seen after the restart), and both `codex@openai-codex` and `gemini@google-gemini` must be listed. Fix whatever is missing before going on. Half a setup is worse than none, because it fails in the middle of a job. Grok is a bonus: if its check failed, say so in one line and go on.

### Step 8: Turn on automatic updates (required, silent)

Run this exactly:

```bash
SKILL="$HOME/.claude/skills/solnest-three-brain"; "$SKILL/bin/py" "$SKILL/scripts/solnest_autoupdate.py" register --name three-brain --folder "$SKILL" --update '{python} scripts/update.py' --after '{python} scripts/update.py --help' --undo '{python} scripts/update.py --undo'
```

From now on the skill keeps itself on the latest release with no one asking: once a day, in the background when Claude Code starts, it installs the newest published release and checks that it starts. It never touches the user's sign-ins, their Gemini key, their own instructions or any file they added, and if a new release fails that check it puts the old version back by itself. Relay the one line it prints. Nothing else to tell them.

### Step 9: Tell the user what worked, then the restart

Short checklist: skill installed, Codex signed in, Gemini key saved, Grok added or skipped, automatic updates on. Then say:

> One last thing: fully quit Claude Code and open it again (quit the app, not just the window). That is when the new plugins and your Gemini key switch on. Then type `/codex:status` and `/gemini:status`. Both should say ready.
>
> After that, on any tough call, say **"ask all three"** or **"debate this"**. You get every answer side by side, with the places they disagree pointed out.

If `/gemini:status` still says not signed in after the restart, the fixes are in `~/.claude/skills/solnest-three-brain/SETUP.md`.

## Update

Updates install themselves (Step 8). Sign-ins, the Gemini key and files the user added are never touched. Changes the user asked for live in `~/.solnest/three-brain/my-instructions.md`, outside the skill folder, so they survive every update. The three plugins are updated by Claude Code itself, not by this tool.

Only when the user asks to update now:

```bash
SKILL="$HOME/.claude/skills/solnest-three-brain"; "$SKILL/bin/py" "$SKILL/scripts/update.py" && "$SKILL/bin/py" "$SKILL/scripts/update.py" --help >/dev/null && echo "[ok] updater starts"
```

Then run the Step 8 line once more, so a newer auto-updater is picked up. To go back one version: `"$HOME/.claude/skills/solnest-three-brain/bin/py" "$HOME/.claude/skills/solnest-three-brain/scripts/update.py" --undo`. If `scripts/update.py` is missing (a copy from before automatic updates), run Step 2 instead, then Step 8.

"Is it updating itself?": `~/.claude/skills/solnest-three-brain/bin/py ~/.solnest/autoupdate.py status`. Use `pause` in place of `status` to stop all automatic updates, and `resume` to turn them back on.

If `status` shows the last check failed, offer to update now with the line above.

## Repair

Run Step 2 again, then Step 7 and Step 8. It keeps every sign-in.

## Uninstall

```bash
~/.claude/skills/solnest-three-brain/bin/py ~/.solnest/autoupdate.py remove --name three-brain
```

Then, after a plain yes from the user, delete the folder `~/.claude/skills/solnest-three-brain`. Their Gemini key file is `~/.solnest/three-brain/.env`; delete it too if they want it gone, along with the one line marked "Solnest Three-Brain" in their shell profile. `codex logout` and `grok logout` sign those out.
