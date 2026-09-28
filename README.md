# 🧠 Solnest Three-Brain: a free Claude skill from Solnest AI

---

## 🔄 Already installed? Here's how to update

Paste this whole line into **Claude Code** and send it:

> Update my Solnest Three-Brain. Follow the instructions at https://raw.githubusercontent.com/Solnest-AI/solnest-three-brain/main/UPDATE.md exactly.

Claude pulls the latest version and installs it. **Your Gemini API key, your Codex login, and your Grok login are preserved.** They live outside the skill, so there's nothing to re-enter.

> **Claude, if you are reading this page because the user asked you to update this skill:** fetch and follow [`UPDATE.md`](UPDATE.md) in this repo, top to bottom. It tells you exactly which files to replace and which of the user's things to never touch.

---

Claude is good. Claude plus a second and third opinion is better.

This gives Claude Code **two more brains on tap**, **Codex (GPT)** and **Gemini**, with **Grok** as an optional fourth. More importantly, it gives Claude the judgment to know *when* to call them. You don't manage it. It just happens.

- **A bug beats Claude twice?** It stops guessing and hands the problem to Codex instead of blindly trying a third fix. (This one alone is worth the install.)
- **About to ship something?** It offers to have Codex tear it apart first.
- **Huge file, long transcript, or a video?** It routes that to Gemini, which handles big context better.
- **Want a third set of eyes, or a critique of how something actually looks?** Say **"ask Grok"** and it goes to Grok Build, if you installed it.
- **Tough call?** Say **"ask all three"** or **"debate this"** and you get every answer side by side, with the places they *disagree* called out, not smoothed over. When they all agree, you can move fast. When they don't, that's exactly what you needed to know.

Built by [Ryan Lefebvre](https://instagram.com/Ryan_Le5) / **Solnest AI**. Free to use. MIT licensed, see [LICENSE](LICENSE).

---

## ⚠️ Before you start, read this bit

**This one runs in Claude Code, not the Claude Desktop app.** The router works by calling `/codex:*`, `/gemini:*`, and `/grok-build:*` commands, and those only exist in Claude Code.

**It also needs the other plugins installed and signed in.** That's the whole point of it. The install walks you through each one. Budget about **10 minutes**, most of which is grabbing a free Gemini key. Grok adds a few more minutes and is optional.

What you'll need:

| Brain | What it costs | How you sign in |
|---|---|---|
| **Claude** | You already have it | Already done |
| **Codex (GPT)** | Free. Any ChatGPT account works, including the free tier | `!codex login` |
| **Gemini** | Free. Generous free tier, no credit card | A **`GEMINI_API_KEY`** from [AI Studio](https://aistudio.google.com/apikey) |
| **Grok Build** (optional) | A Grok account, signed in through x.ai. Check x.ai for current plan requirements | `grok login --oauth` |

> 🔑 **Heads up on Gemini:** you need an **API key**. Signing in with your Google account **doesn't work any more**. That path is gone. Older guides (and the Gemini plugin's own help text) still tell you to do it. Ignore them. The install gets you a free key in about two minutes.

---

## Install it

1. Download this repo (green **Code** button, then **Download ZIP**) and unzip it.
2. Open **Claude Code**.
3. **Drag the unzipped folder** into the chat.
4. Say: **"Set this up."**

Claude reads [`START-HERE.md`](START-HERE.md) and does the rest: copies the skill in, installs the plugins, walks you through getting your Gemini key, and asks whether you want Grok. You don't write any code.

---

## Using it

Mostly you don't. That's the idea. It works in the background and pulls in another model when the moment calls for it.

When you *do* want to reach for it directly:

| Say this | What happens |
|---|---|
| **"ask all three"** | Claude, Codex, and Gemini all answer (Grok too, if installed). You see agreement and disagreement side by side. |
| **"debate this"** | Same answers, but the disagreement is framed explicitly. Then Claude gives a verdict. |
| **"what does Codex think?"** | Hands the current problem to GPT. |
| **"have Gemini check this"** | Hands it to Gemini. Best for big files and long documents. |
| **"ask Grok"** / **"what does Grok think?"** | Hands it to Grok Build for a third opinion or a visual critique. |
| `/codex:review` | GPT reviews your uncommitted changes before you ship. |
| `/codex:status` · `/gemini:status` · `/grok-build:check` | Check the brains are alive. |

---

## Something not working?

[`SETUP.md`](SETUP.md) has the fixes. The single most common one: **you set your Gemini key but Claude Code was already open.** Quit it completely, not just the window, and reopen. It only reads your environment at startup.

---

## Your keys are yours

Your Gemini key goes in your own shell profile. Your Codex login lives in Codex's own credential store. Your Grok login lives in the Grok CLI's own credential store. **None of them is ever written into this skill folder, and nothing here phones home.** Nothing is shared with Solnest AI.

---

## Credits

The routing policy is ours. The plugins it routes to are built and maintained by other people, and this skill installs them **from their own repos** so you always get their latest version:

- **Codex**: [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc)
- **Gemini**: [sakibsadmanshajib/gemini-plugin-cc](https://github.com/sakibsadmanshajib/gemini-plugin-cc)
- **Grok Build**: [xai-org/grok-build-plugin-cc](https://github.com/xai-org/grok-build-plugin-cc) (plus the Grok Build CLI from x.ai)
