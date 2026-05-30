# Project Docs Bootstrap

[English](README.md) | [简体中文](README.zh-CN.md)

> A Codex skill for bootstrapping durable project documentation and LLM-friendly collaboration rules.

`project-docs-bootstrap` helps agents and maintainers quickly establish a reusable documentation baseline for any repository. It creates concise onboarding docs, project context, an LLM change log, and an optional Git hook that nudges future changes to stay traceable.

This skill is intentionally small: it does not try to become a full documentation platform. It gives every project a practical starting point that humans and coding agents can both follow.


## Why This Exists

AI coding agents work better when a repository has stable orientation material:

- Where should an agent start reading?
- Which commands are safe and useful?
- What project facts must not be guessed?
- When code changes, where should the reasoning and validation be recorded?
- How can future agents avoid repeating the same discovery work?

This skill answers those questions by generating a standard document set and a lightweight change-log enforcement hook.


## What It Generates

By default, the bundled script creates these files in a target repository:

```text
target-repo/
├── AGENTS.md
├── README.md
├── docs/
│   ├── project-context.md
│   └── llm-change-log.md
├── .githooks/
│   └── pre-commit
└── scripts/
    └── check-agents-md-sync.sh
```

Each file has a clear purpose:

- `AGENTS.md`: stable collaboration rules for future agents.
- `README.md`: human-facing entry point for the project.
- `docs/project-context.md`: deeper architecture, workflow, assumptions, and validation context.
- `docs/llm-change-log.md`: reverse-chronological record of model-made changes.
- `.githooks/pre-commit`: delegates to the sync-check script.
- `scripts/check-agents-md-sync.sh`: fails commits that change watched code/config/script paths without staging `docs/llm-change-log.md`.


## When To Use It

Use this skill when you want to:

- Add a clean documentation baseline to an existing repository.
- Prepare a project for AI-assisted development.
- Keep agent instructions short while moving detailed context into docs.
- Create a repeatable pattern for project onboarding across multiple repositories.
- Require model-made code/config/script changes to leave a concise change record.

It is especially useful before handing a project to another agent, teammate, or future version of yourself.


## Installation

Clone or copy this repository into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone <your-repo-url> ~/.codex/skills/project-docs-bootstrap
```

After installation, ask Codex to use the skill:

```text
Use $project-docs-bootstrap to create reusable project onboarding docs and change-log hooks for this repository.
```

You can also run the bundled script directly without invoking the skill workflow.


## Quick Start

Run the generator against a target repository:

```bash
python3 ~/.codex/skills/project-docs-bootstrap/scripts/bootstrap_project_docs.py \
  --target /path/to/repo \
  --project-name "My Project" \
  --summary "A short one-sentence project summary." \
  --stack "Python 3.12 / FastAPI / PostgreSQL" \
  --main-flow "HTTP API -> Service -> Database"
```

The default behavior is non-destructive: existing files are skipped. Use `--dry-run` first if you want to preview the planned writes.

```bash
python3 ~/.codex/skills/project-docs-bootstrap/scripts/bootstrap_project_docs.py \
  --target /path/to/repo \
  --project-name "My Project" \
  --summary "A short one-sentence project summary." \
  --stack "Python 3.12 / FastAPI / PostgreSQL" \
  --main-flow "HTTP API -> Service -> Database" \
  --dry-run
```


## CLI Options

| Option | Purpose |
| --- | --- |
| `--target` | Target repository directory. Defaults to the current directory. |
| `--project-name` | Human-readable project name. Defaults to the target directory name. |
| `--summary` | One-sentence project summary used in generated docs. |
| `--stack` | Short technology stack description. |
| `--main-flow` | Main workflow or runtime chain. |
| `--skip-readme` | Do not create or update `README.md`. |
| `--force` | Overwrite existing generated target files. Use deliberately. |
| `--dry-run` | Print planned writes without changing files. |


## Recommended Workflow

1. Inspect the target repository first:

   ```bash
   pwd
   git status --short
   rg --files
   ```

2. Identify the project facts:

   - one-line purpose
   - tech stack
   - main workflow
   - key directories
   - development, test, and build commands
   - important assumptions and safety notes

3. Run this skill's generator.

4. Replace generated `TODO` placeholders with repository-specific facts.

5. Validate the generated shell scripts and Markdown diff:

   ```bash
   bash -n .githooks/pre-commit
   bash -n scripts/check-agents-md-sync.sh
   git diff --check
   ```

6. Enable the Git hook when you are ready:

   ```bash
   git config core.hooksPath .githooks
   ```


## Safety Model

This project is designed to be conservative by default.

- Existing files are skipped unless `--force` is provided.
- `--dry-run` shows what would be written before any file changes.
- The generated hook only checks staged paths; it does not modify files.
- Sensitive values should not be written into generated docs or change logs.
- Template content is only a starting point. Project-specific facts must be edited in after generation.


## Repository Structure

```text
project-docs-bootstrap/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── document-set.md
└── scripts/
    └── bootstrap_project_docs.py
```

- `SKILL.md`: Codex skill definition and operating workflow.
- `agents/openai.yaml`: display metadata for OpenAI agent interfaces.
- `references/document-set.md`: guidance for each generated document.
- `scripts/bootstrap_project_docs.py`: deterministic generator used by the skill.


## Requirements

- Python 3.9 or newer.
- Git, if you want to use the generated pre-commit hook.
- `bash`, for validating and running the generated hook scripts.


## Contributing

Contributions are welcome if they keep the skill focused, predictable, and easy to audit.

Good contributions usually fall into one of these categories:

- Better generated document wording.
- Safer default checks.
- Additional project-type hints that do not overfit one stack.
- Tests or examples that make the generator easier to trust.
- Documentation improvements for installation and real-world usage.

Please avoid adding broad framework assumptions, project-specific business facts, or hidden network behavior. This skill should stay portable across repositories.


## License

No license file is included yet. Before publishing this repository publicly, add a `LICENSE` file that matches how you want others to use and redistribute the skill.
