# Project Documentation Set

Use this reference when customizing generated files for a target project.

## AGENTS.md

Purpose: stable collaboration rules for future agents.

Keep:

- project main chain in one line
- first files/classes to read
- common commands
- rules for risky modules
- documentation update rules
- final delivery checklist

Avoid:

- long architecture explanations
- stale milestone history
- secrets or environment-specific values

## README.md

Purpose: human and agent entry point.

Recommended sections:

- one-line project summary
- tech stack
- main workflow diagram
- common commands
- primary API/CLI usage
- key directories
- database/setup notes when relevant
- links to docs
- critical cautions

## docs/project-context.md

Purpose: detailed implementation context.

Recommended sections:

- one-line purpose
- directory tree
- main business/runtime flows
- key class/module responsibilities
- data model or external contracts
- important assumptions
- validation matrix
- known risks and TODOs

## docs/llm-change-log.md

Purpose: trace model-made changes.

Entry template:

```markdown
## YYYY-MM-DD Short Title

### 背景

### 本次改动

### 影响文件

### 行为变化

### 验证

### 风险 / 待办
```

## .githooks/pre-commit

Purpose: delegate to the sync-check script:

```bash
#!/usr/bin/env bash
set -euo pipefail

"$(git rev-parse --show-toplevel)/scripts/check-agents-md-sync.sh"
```

## scripts/check-agents-md-sync.sh

Purpose: fail commits that change code/config/scripts/hooks without also staging `docs/llm-change-log.md`.

Default watched paths:

- `src/`
- `pom.xml`
- `package.json`
- `pyproject.toml`
- `go.mod`
- `Cargo.toml`
- `src/main/resources/`
- `scripts/`
- `.githooks/`
