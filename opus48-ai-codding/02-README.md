# Opus48 AI 编程工作流

> **版本**：V2.2  
> **核心理念**：Matt Pocock Agent Skills + Loop Engineering  
> **设计原则**：极简、艺术、先理解再动手、在聪明区工作  
> **适用场景**：任何编程项目（Java/SpringBoot 优先支持）

**V2.3 更新**：新增原型图→业务梳理→PRD 流程，支持从设计稿开始开发

---

## 🎨 理念

> 「编码如同作画：意在笔先，一笔一划皆有节奏。」

### 三大原则

1. **先 Grill，再动手**：充分理解后才写代码，用问题澄清代替猜测
2. **在聪明区工作**：保持在 120K tokens 以内，需要时用 Handoff 分流
3. **垂直切片，TDD 循环**：一次切一个完整故事，红 → 绿 → 重构，慢就是快

---

## 🗺️ 全景图

```
                     ┌─────────────────────────────────────┐
                     │  1. /triage - 画布整理              │
                     │     （梳理 backlog，标记 AFK/HITL）  │
                     └────────────────┬────────────────────┘
                                      │
                                      ▼
                     ┌─────────────────────────────────────┐
                     │  2. /grill-with-docs - 对齐共识      │
                     │     （无情提问，建立 CONTEXT.md）    │
                     └────────────────┬────────────────────┘
                                      │
              ┌───────────────────────┴─────────────────────────┐
              │                                                   │
              ▼                                                   ▼
    ┌──────────────────────┐      ╔══════════════════════════════════════╗
    │  /handoff + /prototype│      ║  3. /to-prd - 定稿草图               ║
    │   （需要原型时）       │      ║     （固化共识，寻找深模块机会）      ║
    └──────────────────────┘      ╚═════════════════╦════════════════════╝
                                              ┌─────────┘
                                              ▼
                              ╔══════════════════════════════════════╗
                              ║  4. /to-issues - 垂直切片              ║
                              ║     （曳光弹先行，标记 AFK/HITL）      ║
                              ╚═════════════════╦════════════════════╝
                                              ┌─────────┘
                                              ▼
              ┌───────────────────────────────┴───────────────────────────────┐
              │                                                               │
              ▼                                                               ▼
    ╔══════════════════════════════════╗        ┌─────────────────────────────────┐
    ║  5. /implement - 一条龙           ║        │  分开走：/tdd + /codex-review  │
    ║     （TDD + 审查一步完成）        │        │     （灵活控制每一步）         │
    ╚═════════════════╦════════════════╝        └─────────────────┬───────────────┘
                      └───────────────────────┬───────────────────┘
                                              ▼
                              ┌─────────────────────────────────────┐
                              │  6. /improve-architecture - 深化    │
                              │     （不要重写，要让模块变深）        │
                              └────────────────┬────────────────────┘
                                              │
                                              ▼
                              ┌─────────────────────────────────────┐
                              │  7. /doc-rot - 月度巡检            │
                              │     （检查腐化，回触前面步骤）      │
                              └─────────────────────────────────────┘
```

---

## 📁 目录结构

```
opus48-ai-codding/
├── 00-NAVIGATION.md               # [AI专用] 路由表 + 通用规则（AI第一个读）
├── 01-AI-REFERENCE.md            # [AI专用] AI使用参考手册（不知道怎么做时看这个）
├── 02-README.md                  # [人类用] 本文件（全景图 + 导航）
├── 03-QUICKSTART.md              # [人类用] 快速开始（新手路径 + 老项目接入）
├── 04-CHECKLIST.md               # [速查] 完整检查清单
├── 05-WORKFLOW.md               # [人类用] 完整工作流调用指南（新！）
├── 06-CONTEXT.md                 # [项目用] 共享语言模板（复制到项目根目录）
├── skills/                        # 12 个 Skill（按顺序）
│   ├── 01-triage.md               # 画布整理
│   ├── 02-grill-with-docs.md      # 对齐共识
│   ├── 02.5-prototype-to-business.md # 原型转业务梳理（新！）
│   ├── 03-handoff.md              # 上下文接力
│   ├── 04-prototype.md            # 草稿探索
│   ├── 05-to-prd.md               # 定稿草图（支持业务梳理文档）
│   ├── 06-to-issues.md            # 垂直切片
│   ├── 07-tdd.md                 # 红→绿→重构
│   ├── 08-codex-review.md        # 画布审查
│   ├── 09-improve-architecture.md # 深化模块
│   ├── 10-doc-rot.md             # 月度巡检
│   └── 11-implement.md           # 实现一条龙
├── templates/                     # 脚手架模板（复制即用）
│   ├── README.md                  # 模板使用说明
│   ├── CONTEXT.md.template        # 共享语言模板
│   ├── grill-report.md.template   # Grill 报告模板
│   ├── prd.md.template            # PRD 模板
│   ├── business-analysis.md.template # 业务梳理文档模板（新！）
│   ├── issues.md.template         # Issue 清单模板（旧格式）
│   ├── issues-readme.md.template  # Issue 总览模板（新格式）
│   ├── single-issue.md.template   # 单个 GitHub-style Issue 模板
│   ├── todo.md.template           # TODO 项模板
│   └── implement-report.md.template # Implement 报告模板
└── examples/sample-project/       # 完整示例项目
    ├── README.md                  # 示例说明
    ├── CONTEXT.md                 # 示例共享语言
    ├── docs/
    │   ├── business/...           # 示例业务梳理文档（新！）
    │   ├── prd/...                # 示例 PRD
    │   ├── issues/...             # 示例 Issue 清单（旧 + 新格式）
    │   ├── todos/...              # 示例 TODO 列表
    │   └── reports/...            # 示例报告
    └── src/models/...             # 示例代码 + 测试
```

---

## 🚀 从这里开始

| 你是谁 | 先看哪里 |
|-------|---------|
| **AI** | 00-NAVIGATION.md → 01-AI-REFERENCE.md |
| **新手** | 03-QUICKSTART.md → 05-WORKFLOW.md → examples/sample-project/ |
| **老手** | 02-README.md → 05-WORKFLOW.md → 04-CHECKLIST.md |
| **老项目接入** | 03-QUICKSTART.md → "老项目接入路径" |
| **想看完整流程** | 05-WORKFLOW.md（新！） |

---

## 📚 核心概念（快速参考）

### 聪明区 vs 变笨区

- **聪明区**：0–120K tokens —— AI 专注、有创造力、能深度推理
- **变笨区**：> 120K tokens —— AI 注意力分散、开始编造假想、决策质量下降

**怎么办**：用 `/handoff` 分流，保持每个会话纯粹。

### 深模块 vs 浅模块

- **深模块**：简单接口 + 丰富实现 —— 调用者不用知道里面在做什么
- **浅模块**：接口复杂 + 实现简单 —— 调用者要知道所有细节才能用

**目标**：每个月让几个模块变深。

### 垂直切片 vs 水平切片

- **垂直切片**：用户可以端到端做一件事（如「创建订单并看到在列表中」）
- **水平切片**：只做一层（如「先写数据库层，再写 API 层」）

**永远用垂直切片**：一次一个完整故事，能独立验证，能快速交付价值。

### AFK vs HITL

- **AFK**（Away From Keyboard）：Agent 可以自己做完，不需要人盯着
- **HITL**（Human In The Loop）：需要人在关键节点做决策

**规则**：简单 = AFK，复杂/涉及设计 = HITL。

---

### GitHub-style Issue 格式（新）

V2.2 新增支持 GitHub 风格的单个 Issue 文件：

- **旧格式**：所有 issue 在一个清单文件中（`docs/issues/{功能名}-{YYYY-MM-DD}.md`）
- **新格式**：每个 issue 独立文件 + 总览 README（`docs/issues/{功能名}-{YYYY-MM-DD}/`）

**新格式特点**：
- 每个 issue 一个文件：`001-{标题}.md`、`002-{标题}.md`...
- GitHub 兼容的 frontmatter（title、labels、assignees、created）
- 状态跟踪（pending/in-progress/blocked/done）
- TODO 关联支持（明确标记哪个 TODO 阻塞了哪个 issue）
- 历史记录（记录状态变更）

**TODO 跟踪**：
- 单独的 `docs/todos/` 目录
- 每个 TODO 一个文件，记录需要确认的问题
- 明确标记 TODO 阻塞的 issue

---

## 💡 一句话总结

> **充分理解，垂直切片，TDD 循环，每月深化。**
