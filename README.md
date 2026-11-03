# Persona

A collection of **advisor agents**. Each one is modeled on a real expert's public body of work: books, frameworks, interviews and podcasts. You can ask an agent for advice and get it in that expert's way of thinking.

Each persona is built from a research dossier. The dossier records what the expert has actually said and taught, how sure we are of each claim, and where the evidence is disputed. The agent prompt is then derived from the dossier. The agents never claim to *be* the real person. They are simulations of a public point of view.

## Agents

| Agent | Modeled on | Good for | Files |
|---|---|---|---|
| **Chase** | Chase Hughes: behavior profiler, author of *The Ellipsis Manual*, *Six-Minute X-Ray* and *The Behavior Ops Manual* | Authority and confidence, influence and persuasion, reading people, negotiation and sales, spotting and resisting manipulation, planning how to reach an outcome with another person | [`personas/chase/`](personas/chase/) |

## How to use an agent

### In Claude Code
Every persona is also registered as a Claude Code subagent in [`.claude/agents/`](.claude/agents/). From this repo, ask for it by name:

```
> Ask Chase how I should handle asking my boss for a raise next week.
```

or be explicit: `Use the chase agent to …`. You can also run `/agents` to see it listed. The subagent reads its system prompt and dossier from `personas/<name>/` on each run, so it always uses the current version.

### In any other chatbot (Claude.ai Projects, ChatGPT Custom GPTs, etc.)
1. Paste the contents of `personas/<name>/system-prompt.md` into the system prompt or "instructions" field.
2. Optionally upload `personas/<name>/profile.md` as a knowledge file. The agent then has the full dossier to draw on.

## Repository layout

```
personas/
  _template/            # copy this to start a new persona
  chase/
    profile.md          # deep research dossier (the "source of truth")
    system-prompt.md    # portable agent prompt derived from the dossier
    FACTCHECK.md        # how the dossier was verified, and what changed
tools/
  quotecheck.py         # check quotes against downloaded transcripts
.claude/agents/
  chase.md              # Claude Code subagent wrapper (loads the files above)
```

## Adding a new persona
1. Copy `personas/_template/` to `personas/<name>/`.
2. Research the expert and fill in `profile.md`. Cite every claim and mark how confident you are in it.
3. Write `system-prompt.md` from the profile. Keep it self-contained so it can be pasted anywhere.
4. Add `.claude/agents/<name>.md`, modeled on `chase.md`.
5. Add a row to the table above.

## Ground rules for every persona
- **Simulation, not impersonation.** Agents describe themselves as advisors *modeled on* a person's public work. They never claim to be that person and never invent private facts about them.
- **Faithful but honest.** Agents advise the way the expert would. Where the expert's claims go beyond the evidence (for example, body-language lie detection), the agent says so.
- **No harm.** Agents will explain manipulation tactics so you can recognize and resist them. They will not coach coercive control, deception that harms someone, or covert manipulation of a specific person against their interests.
