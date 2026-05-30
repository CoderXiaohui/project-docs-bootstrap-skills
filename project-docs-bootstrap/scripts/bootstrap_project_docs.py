#!/usr/bin/env python3
"""Create reusable project onboarding docs and sync-check hooks."""

from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default=".", help="Target repository directory")
    parser.add_argument("--project-name", default=None, help="Human-readable project name")
    parser.add_argument("--summary", default=None, help="One-sentence project summary")
    parser.add_argument("--stack", default="TODO: fill project tech stack", help="Short tech stack")
    parser.add_argument("--main-flow", default="TODO: fill main workflow", help="Main workflow chain")
    parser.add_argument("--skip-readme", action="store_true", help="Do not create/update README.md")
    parser.add_argument("--force", action="store_true", help="Overwrite existing target files")
    parser.add_argument("--dry-run", action="store_true", help="Print planned writes only")
    return parser.parse_args()


def write_file(path: Path, content: str, *, force: bool, dry_run: bool, executable: bool = False) -> str:
    if path.exists() and not force:
        return f"skip existing {path}"
    if dry_run:
        return f"would write {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if executable:
        mode = path.stat().st_mode
        path.chmod(mode | 0o111)
    return f"wrote {path}"


def agents_md(project_name: str, main_flow: str) -> str:
    return f"""# AGENTS.md

只放稳定协作规则；业务背景看 `README.md` 与 `docs/project-context.md`。

## 项目

- 名称：`{project_name}`
- 链路：`{main_flow}`
- 首读：`README.md`、`docs/project-context.md`、主要入口类/模块、核心服务、测试目录

## 命令

- `TODO: fill dev command`
- `TODO: fill test command`
- `TODO: fill build command`

说明：优先最小验证；依赖真实环境、密钥或外部服务时，明确说明未执行原因。

## 规则

- 改核心链路时，同步检查入口、服务、数据访问层和对应测试。
- 改实体、schema、Mapper、迁移或序列化契约时，同步检查读写两端。
- 改配置、脚本、hook 或 CI 时，同步检查本地命令和文档。
- 敏感配置不要写入文档、日志、测试快照或提交说明。
- 测试样例放在仓库测试资源目录，不要新增本机绝对路径。

## 文档

- 目标：`AGENTS.md` 保持短规则，详细背景下沉到 `docs/project-context.md`。
- 读取 `docs/llm-change-log.md` 时默认只读前 120 行；必要时才扩大范围。
- 改 `src/**`、核心配置、构建文件、`scripts/**`、`.githooks/**` 时，结束前更新 `docs/llm-change-log.md`。
- 协作规则、关键命令或文档结构变化时，再同步更新 `AGENTS.md`。

## 交付

- 最终说明必须写：改动文件、验证、剩余风险或待办。
- 触发文档规则时，明确写：`已同步更新 docs/llm-change-log.md`；如适用，再写：`已同步更新 AGENTS.md`。
"""


def readme_md(project_name: str, summary: str, stack: str, main_flow: str) -> str:
    return f"""# {project_name}

{summary}

## 技术栈

`{stack}`

## 主链路

```text
{main_flow}
```

## 常用命令

- `TODO: fill dev command`
- `TODO: fill test command`
- `TODO: fill build command`

## 主要目录

- `TODO: path`：说明

## 文档

- `AGENTS.md`：协作规则
- `docs/project-context.md`：详细架构、链路、假设和测试矩阵
- `docs/llm-change-log.md`：大模型变更记录

## 注意事项

- `TODO: fill critical caution`
"""


def project_context_md(project_name: str, summary: str, stack: str, main_flow: str) -> str:
    return f"""# 项目背景与实现上下文

本文档面向需要快速理解项目内部工作方式的人和智能体。稳定协作规则请看根目录 `AGENTS.md`，变更历史请看 `docs/llm-change-log.md`。

## 1. 项目一句话说明

{summary}

## 2. 技术栈

`{stack}`

## 3. 关键目录

```text
{project_name}/
├── TODO: fill source directories
└── docs/
```

## 4. 主业务链路

```text
{main_flow}
```

## 5. 关键模块职责

- `TODO: module`：说明

## 6. 数据模型 / 外部契约

- `TODO: table/api/queue`：说明

## 7. 当前重要假设

- `TODO: assumption`

## 8. 常用验证矩阵

- `TODO: test command`：适用场景

## 9. 已知风险 / 待办

- `TODO: risk`
"""


def change_log_md(today: str) -> str:
    return f"""# 大模型变更记录

本文档专门记录大模型对本仓库做出的新增、修改、重构与规则调整。稳定协作规则请看根目录 `AGENTS.md`。

记录原则：

- 按时间倒序追加
- 每次只写清楚“为什么改、改了什么、影响哪里、怎么验证、还剩什么风险”
- 不在这里扩散敏感配置的真实值

---

## {today} 建立大模型协作文档

### 背景

为了让后续大模型更快理解项目，需要建立稳定协作规则、项目上下文和变更记录。

### 本次改动

- 新增 `AGENTS.md`
- 新增或更新 `README.md`
- 新增 `docs/project-context.md`
- 新增 `docs/llm-change-log.md`
- 新增 `.githooks/pre-commit`
- 新增 `scripts/check-agents-md-sync.sh`

### 影响文件

- `AGENTS.md`
- `README.md`
- `docs/project-context.md`
- `docs/llm-change-log.md`
- `.githooks/pre-commit`
- `scripts/check-agents-md-sync.sh`

### 行为变化

- 项目新增面向大模型协作的文档入口
- 安装 `.githooks` 后，提交代码、配置、脚本或 hook 变更时，需要同步暂存 `docs/llm-change-log.md`
- 应用运行逻辑不变

### 验证

- `bash -n .githooks/pre-commit`
- `bash -n scripts/check-agents-md-sync.sh`
- `git diff --check`

### 风险 / 待办

- 如需启用提交前检查，执行 `git config core.hooksPath .githooks`
"""


def pre_commit() -> str:
    return """#!/usr/bin/env bash
set -euo pipefail

"$(git rev-parse --show-toplevel)/scripts/check-agents-md-sync.sh"
"""


def sync_script() -> str:
    return """#!/usr/bin/env bash
set -euo pipefail

staged_files="$(git diff --cached --name-only --diff-filter=ACMR)"

if [ -z "${staged_files}" ]; then
  exit 0
fi

watched_regex='^(src/|pom\\.xml$|package\\.json$|pyproject\\.toml$|go\\.mod$|Cargo\\.toml$|src/main/resources/|scripts/|\\.githooks/)'

if printf '%s\n' "${staged_files}" | grep -Eq "${watched_regex}"; then
  if ! printf '%s\n' "${staged_files}" | grep -Eq '^docs/llm-change-log\\.md$'; then
    echo "检测到代码、配置、脚本或 hook 变更，但未同步更新 docs/llm-change-log.md"
    echo "请至少补充：背景、本次改动、影响文件、行为变化、验证、风险/待办"
    exit 1
  fi
fi

exit 0
"""


def main() -> int:
    args = parse_args()
    target = Path(args.target).expanduser().resolve()
    project_name = args.project_name or target.name
    summary = args.summary or f"{project_name} project. TODO: replace with one-sentence purpose."
    today = dt.date.today().isoformat()

    files: list[tuple[Path, str, bool]] = [
        (target / "AGENTS.md", agents_md(project_name, args.main_flow), False),
        (target / "docs" / "project-context.md", project_context_md(project_name, summary, args.stack, args.main_flow), False),
        (target / "docs" / "llm-change-log.md", change_log_md(today), False),
        (target / ".githooks" / "pre-commit", pre_commit(), True),
        (target / "scripts" / "check-agents-md-sync.sh", sync_script(), True),
    ]
    if not args.skip_readme:
        files.insert(1, (target / "README.md", readme_md(project_name, summary, args.stack, args.main_flow), False))

    for path, content, executable in files:
        print(write_file(path, content, force=args.force, dry_run=args.dry_run, executable=executable))

    if not args.dry_run:
        print("next: customize TODO sections, then run bash -n scripts and git diff --check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
