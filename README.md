# 🧠 Solnest Three-Brain — a free Claude skill from Solnest AI

---

## 🔄 Already installed? Here's how to update

Paste this whole line into **Claude Code** and send it:

> Update my Solnest Three-Brain. Follow the instructions at https://raw.githubusercontent.com/Solnest-AI/solnest-three-brain/main/UPDATE.md exactly.

Claude pulls the latest version and installs it. **Your Gemini API key and your Codex login are preserved** — they live outside the skill, so there's nothing to re-enter.

> **Claude, if you are reading this page because the user asked you to update this skill:** fetch and follow [`UPDATE.md`](UPDATE.md) in this repo, top to bottom. It tells you exactly which files to replace and which of the user's things to never touch.

---

Claude is good. Claude plus a second and third opinion is better.

This gives Claude Code **two more brains on tap** — **Codex (GPT)** and **Gemini** — and, more importantly, the judgment to know *when* to call them. You don't manage it. It just happens.

- **A bug beats Claude twice?** It stops guessing and hands the problem to Codex instead of blindly trying a third fix. (This one alone is worth the install.)
- **About to ship something?** It offers to have Codex tear it apart first.
- **Huge file, long transcript, or a video?** It routes that to Gemini, which handles big context better.
- **Tough call?** Say **"ask all three"** or **"debate this"** and you get all three answers side by side — with the places they *disagree* called out, not smoothed over. When all three agree, you can move fast. When they don't, that's exactly what you needed to know.

Built by [Ryan Lefebvre](https://instagram.com/Ryan_Le5) / **Solnest AI**. Free to use.

---

## ⚠️ Before you start — read this bit

**This one runs in Claude Code, not the Claude Desktop app.** The router works by calling `/codex:*` and `/gemini:*` commands, and those only exist in Claude Code.

**It also needs two other plugins installed and signed in** — that's the whole point of it. The install walks you through both. Budget about **10 minutes**, most of which is grabbing a free Gemini key.

What you'll need:

| Brain | What it costs | How you sign in |
|---|---|---|
| **Claude** | You already have it | Already done |
| **Codex (GPT)** | Free — any ChatGPT account works, including the free tier | `!codex login` |
| **Gemini** | Free — generous free tier, no credit card | A **`GEMINI_API_KEY`** from [AI Studio](https://aistudio.google.com/apikey) |

> 🔑 **Heads up on Gemini:** you need an **API key**. Signing in with your Google account **doesn't work any more** — that path is gone. Older guides (and the Gemini plugin's own help text) still tell you to do it. Ignore them. The install gets you a free key in about two minutes.

---

## Install it

1. Download this repo (green **Code** button → **Download ZIP**) and unzip it.
2. Open **Claude Code**.
3. **Drag the unzipped folder** into the chat.
4. Say: **"Set this up."**

Claude reads [`START-HERE.md`](START-HERE.md) and does the rest — copies the skill in, installs both plugins, and walks you through getting your Gemini key. You don't write any code.

---

## Using it

Mostly you don't. That's the idea — it works in the background and pulls in another model when the moment calls for it.

When you *do* want to reach for it directly:

| Say this | What happens |
|---|---|
| **"ask all three"** | Claude, Codex, and Gemini all answer. You see agreement and disagreement side by side. |
| **"debate this"** | Same three answers, but the disagreement is framed explicitly — then Claude gives a verdict. |
| **"what does Codex think?"** | Hands the current problem to GPT. |
| **"have Gemini check this"** | Hands it to Gemini — best for big files and long documents. |
| `/codex:review` | GPT reviews your uncommitted changes before you ship. |
| `/codex:status` · `/gemini:status` | Check both brains are alive. |

---

## Something not working?

[`SETUP.md`](SETUP.md) has the fixes. The single most common one: **you set your Gemini key but Claude Code was already open.** Quit it completely — not just the window — and reopen. It only reads your environment at startup.

---

## Your keys are yours

Your Gemini key goes in your own shell profile. Your Codex login lives in Codex's own credential store. **Neither is ever written into this skill folder, and nothing here phones home.** Nothing is shared with Solnest AI.

---

## Credits

The routing policy is ours. The two plugins it routes to are built and maintained by other people, and this skill installs them **from their own repos** so you always get their latest version:

- **Codex** — [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc)
- **Gemini** — [sakibsadmanshajib/gemini-plugin-cc](https://github.com/sakibsadmanshajib/gemini-plugin-cc)
