[日本語](README.md) | **English**

# claude-code-life

> An AI-native framework for running "your whole life as a single repository" with Claude Code (template).

Journal, self-analysis, project management, and ideas — collected into one repository designed so that **the primary reader is AI, not humans** — and operated through purpose-specific Claude Code skills (agents).

Design write-up (in Japanese) → [Repositories aren't written for humans — running journaling, investing, and parenting on Claude Code (overview)](https://zenn.dev/takotyan00/articles/claude-code-life-repository)

## Concept

- **The primary reader is AI**: documents are structured for an AI's search and cross-referencing, not for human readability. One fact per file, metadata in frontmatter, and filenames chosen for "can the AI find this later?" above all.
- **Bundle onto one foundation**: instead of scattering across separate tools, everything lives in one repository so context is shared. The more you build, the stronger the base gets.
- **Multi-agent operation**: each skill reads the same knowledge base, and one skill's output becomes another's input.

## Structure

```
.
├── CLAUDE.md                         # Shared-instruction template for Claude Code
├── journal/                          # Dialogue-style journal (year/month/day.md)
├── ideas/                            # Idea stock
├── projects/                         # Per-project metadata
├── persona/                          # Dialogue-based persona (self-analysis)
└── .claude/
    ├── config/context.example.yaml   # Template for the context all skills share
    ├── rules/                        # Behavioral rules injected into the agents
    └── skills/                       # Per-purpose agents (/journal, /weekly-review, /persona)
```

## What's included (the scope of this template)

- `CLAUDE.md` — shared-instruction template for Claude Code
- `.claude/skills/` — three skills (generic versions): dialogue journal / weekly review / persona building
- `.claude/rules/` — methodology rules (mcp-vs-skills) + dialogue-behavior rules (unknown-term-lookup) + format templates
- `.claude/rules/correction-rules/` — correction rules that keep the AI from misreading you, with one generalized example (`example-understated-expression.md`) to copy from
- `.claude/config/context.example.yaml` — template for the context all skills share
- `journal/` `ideas/` `projects/` `persona/` — each directory's role is explained in its README

## Getting started

1. Clone this repository (or use it as a template).
2. Copy `.claude/config/context.example.yaml` to `.claude/config/context.yaml` in the same place, and fill in your own interests and projects.
3. Launch `/journal`, `/weekly-review`, or `/persona` in Claude Code.
4. Adjust `CLAUDE.md`, `rules`, and `skills` to fit how you operate.

## Not yet included (rolled out over time)

- **More correction rules** — one generalized example already ships (see `.claude/rules/correction-rules/`); the rest contain personal examples, so they're generalized and added over time. The thinking behind them is covered in the article above and its sequels.
- Domain-specific skills such as finance and hobby recommendations.
- Peripheral skills like `/trend` (trend collection) and `/improve` (environment tuning) — not shipped in this template. The `sources` / `improvement_backlog` fields in `context.yaml` are left in as scaffolding for when you add them yourself.

## Privacy

Personal data — journals, self-analysis, real names, asset figures — is **not included in this repository**. When you run your own copy, separate sensitive information into `*.local.md` (git-ignored), or keep the repository private.

## License

[MIT](./LICENSE)
