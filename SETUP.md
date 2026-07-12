# Setup — the two other brains

You only need this file if something stopped working, or if you skipped the guided install. Normally `START-HERE.md` does all of this for you.

The router itself is just text. **The two models it routes to are separate plugins**, and each needs to be installed and signed in. If either one is missing, the router quietly loses that brain.

---

## Codex (GPT) — the second brain

```
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
!codex login
```

Signs in with **any ChatGPT account, including the free tier**, or an OpenAI API key. The login opens a browser.

Check: `/codex:status`

---

## Gemini — the third brain

```
/plugin marketplace add sakibsadmanshajib/gemini-plugin-cc
/plugin install gemini@google-gemini
```

### Gemini needs an API key — Google sign-in no longer works

This is the one thing people get stuck on. Older guides say to run `!gemini` and sign in with your Google account. **That doesn't work any more.** An API key is the only way in.

1. Go to **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)**.
2. Click **Create API key**. It's free, and there's no credit card required.
3. Copy it — it starts with `AIza...`.

Set it so it survives a restart:

**macOS (zsh — the default):**
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

Then **fully quit and reopen Claude Code** — not just the window. It reads environment variables at startup, so a key set after launch won't be seen.

Check: `/gemini:status`

---

## Both brains up?

```
/codex:status
/gemini:status
```

Both ready means the router is live.

---

## Troubleshooting

**`/gemini:status` still says unauthenticated.**
Nine times out of ten, Claude Code was already running when you set the key. Quit it completely and reopen. To prove the key is actually in your environment, run `echo $GEMINI_API_KEY` (macOS/Linux) or `echo $env:GEMINI_API_KEY` (PowerShell) in a **fresh** terminal — if that comes back empty, the key never made it into your shell profile.

**It's telling me to sign in with Google.**
Ignore it. That's stale help text inside the Gemini plugin. Get an API key instead.

**Codex login won't open a browser.**
Run `!codex login` from a normal terminal outside Claude Code, then come back and check `/codex:status`.

**Everything says ready but nothing routes.**
The router only pulls in another model when the situation calls for it — a bug that beat Claude twice, a huge file, a review request. To force it, just ask directly: *"ask all three"*, *"debate this"*, or run `/codex:review`.

---

## Your keys are yours

Both keys live in **your** environment — your shell profile, your machine. They are never written into this skill folder, and nothing here phones home. If you ever want out, delete the `GEMINI_API_KEY` line from your profile and run `!codex logout`.
