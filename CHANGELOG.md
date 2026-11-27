# Changelog

## 1.2.0

- **New way to install: paste this repo's link into Claude Code and say "set this up".** Claude installs the skill, adds the plugins from their makers' own marketplaces, and checks each sign-in. Already have an older copy? Do the same thing once. Your sign-ins stay.
- **Updates install themselves.** Once a day, in the background, from published releases only. If a new release does not start, the old one is put back by itself. An update never touches your sign-ins, your Gemini key, or any file you added. Changes you ask for are kept in `~/.solnest/three-brain/my-instructions.md`.
- **Grok is now an optional fourth brain.** The router can bring in Grok through xAI's own `grok-build@xai-grok-build` plugin: a third review, a critique of how something looks, or whenever you say "ask Grok". Nothing changes if you skip it.
- **New `scripts/grok-consult.sh`.** Grok's read-only mode refuses to start on some Macs (the ones with Docker Desktop), which breaks the plugin's review commands. The script copies your files to a throwaway folder and runs Grok there, so the real project can never be touched.
- **The Gemini key no longer goes through a terminal command.** Setup opens a small file, you paste the key and save. It never appears in the chat. A key you already set by hand keeps working.
- The skill folder is now only the skill. The old setup pages are gone from it.

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
