# universal-engineering-standard

The Universal Software Engineering Standard (edition 2026-11-01) as an Agent Skill. `SKILL.md` plus `references/` is the complete standard; there is no separate source document.

- **Scope:** web, mobile, desktop, API, backend, CLI, data, ML, and AI applications.
- **Purpose:** software that is correct, simple, secure, understandable, maintainable, observable, and economical to change.

Plain Markdown in the open Agent Skills format (`SKILL.md` + `references/`), so any agent that loads skills can use it.

## Install

Copy or symlink this folder into your agent's skills directory, for example:

```sh
ln -s "$PWD/universal-engineering-standard" ~/.claude/skills/   # Claude Code (user)
ln -s "$PWD/universal-engineering-standard" .claude/skills/     # Claude Code (project)
```

Other agents: place the folder wherever that agent reads skills from (see its docs).

## Agents without skill support

Add this line to the repo's `AGENTS.md` (or `CLAUDE.md`, `.cursorrules`, `GEMINI.md`, `.github/copilot-instructions.md`):

```md
Before architecture, pattern, dependency, or infrastructure decisions, audits, or declaring a change done, read `universal-engineering-standard/SKILL.md` and follow it.
```

© 2026 PyModel LLC
