---
name: solnest-three-brain
description: >-
  Solnest Three-Brain — a multi-model router for Claude Code. Use when a coding
  task would benefit from a second model: getting another opinion ("ask all
  three", "what does Codex think", "have Gemini check this"), running an
  adversarial review, breaking a stalemate after Claude has failed a fix twice,
  handling a huge-context job (large files, long docs, video), or comparing
  models head to head ("debate this", "consensus"). Routes between Claude
  (primary), Codex/GPT, and Gemini using the codex@openai-codex and
  gemini@google-gemini plugins.
---

# Solnest Three-Brain Router

Claude is the default driver. Codex (GPT) and Gemini are on tap through their plugins. This skill is the routing policy that decides when to pull one of them in, plus the consensus and debate modes.

The underlying commands come from two installed plugins:

- **Codex:** `/codex:rescue`, `/codex:review`, `/codex:adversarial-review`, `/codex:status`, `/codex:setup`
- **Gemini:** `/gemini:rescue`, `/gemini:review`, `/gemini:adversarial-review`, `/gemini:status`, `/gemini:setup`

`rescue` delegates a task to that model and returns its output verbatim. `review` runs that model against local git state. This skill orchestrates them — it does not replace them.

## Routing policy — who gets the task

**Claude (default):** everything, unless one of the cases below applies. Building, editing, refactoring, explaining, normal review.

**Codex / GPT — pull in when:**

- A bug has resisted **two** Claude attempts (see the two-strike rule below).
- You want an adversarial second pair of eyes on a finished change → `/codex:review` or `/codex:adversarial-review`.
- The problem is subtle reasoning or algorithmic, where a different model is likely to catch what Claude missed.
- Route with `/codex:rescue <what to investigate or fix>`.

**Gemini — pull in when:**

- **Huge context:** very large files, long transcripts or docs, or a whole-repo sweep where Gemini's context window helps.
- **Multimodal input:** images, video, PDFs.
- Cheap, fast lookups where spending Gemini quota beats spending Claude turns.
- Route with `/gemini:rescue <task>`.

## Two-strike rule (the important one)

When Claude is fixing a specific bug or failing test and **two consecutive attempts** don't resolve it:

1. Stop. Don't attempt a third blind fix.
2. Say so plainly: "Two strikes on this — handing it to Codex."
3. Run `/codex:rescue <concise description of the bug, what was tried, and the error>`.
4. Report Codex's findings, then let Claude apply the fix.

Two failed attempts on the *same* problem is the trigger — not two unrelated bugs.

## Auto-offer review after a build

After completing a non-trivial code change (a new feature, a multi-file edit, anything shippable), offer once:

> "Want Codex to review this before you ship? (`/codex:review`)"

Offer once. Don't nag. Skip it for trivial one-liners.

## Consensus and debate modes

**"Ask all three" / "consensus":** Give Claude's own answer, then run `/codex:rescue <question>` and `/gemini:rescue <question>` on the same prompt. Lay the three answers side by side and call out where they agree and where they diverge. Agreement across all three means high confidence. Divergence gets flagged, never papered over.

**"Debate this":** Same three answers, but frame the *disagreement* explicitly — what each model argues and why — then give Claude's reasoned verdict on which is right.

For both modes, prefer `--background` on the rescue calls when the question is heavy, so the runs don't block each other.

## Direct passthrough

You can always skip the router and hit a model directly with `/codex:*` or `/gemini:*`. This skill is for when the *routing decision itself* is the value. Otherwise just run the command.

## If a model isn't ready

If `/codex:rescue` or `/gemini:rescue` reports that the model is missing or unauthenticated, stop and fix the auth — don't silently fall back to Claude-only without saying so.

- **Codex** signs in with a ChatGPT account (any tier, including Free) or an OpenAI API key: run `!codex login`, or `/codex:setup` to check.
- **Gemini** needs a **`GEMINI_API_KEY`** in the environment. Get one free at [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

  ⚠️ **Interactive `gemini` CLI sign-in with a Google account no longer works.** If Gemini reports itself unauthenticated, do **not** tell the user to run `!gemini` and sign in — that path is dead. The API key is the only way in. Point them at `SETUP.md` in this skill folder.
