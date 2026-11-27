---
name: solnest-three-brain
description: >-
  Solnest Three-Brain, a multi-model router for Claude Code. Use when a coding
  task would benefit from a second model: getting another opinion ("ask all
  three", "what does Codex think", "have Gemini check this", "ask Grok", "what
  does Grok think", "consult Codex and Grok"), running an adversarial review,
  breaking a stalemate after Claude has failed a fix twice, handling a
  huge-context job (large files, long docs, video), or comparing models head to
  head ("debate this", "consensus"). Routes between Claude (primary), Codex/GPT,
  Gemini, and optionally Grok, using the codex@openai-codex, gemini@google-gemini,
  and grok-build@xai-grok-build plugins.
---

# Solnest Three-Brain Router

## Your own changes (read first, every time)

Before anything else, read `~/.solnest/three-brain/my-instructions.md` if it exists and
follow it. It holds this user's own changes to how this tool works, and it wins over the
defaults in this file.

When the user asks to change how this tool works for them (wording, tone, topics, steps,
defaults, what to include or leave out), write the change into that file in plain words,
create it if needed, and read it back to them. **Never edit this tool's own files for
that.** This tool updates itself automatically and replaces its own files, so a change
made there is lost on the next update. Their sign-ins are never touched by an update
either: the Gemini key file (`~/.solnest/three-brain/.env`, or a key already in their
shell profile), the Codex and Grok logins, and the three plugins all live outside this
skill folder.

## What this is

Claude is the default driver. Codex (GPT) and Gemini are on tap through their plugins, and Grok Build can be wired in as an optional fourth. This skill is the routing policy that decides when to pull one of them in, plus the consensus and debate modes.

The underlying commands come from the installed plugins:

- **Codex:** `/codex:rescue`, `/codex:review`, `/codex:adversarial-review`, `/codex:status`, `/codex:setup`
- **Gemini:** `/gemini:rescue`, `/gemini:review`, `/gemini:adversarial-review`, `/gemini:status`, `/gemini:setup`
- **Grok (optional):** `/grok-build:check`, `/grok-build:review`, `/grok-build:critique`, `/grok-build:delegate`, `/grok-build:runs`, `/grok-build:show`, `/grok-build:stop`. These come from xAI's official `grok-build@xai-grok-build` plugin plus the Grok Build CLI (`grok`). If neither is installed, skip every Grok step below. The router works fine with two extra brains.

`rescue` delegates a task to that model and returns its output verbatim. `review` runs that model against local git state. This skill orchestrates them. It does not replace them.

## Routing policy: who gets the task

**Claude (default):** everything, unless one of the cases below applies. Building, editing, refactoring, explaining, normal review.

**Codex / GPT, pull in when:**

- A bug has resisted **two** Claude attempts (see the two-strike rule below).
- You want an adversarial second pair of eyes on a finished change: `/codex:review` or `/codex:adversarial-review`.
- The problem is subtle reasoning or algorithmic, where a different model is likely to catch what Claude missed.
- Route with `/codex:rescue <what to investigate or fix>`.

**Gemini, pull in when:**

- **Huge context:** very large files, long transcripts or docs, or a whole-repo sweep where Gemini's context window helps.
- **Multimodal input:** images, video, PDFs.
- Cheap, fast lookups where spending Gemini quota beats spending Claude turns.
- Route with `/gemini:rescue <task>`.

**Grok, pull in when (only if it is installed):**

- You want a third independent review on top of Codex.
- Visual or design critique of rendered output: screenshots, exported images, PDFs. In our testing, Grok Build with file access measured real pixels and re-ran code, on par with Codex.
- The user asks for it by name: "ask Grok", "what does Grok think".
- Route with the wrapper script below, or `/grok-build:review` against git state.

## Grok: read this before calling it

**Grok's `read-only` and `strict` sandboxes can refuse to start on macOS** when `/var/run/docker.sock` is a symlink (Docker Desktop sets it up that way). The plugin's `review` and `critique` commands hardcode `--sandbox read-only` and auto-approve every tool call, so on an affected machine they fail with `could not apply the 'read-only' sandbox profile`. Do NOT work around it by running Grok with no sandbox: headless runs auto-approve everything, so the sandbox is the only safety boundary.

**Use the wrapper for consults and reviews:**

```bash
bash ~/.claude/skills/solnest-three-brain/scripts/grok-consult.sh <source_dir> "<question>" [output_file]
```

It copies `<source_dir>` to a throwaway temp folder and runs Grok there with `--sandbox workspace` (read anywhere, write only inside the copy), so the real project cannot be touched. The copy is deleted when the run ends.

- `/grok-build:check` only probes auth and works everywhere. If it says Grok is not authenticated, the fix is `grok login --oauth` (opens a browser). Afterwards `grok models` should print "logged in with grok.com".
- `/grok-build:delegate` is write-capable and runs with NO sandbox by the plugin's design. Only use it in a git worktree or a disposable copy, never on a live repo.

## Two-strike rule (the important one)

When Claude is fixing a specific bug or failing test and **two consecutive attempts** don't resolve it:

1. Stop. Don't attempt a third blind fix.
2. Say so plainly: "Two strikes on this. Handing it to Codex."
3. Run `/codex:rescue <concise description of the bug, what was tried, and the error>`.
4. Report Codex's findings, then let Claude apply the fix.

Two failed attempts on the *same* problem is the trigger, not two unrelated bugs.

## Auto-offer review after a build

After completing a non-trivial code change (a new feature, a multi-file edit, anything shippable), offer once:

> "Want Codex to review this before you ship? (`/codex:review`)"

Offer once. Don't nag. Skip it for trivial one-liners.

## Consensus and debate modes

**"Ask all three" / "consensus":** Give Claude's own answer, then run `/codex:rescue <question>` and `/gemini:rescue <question>` on the same prompt. If Grok is installed, run `grok-consult.sh` on the same question as well. Lay the answers side by side and call out where they agree and where they diverge. Agreement across the board means high confidence. Divergence gets flagged, never papered over.

**"Debate this":** Same answers, but frame the *disagreement* explicitly: what each model argues and why. Then give Claude's reasoned verdict on which is right.

For both modes, prefer `--background` on the rescue calls when the question is heavy, so the runs don't block each other.

## Direct passthrough

You can always skip the router and hit a model directly with `/codex:*`, `/gemini:*`, or `/grok-build:*`. This skill is for when the *routing decision itself* is the value. Otherwise just run the command.

## If a model isn't ready

If a rescue or review reports that the model is missing or unauthenticated, stop and fix the auth. Don't silently fall back to Claude-only without saying so.

- **Codex** signs in with a ChatGPT account (any tier, including Free) or an OpenAI API key: run `!codex login`, or `/codex:setup` to check.
- **Gemini** needs a **`GEMINI_API_KEY`**. Check with `bash ~/.claude/skills/solnest-three-brain/scripts/gemini-key.sh status` (it never prints the key). Get one free at [aistudio.google.com/apikey](https://aistudio.google.com/apikey). Never ask for the key in chat and never print it: `gemini-key.sh open` opens the key file for the user to paste into, and `gemini-key.sh apply` switches it on. The steps are in `SETUP.md` in this skill folder.

  Warning: **interactive `gemini` CLI sign-in with a Google account no longer works.** If Gemini reports itself unauthenticated, do **not** tell the user to run `!gemini` and sign in. That path is dead. The API key is the only way in. Point them at `SETUP.md` in this skill folder.
- **Grok** (optional) signs in with `grok login --oauth`, then `/grok-build:check` confirms it. If the Grok Build CLI or plugin was never installed, say so once and carry on with Codex and Gemini. Setup steps are in `SETUP.md`.
