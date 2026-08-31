# Changelog

## 1.1.0

- **START-HERE no longer offers to take the user's Gemini API key in chat.** It
  said "Ask them to paste the key to you, or better, have them run this
  themselves" — and a key pasted into a transcript is a leaked key. It now tells
  Claude never to ask, hands over the command with a placeholder for the user to
  fill in themselves, and verifies with `/gemini:status` instead of reading the
  key back. This matches what `SETUP.md` already did correctly.
- Added a `LICENSE` (MIT) to back up the "free to use" line in the README.


## 1.0.0

- First public release.
- Routes between Claude, Codex (GPT), and Gemini — with the two-strike rule that hands a stuck bug to Codex instead of letting Claude guess a third time.
- "Ask all three" and "debate this" consensus modes.
- **Gemini now authenticates with a `GEMINI_API_KEY` from AI Studio.** Signing in with a Google account no longer works, so the setup walks you through getting a free key instead.
