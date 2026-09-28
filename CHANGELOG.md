# Changelog

## 1.2.0

- **Grok Build is now an optional fourth brain.** The router can pull in Grok
  through xAI's official `grok-build@xai-grok-build` plugin: a third independent
  review, visual or design critique of rendered output, or whenever you say
  "ask Grok" or "what does Grok think". Nothing changes if you skip it; Codex and
  Gemini still work exactly as before.
- **New `scripts/grok-consult.sh`.** Grok's read-only sandbox refuses to start on
  some Macs (Docker Desktop's `docker.sock` symlink), which breaks the plugin's
  `review` and `critique` commands. The wrapper copies your files to a throwaway
  folder and runs Grok there in its `workspace` sandbox, so the real project can
  never be touched. `SKILL.md` tells Claude to use it, and never to run Grok
  with no sandbox at all.
- `SETUP.md`, `START-HERE.md`, and `UPDATE.md` walk through the optional Grok
  install and add `/grok-build:check` to the health checks.
- House style pass on all docs.

## 1.1.0

- **START-HERE no longer offers to take the user's Gemini API key in chat.** It
  said "Ask them to paste the key to you, or better, have them run this
  themselves", and a key pasted into a transcript is a leaked key. It now tells
  Claude never to ask, hands over the command with a placeholder for the user to
  fill in themselves, and verifies with `/gemini:status` instead of reading the
  key back. This matches what `SETUP.md` already did correctly.
- Added a `LICENSE` (MIT) to back up the "free to use" line in the README.

## 1.0.0

- First public release.
- Routes between Claude, Codex (GPT), and Gemini, with the two-strike rule that hands a stuck bug to Codex instead of letting Claude guess a third time.
- "Ask all three" and "debate this" consensus modes.
- **Gemini now authenticates with a `GEMINI_API_KEY` from AI Studio.** Signing in with a Google account no longer works, so the setup walks you through getting a free key instead.
