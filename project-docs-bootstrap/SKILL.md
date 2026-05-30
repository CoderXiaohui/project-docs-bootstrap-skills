---
name: project-docs-bootstrap
description: Create or refresh reusable project onboarding documents and change-log enforcement scripts for a repository. Use when Codex needs to add AGENTS.md, README.md, docs/project-context.md, docs/llm-change-log.md, .githooks/pre-commit, or scripts/check-agents-md-sync.sh to a project, clone this documentation pattern across projects, or help future vibe-coding agents understand a codebase.
---

# Project Docs Bootstrap

## Workflow

1. Inspect the target repository before writing:
   - `pwd`, `git status --short`, `rg --files`
   - package/build files such as `pom.xml`, `build.gradle`, `package.json`, `pyproject.toml`, `go.mod`
   - existing `README.md`, docs, scripts, hooks, and main source directories
2. Identify the project-specific facts:
   - one-line purpose, tech stack, main workflow, key directories, commands, tests
   - important assumptions, safety notes, sensitive config locations, and known risks
3. Run `scripts/bootstrap_project_docs.py` from this skill to create missing files and hook scripts.
4. Edit generated docs so they describe the target project, not the template project.
5. Validate:
   - `bash -n .githooks/pre-commit`
   - `bash -n scripts/check-agents-md-sync.sh`
   - `git diff --check`
   - run targeted project tests only if source or behavior changed

## Script

Use the bundled script for deterministic file creation:

```bash
python3 /path/to/project-docs-bootstrap/scripts/bootstrap_project_docs.py \
  --target /path/to/repo \
  --project-name "project-name" \
  --summary "one sentence summary" \
  --stack "Java 17 / Spring Boot / MyBatis" \
  --main-flow "API -> Worker -> DB"
```

Default behavior is non-destructive: existing files are skipped. Use `--force` only after confirming overwrite is intended.

Useful options:

- `--skip-readme`: leave an existing or separately managed README untouched.
- `--force`: overwrite generated targets.
- `--dry-run`: print planned writes without changing files.

## Editing Rules

- Never modify a source/template project when the user says it is only a reference.
- Do not copy another project's business facts into the target project. Keep only the document structure and adapt all content.
- Keep `AGENTS.md` concise and rule-focused; put architecture and long explanations in `docs/project-context.md`.
- Keep `docs/llm-change-log.md` reverse chronological and avoid sensitive values.
- Make hook scripts executable after creation.
- If `scripts/**` or `.githooks/**` are created or changed, include the change in `docs/llm-change-log.md`.

## Document Set

Read `references/document-set.md` when deciding what each generated file should contain or when customizing sections for a specific repository.
