# Project Docs Bootstrap

[English](README.en-US.md) | [简体中文](README.md)

> 一个用于初始化项目协作文档、项目上下文和大模型变更记录的 Codex Skill。

`project-docs-bootstrap` 帮助维护者和 AI 编程代理快速为任意仓库建立一套稳定、可复用、可追溯的文档基线。它会生成面向人类与智能体的项目入口文档、协作规则、上下文说明、LLM 变更记录，以及一个可选的 Git 提交前检查 hook。

这个项目刻意保持轻量。它不是大型文档平台，也不试图替代项目管理系统；它只解决一个非常具体的问题：让一个仓库更容易被人和 AI 正确接手。


## 为什么需要它

AI 编程代理在进入一个新仓库时，最容易出问题的地方通常不是代码能力，而是上下文缺失：

- 项目入口应该先读哪里？
- 哪些命令可以安全运行？
- 项目的关键链路是什么？
- 哪些事实不能靠猜？
- 代码、配置或脚本变更后，应该在哪里记录原因、影响和验证方式？
- 下一个代理如何避免重复踩坑？

`project-docs-bootstrap` 用一组固定文档和一个轻量 hook，把这些信息沉淀下来，让后续协作更稳定。


## 核心能力

- 生成标准化项目协作文档集。
- 为目标仓库创建 `AGENTS.md`，保存稳定的智能体协作规则。
- 创建 `docs/project-context.md`，沉淀架构、链路、假设、验证矩阵和风险。
- 创建 `docs/llm-change-log.md`，记录大模型对仓库做过的变更。
- 创建 `.githooks/pre-commit` 和 `scripts/check-agents-md-sync.sh`。
- 当代码、配置、脚本或 hook 发生提交变更时，提醒同步暂存 `docs/llm-change-log.md`。
- 默认非破坏式写入：已有文件会跳过，除非显式使用 `--force`。
- 支持 `--dry-run` 预览写入计划。
- 支持 `--skip-readme` 跳过 README 生成。


## 生成内容

默认情况下，脚本会在目标仓库中生成以下结构：

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

各文件职责如下：

- `AGENTS.md`：面向后续智能体的稳定协作规则。
- `README.md`：面向人类读者的项目入口。
- `docs/project-context.md`：更完整的项目背景、架构、主链路、假设和验证矩阵。
- `docs/llm-change-log.md`：按时间倒序记录大模型变更。
- `.githooks/pre-commit`：提交前检查入口。
- `scripts/check-agents-md-sync.sh`：检查代码、配置、脚本或 hook 变更是否同步记录到 `docs/llm-change-log.md`。


## 适用场景

适合在这些情况下使用：

- 你准备把一个项目交给 AI 编程代理继续开发。
- 你希望多个项目都使用一致的协作文档结构。
- 你想让后续维护者快速理解项目入口、主链路和验证方式。
- 你希望大模型改动有记录、有原因、有验证、有剩余风险说明。
- 你正在整理一个准备开源或长期维护的仓库。

它尤其适合在项目刚开始被 AI 参与维护之前运行一次。


## 安装

把本仓库克隆或复制到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
git clone <你的仓库地址> ~/.codex/skills/project-docs-bootstrap
```

安装后，可以直接让 Codex 使用这个 skill：

```text
Use $project-docs-bootstrap to create reusable project onboarding docs and change-log hooks for this repository.
```

如果不通过 Codex，也可以直接运行内置脚本。


## 快速开始

对目标仓库运行生成器：

```bash
python3 ~/.codex/skills/project-docs-bootstrap/scripts/bootstrap_project_docs.py \
  --target /path/to/repo \
  --project-name "My Project" \
  --summary "一句话说明这个项目的用途。" \
  --stack "Python 3.12 / FastAPI / PostgreSQL" \
  --main-flow "HTTP API -> Service -> Database"
```

建议先用 `--dry-run` 预览写入计划：

```bash
python3 ~/.codex/skills/project-docs-bootstrap/scripts/bootstrap_project_docs.py \
  --target /path/to/repo \
  --project-name "My Project" \
  --summary "一句话说明这个项目的用途。" \
  --stack "Python 3.12 / FastAPI / PostgreSQL" \
  --main-flow "HTTP API -> Service -> Database" \
  --dry-run
```

默认行为是非破坏式的：如果目标文件已经存在，脚本会跳过，不会覆盖。


## 参数说明

| 参数 | 说明 |
| --- | --- |
| `--target` | 目标仓库目录，默认是当前目录。 |
| `--project-name` | 项目名称，默认使用目标目录名。 |
| `--summary` | 项目一句话说明，会写入生成文档。 |
| `--stack` | 项目技术栈简述。 |
| `--main-flow` | 主业务链路或运行链路。 |
| `--skip-readme` | 不创建或更新 `README.md`。 |
| `--force` | 覆盖已存在的目标文件，使用前请确认风险。 |
| `--dry-run` | 只打印计划写入内容，不实际修改文件。 |


## 推荐工作流

1. 先检查目标仓库：

   ```bash
   pwd
   git status --short
   rg --files
   ```

2. 提取项目事实：

   - 项目一句话说明
   - 技术栈
   - 主业务链路
   - 关键目录
   - 开发、测试、构建命令
   - 重要假设、安全注意事项和已知风险

3. 运行生成器。

4. 替换生成文档里的 `TODO` 内容。

5. 校验生成的脚本和 Markdown diff：

   ```bash
   bash -n .githooks/pre-commit
   bash -n scripts/check-agents-md-sync.sh
   git diff --check
   ```

6. 准备启用 hook 时，执行：

   ```bash
   git config core.hooksPath .githooks
   ```


## 安全边界

这个 skill 的默认行为比较保守：

- 已存在文件默认跳过，不覆盖。
- `--dry-run` 可以在写入前查看计划。
- 生成的 hook 只检查暂存文件，不会自动修改内容。
- 文档和变更记录不应该写入密钥、令牌、真实生产配置等敏感信息。
- 生成内容只是模板，必须结合目标仓库真实情况补全。
- `--force` 会覆盖目标文件，使用前应明确确认。


## 仓库结构

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

- `SKILL.md`：Codex skill 定义和执行工作流。
- `agents/openai.yaml`：OpenAI agent 展示元数据。
- `references/document-set.md`：生成文档集的内容边界说明。
- `scripts/bootstrap_project_docs.py`：确定性文档生成脚本。


## 环境要求

- Python 3.9 或更新版本。
- Git：如果需要启用生成的 pre-commit hook。
- `bash`：用于运行和校验生成的 hook 脚本。


## 贡献指南

欢迎提交改进，但建议保持这个 skill 的定位清晰、行为可预测、变更容易审计。

适合贡献的方向包括：

- 优化生成文档的表达。
- 增强默认检查的安全性。
- 增加不过度绑定具体技术栈的项目类型提示。
- 补充测试或示例，让生成器更容易被信任。
- 改进安装、使用和真实场景说明。

请避免引入强业务假设、隐藏网络行为、过度复杂的模板系统，或只适用于单个项目的规则。


