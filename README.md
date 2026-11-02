# universal-engineering-standard

The Universal Software Engineering Standard (edition 2026-11-01) as an Agent Skill. `SKILL.md` plus `references/` is the complete standard; there is no separate source document.

- **Scope:** web, mobile, desktop, API, backend, CLI, data, ML, and AI applications.
- **Purpose:** software that is correct, simple, secure, understandable, maintainable, observable, and economical to change.

Plain Markdown in the open Agent Skills format (`SKILL.md` + `references/`), so any agent that loads skills can use it.

## Install

### Personal (all your projects)

Clone once, then link the clone into each agent's skills directory:

```sh
git clone https://github.com/PyModel/universal-engineering-standard.git
cd universal-engineering-standard

# Claude Code
mkdir -p "$HOME/.claude/skills"
ln -sn "$(pwd)" "$HOME/.claude/skills/universal-engineering-standard"

# Codex and other agents that read the shared ~/.agents/skills directory
mkdir -p "$HOME/.agents/skills"
ln -sn "$(pwd)" "$HOME/.agents/skills/universal-engineering-standard"
```

Other agents: link the clone into whatever directory that agent reads skills from (see its docs). `git pull` in the clone updates every link.

Check the target first with `ls -ld <target>`. If a link is already there, `ln -sn` stops with `File exists`; if an older copy is there as a real directory, `ln` puts the new link *inside* it instead. Either way, remove or rename the old entry, then rerun `ln -sn`.

### Project (shared with collaborators)

Commit a copy inside the project, since a symlink into your home directory does not exist on other machines. From the project root, with `DIR` set to the directory your agent reads (`.claude/skills` for Claude Code, `.agents/skills` for Codex):

```sh
DIR=.agents/skills
mkdir -p "$DIR"
git clone --depth 1 https://github.com/PyModel/universal-engineering-standard.git "$DIR/universal-engineering-standard"
rm -rf "$DIR/universal-engineering-standard/.git"
```

## Agents without skill support

Vendor the skill into the project as above, then add this line to the project's `AGENTS.md` (or `CLAUDE.md`, `.cursorrules`, `GEMINI.md`, `.github/copilot-instructions.md`), using the path where you placed it:

```md
Before architecture, pattern, dependency, or infrastructure decisions, audits, or declaring a change done, read `.agents/skills/universal-engineering-standard/SKILL.md` and follow it.
```

## Maintaining the skill

- `python3 scripts/check.py` checks local links and eval case/rubric correspondence; CI also runs the official `skills-ref validate`.
- `evals/` holds the behavioral evaluation corpus and procedure; see [evals/README.md](evals/README.md).
- `evals/`, `scripts/`, and `.github/` are `export-ignore`d, so `git archive HEAD` produces the bare installable skill.

## License

MIT. See [LICENSE](LICENSE).

© 2026 PyModel LLC
