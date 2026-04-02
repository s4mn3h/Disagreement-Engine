# Disagreement-Engine
Minimal adversarial self-review for LLM outputs — two API calls, two voices, one catches what the other misses.
# Disagreement Engine

A minimal Python tool that catches AI overconfidence by running every query through two adversarial voices — one that answers, one that challenges.

## Why This Exists

A single LLM responding to a query has no internal mechanism for checking its own work. It generates the most plausible-sounding response and presents it with uniform confidence regardless of whether it's correct.

The Disagreement Engine runs the same query through two differently-instructed instances. Voice One answers the question directly and states its confidence level. Voice Two receives both the question and Voice One's answer, then attempts to find errors, overstatements, missing context, and unjustified confidence. The output is both responses, side by side.

This is not a novel idea in principle — adversarial review is standard in science, law, and engineering. What's uncommon is applying it to LLM outputs as a default workflow rather than an occasional check.

## What It Catches

- **Overconfident claims** in domains where the model's training data is thin
- **Missing context** that changes the practical meaning of a technically correct answer
- **Unstated assumptions** baked into the answer that the user might not share
- **Logical gaps** between evidence cited and conclusions drawn

## What It Doesn't Catch

- Errors where both voices share the same systematic bias (same model, same training data)
- Factual errors where the underlying data is wrong, not the reasoning
- Adversarial manipulation specifically designed to fool both voices

These limitations are real and documented here intentionally. A future version using two different models (not just two different prompts) would address the shared-bias problem at the cost of higher complexity and compute.

## Usage

```bash
# Set your API key (one time)
# Windows:  setx ANTHROPIC_API_KEY "your-key-here"
# Mac/Linux: export ANTHROPIC_API_KEY="your-key-here"

python disagreement_engine.py
```

Edit the `question` variable in the script to test different queries. The script prints both voices' responses sequentially.

## How It Works

```
User Question
     │
     ▼
┌─────────────┐
│  Voice One  │ ── Answers directly, states confidence level
│  (Answerer) │
└──────┬──────┘
       │ answer
       ▼
┌─────────────┐
│  Voice Two  │ ── Receives question + Voice One's answer
│ (Challenger)│    Finds errors, challenges weak reasoning
└──────┬──────┘
       │ challenge
       ▼
  Both outputs
  printed for
  human review
```

Two API calls. That's it. The human decides what to do with the disagreement.

## Design Decisions

**Why two voices, not three or more?**
Two is the minimum viable disagreement. It catches a meaningful percentage of errors at minimum cost (two API calls). Adding a third voice (adjudicator) is a natural extension but triples the cost and adds complexity. Start with two, measure what it catches, decide if a third voice addresses a demonstrated gap.

**Why same model with different prompts, not different models?**
Simplicity and cost. Two calls to one API versus managing two different API integrations. The tradeoff is that same-model voices share systematic biases — if Claude consistently gets something wrong, both voices will miss it. This is a known limitation, not an overlooked one. A production version should use heterogeneous models.

**Why does the human make the final call?**
Because automated resolution reintroduces the single-process problem. If a third model adjudicates between Voice One and Voice Two, that adjudicator has its own biases and can't reliably evaluate its own judgment. Human review keeps the loop open and maintains accountability.

## Example Output

```
============================================================
QUESTION: Is nuclear energy the safest form of power generation?
============================================================

--- VOICE ONE (Answerer) ---

By deaths per unit of energy produced, nuclear energy has the lowest
mortality rate of any major power source, including wind and solar...
[states evidence, concludes with Confidence: High]

--- VOICE TWO (Challenger) ---

The answer is technically defensible but frames safety narrowly.
"Safest" by deaths-per-TWh is one metric. If safety includes...
[challenges framing, notes missing context about waste storage
and catastrophic tail risk, assesses confidence as partially
justified for the narrow claim but overstated for the broad one]
```

## Background

This tool is part of a broader architecture I'm developing around AI error reduction through functional separation. The core principle: the process that generates an output should not be the sole process that evaluates that output. Related concepts include a [clarification intermediary layer](link) for reducing input ambiguity and a confidence calibration tracker for measuring accuracy by domain over time.

I developed these concepts through systems analysis in early 2026, working from a trades and industrial background rather than formal CS. The thinking overlaps with several patterns in Anthropic's published agent architecture research (evaluator-optimizer pattern, multi-agent orchestration) and alignment work (Constitutional AI's use of one model to evaluate another).

## Roadmap

- [ ] Add logging — record every query, both responses, and eventual ground truth when available
- [ ] Confidence calibration — feed logged accuracy data back into Voice One's prompt
- [ ] Heterogeneous models — Voice One and Voice Two use different providers
- [ ] Resolution layer — optional third voice that synthesizes disagreements (with human override)
- [ ] Domain-specific challenger prompts — different challenge strategies for medical, technical, financial queries

## License

MIT
