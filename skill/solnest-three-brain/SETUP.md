# Fixes: the other brains

You only need this page if something stopped working. The guided setup (paste the GitHub link into Claude Code and say "set this up") does all of this for you, and it is safe to run again.

The router itself is just text. **The models it routes to are separate plugins**, and each needs to be installed and signed in. If one is missing, the router quietly loses that brain.

---

## Codex (GPT): the second brain

```
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
!codex login
```

Signs in with **any ChatGPT account, including the free tier**, or an OpenAI API key. The login opens a browser.

Check: `/codex:status`

---

## Gemini: the third brain

```
/plugin marketplace add sakibsadmanshajib/gemini-plugin-cc
/plugin install gemini@google-gemini
```

### Gemini needs an API key. Google sign-in no longer works

This is the one thing people get stuck on. Older guides say to run `!gemini` and sign in with your Google account. **That doesn't work any more.** An API key is the only way in.

1. Go to **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)**.
2. Click **Create API key**. It's free, and there's no credit card required.
3. Copy it. It starts with `AIza...`.

Never paste the key into the chat. Ask Claude to "open my Gemini key file", or run:

```bash
bash ~/.claude/skills/solnest-three-brain/scripts/gemini-key.sh open
```

A small text file opens (`~/.solnest/three-brain/.env`). Paste the key right after `GEMINI_API_KEY=`, save, close. Then:

```bash
bash ~/.claude/skills/solnest-three-brain/scripts/gemini-key.sh apply
```

That adds one line to your shell profile that loads the file (Mac, Linux), or saves the key as a user environment variable (Windows). A key you already set by hand in your shell profile keeps working. You do not need both.

Then **fully quit and reopen Claude Code**, not just the window. It reads the key when it starts, so a key added after launch is not seen.

Check: `/gemini:status`

---

## Grok Build: the optional fourth brain

Skip this section entirely if you don't want Grok. The router works without it.

Grok needs two pieces: the **Grok Build CLI** on your machine, and xAI's **Claude Code plugin** that calls it.

**1. Install the CLI (macOS / Linux).** This is xAI's official installer:

```bash
curl -fsSL https://x.ai/cli/install.sh | bash
```

Open a new terminal afterwards so `grok` is on your PATH. On Windows the installer is a bash script, so use WSL or skip Grok.

**2. Sign in.** This opens a browser to x.ai:

```
!grok login --oauth
```

**3. Install the plugin:**

```
/plugin marketplace add xai-org/grok-build-plugin-cc
/plugin install grok-build@xai-grok-build
```

Check: `/grok-build:check`

### The sandbox gotcha on Macs with Docker Desktop

Grok's `read-only` sandbox can refuse to start when `/var/run/docker.sock` is a symlink, which Docker Desktop sets up. When that happens, `/grok-build:review` and `/grok-build:critique` fail with `could not apply the 'read-only' sandbox profile`.

The fix is already in this skill: `scripts/grok-consult.sh` copies your files to a throwaway folder and runs Grok there in its `workspace` sandbox, so the real project cannot be touched. Claude knows to use it. If you run it yourself:

```bash
bash ~/.claude/skills/solnest-three-brain/scripts/grok-consult.sh <folder> "your question"
```

Never "fix" this by running Grok with no sandbox. Headless runs auto-approve every tool call, so the sandbox is the only thing between Grok and your files.

---

## All brains up?

```
/codex:status
/gemini:status
/grok-build:check
```

Codex and Gemini ready means the router is live. Grok is a bonus.

---

## Troubleshooting

**`/gemini:status` still says unauthenticated.**
Nine times out of ten, Claude Code was already running when the key was saved. Quit it completely and reopen. To check without showing the key, run `bash ~/.claude/skills/solnest-three-brain/scripts/gemini-key.sh status`. `[ok]` means Claude Code sees it. `[..]` means the key is in the file but not switched on yet: run `apply`, then quit and reopen. `[--]` means there is no key yet.

**Gemini says it is "not running in a trusted directory".**
Newer Gemini versions want a folder marked as trusted before they work in it. Gemini's own message says how: open a terminal in that project folder, run `gemini`, and trust the folder when it asks. Then try again.

**It's telling me to sign in with Google.**
Ignore it. That's stale help text inside the Gemini plugin. Get an API key instead.

**Codex login won't open a browser.**
Run `!codex login` from a normal terminal outside Claude Code, then come back and check `/codex:status`.

**`/grok-build:check` says not authenticated.**
Grok logins expire. Run `grok login --oauth` again in a terminal, then re-check. `grok models` should print "logged in with grok.com".

**`grok` command not found after installing.**
Open a new terminal. The installer adds `~/.grok/bin` to your PATH, but a terminal that was already open won't see it.

**Everything says ready but nothing routes.**
The router only pulls in another model when the situation calls for it: a bug that beat Claude twice, a huge file, a review request. To force it, just ask directly: *"ask all three"*, *"debate this"*, *"ask Grok"*, or run `/codex:review`.

---

## Your keys are yours

Everything lives on **your** machine: your Gemini key file (`~/.solnest/three-brain/.env`), and the Codex and Grok tools' own sign-in stores. Nothing is ever written into this skill folder, and nothing is sent to Solnest AI. If you ever want out, delete the key file and the one line marked "Solnest Three-Brain" in your shell profile, run `!codex logout`, and run `grok logout` if you installed Grok.
