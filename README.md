# Three-Brain

A Solnest AI Skool tool for Claude Code.

Claude is good. Claude with a second and third opinion is better. This gives Claude Code two more models to call on, Codex (GPT) and Gemini, plus Grok if you want it, and the judgment to know when to use them. A bug beats Claude twice? It hands the problem to Codex. A huge file or a long video? That goes to Gemini. On a tough call, say "ask all three" and see every answer side by side, with the disagreements pointed out.

## What you need

- Claude Code, logged in.
- A ChatGPT account for Codex. A free account works.
- A Gemini API key from Google AI Studio. Free, no credit card. Setup walks you through it (2 minutes).
- Optional: a Grok account, for a fourth opinion. Mac and Linux only for now. Check x.ai for what your plan includes.
- Node.js 18 or newer. Setup checks, and tells you where to get it if it is missing.
- About 10 minutes.

## Set it up in 3 steps

1. Copy this page's link.
2. Paste it into Claude Code and say: **set this up**
3. When it is done, give Claude a tough decision and say: **ask all three**

Already have an older copy? Do the same three steps. Your sign-ins stay as they are.

## What to say

| Say this | What happens |
|---|---|
| **ask all three** | Claude, Codex and Gemini each answer. You see where they agree and where they do not. |
| **debate this** | Same answers, with the disagreement laid out, then Claude gives a verdict. |
| **what does Codex think?** | Hands the current problem to GPT. |
| **have Gemini check this** | Hands it to Gemini. Best for big files and long documents. |
| **ask Grok** | A third reviewer, if you added Grok. |

Most of the time you say nothing. It works in the background and brings in another model when the moment calls for it.

## Good to know

- Updates install themselves. Once a day, when Claude Code starts, the tool quietly moves to the newest release. You never have to ask.
- An update never wipes your own changes. Your sign-ins, your Gemini key and any change you asked Claude to make to how this tool works stay exactly as they are.
- Your keys are yours. The Gemini key sits in a file on your computer. Codex and Grok keep their own sign-ins. Nothing is sent to Solnest AI.
- Want it to work differently? Just tell Claude ("always ask Codex before I ship"). It remembers.
- Something not working? Say "fix my Three-Brain setup" and Claude runs the checks again.

## Credits

The routing rules are ours (MIT, see [LICENSE](LICENSE)). The plugins it calls are made by other people. Setup installs each one from its maker's own source, so you always get their latest version:

- Codex: [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc)
- Gemini: [sakibsadmanshajib/gemini-plugin-cc](https://github.com/sakibsadmanshajib/gemini-plugin-cc)
- Grok: [xai-org/grok-build-plugin-cc](https://github.com/xai-org/grok-build-plugin-cc), plus the Grok Build tool from x.ai

## Support

hello@solnestai.com

---

Claude: someone pasted this link and said "set this up" (or asked to update or fix their copy). Read [CLAUDE.md](https://raw.githubusercontent.com/Solnest-AI/solnest-three-brain/main/CLAUDE.md) in this repo and follow its SETUP section, one step per message. You run the commands yourself. Never ask for a key in chat.
