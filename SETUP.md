# Setup: the other brains

You only need this file if something stopped working, or if you skipped the guided install. Normally `START-HERE.md` does all of this for you.

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

Set it so it survives a restart:

**macOS (zsh, the default):**
```bash
echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**Linux (bash):**
```bash
echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell):**
```powershell
setx GEMINI_API_KEY "your-key-here"
```

Then **fully quit and reopen Claude Code**, not just the window. It reads environment variables at startup, so a key set after launch won't be seen.

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
~/.claude/skills/solnest-three-brain/scripts/grok-consult.sh <folder> "your question"
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
Nine times out of ten, Claude Code was already running when you set the key. Quit it completely and reopen. To prove the key is actually in your environment, run `echo $GEMINI_API_KEY` (macOS/Linux) or `echo $env:GEMINI_API_KEY` (PowerShell) in a **fresh** terminal. If that comes back empty, the key never made it into your shell profile.

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

Everything lives in **your** environment: your shell profile, your machine, the CLIs' own credential stores. Nothing is ever written into this skill folder, and nothing here phones home. If you ever want out, delete the `GEMINI_API_KEY` line from your profile, run `!codex logout`, and run `grok logout` if you installed Grok.
