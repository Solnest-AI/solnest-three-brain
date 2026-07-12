# START HERE — Auto-installer (Claude reads this)

**You are Claude running in Claude Code. The user just dragged in this folder to install the "Solnest Three-Brain" skill. Do the install FOR them now, one step at a time, in plain language. Never paste a raw error at them — fix it quietly, or explain it in one friendly sentence.**

This skill is **text-only — nothing to compile.** But unlike most skills, it **only works if two other plugins are installed and signed in**, because its whole job is routing work to them. So this install has two halves: copy the skill in, then wire up the two other brains.

> ⚠️ **This one needs Claude Code, not the Claude Desktop app.** The router calls `/codex:*` and `/gemini:*` slash commands, and those only exist in Claude Code. If the user is in the Desktop app, tell them that plainly and stop.

---

## Step 1 — Copy the skill into place

- **Source:** the folder this `START-HERE.md` is sitting in (it contains `SKILL.md`).
- **Destination:** the user's personal Claude skills folder, in a subfolder named `solnest-three-brain`:
  - macOS / Linux: `~/.claude/skills/solnest-three-brain`
  - Windows: `%USERPROFILE%\.claude\skills\solnest-three-brain`

If it already exists, just say you're updating their existing copy and continue.

**macOS / Linux (bash):**
```bash
mkdir -p ~/.claude/skills
cp -R "<<THIS_FOLDER>>" ~/.claude/skills/solnest-three-brain
```

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse -Force "<<THIS_FOLDER>>" "$env:USERPROFILE\.claude\skills\solnest-three-brain"
```

(Replace `<<THIS_FOLDER>>` with the real path of the folder you're reading this from.)

Confirm `SKILL.md` landed at the destination before moving on.

---

## Step 2 — Install the second brain: Codex (GPT)

Tell the user you're adding the Codex plugin, then have them run these two lines in Claude Code:

```
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
```

Then sign in:

```
!codex login
```

Codex works with **any ChatGPT account — including the free tier** — or an OpenAI API key. The login is interactive and opens a browser.

Check it took:

```
/codex:status
```

---

## Step 3 — Install the third brain: Gemini

Have them run:

```
/plugin marketplace add sakibsadmanshajib/gemini-plugin-cc
/plugin install gemini@google-gemini
```

### Now the part that trips everyone up

**Gemini needs an API key. Signing in with a Google account no longer works.**

You may see older guides (and even the plugin's own help text) say "run `!gemini` and sign in with Google." **That path is dead.** Don't send the user down it — they'll hit a wall and think they broke something. The API key is the only way in.

Walk them through it:

1. Go to **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)** and sign in with a Google account.
2. Click **Create API key**. It's free — the free tier is generous and no credit card is required.
3. Copy the key (it starts with `AIza...`).

Then set it as an environment variable so it persists across restarts. **Ask them to paste the key to you, or better, have them run this themselves with their key pasted in.**

**macOS / Linux** — figure out their shell first (`echo $SHELL`), then append to the right profile:

```bash
# zsh (the default on modern macOS)
echo 'export GEMINI_API_KEY="paste-their-key-here"' >> ~/.zshrc
source ~/.zshrc

# bash
echo 'export GEMINI_API_KEY="paste-their-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell):**
```powershell
setx GEMINI_API_KEY "paste-their-key-here"
```
(Windows needs a **new terminal** afterwards for `setx` to take effect.)

⚠️ **Their key is theirs.** It goes in their shell profile, never inside this skill folder, and never into a file that gets committed anywhere.

### Confirm Gemini is live

They must **fully quit and reopen Claude Code** so it picks up the new environment variable. Then:

```
/gemini:status
```

If it still says unauthenticated, the usual cause is that Claude Code was started before the variable was set — quit it completely (not just the window) and reopen.

---

## Step 4 — Confirm all three brains are up

Run both:

```
/codex:status
/gemini:status
```

Both should report ready. If one doesn't, fix that one before telling the user they're done — a half-installed router is worse than none, because it fails silently mid-task.

---

## Step 5 — Tell them they're done

Say something like:

> You're all set — you've got three brains now. Claude drives by default, and it'll automatically pull in **Codex** for a second opinion when a bug beats it twice, and **Gemini** for huge files, long documents, or video.
>
> Try it: ask me to **"debate this"** or **"ask all three"** on any tough call and you'll get all three answers side by side, with the disagreements called out.
>
> You can also go direct any time: `/codex:review` to have GPT tear apart your last change before you ship it.

Don't oversell it. It's a router — it earns its keep quietly.
