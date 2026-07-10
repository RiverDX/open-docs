# Opus48 工作流调用指南

> **版本**：V2.3
> **目的**：完整的端到端调用流程，从想法到代码

---

## 📋 目录

- [全景流程](#-全景流程)
- [阶段 1：理解阶段](#-阶段-1理解阶段)
- [阶段 2：需求固化阶段](#-阶段-2需求固化阶段)
- [阶段 3：实现阶段](#-阶段-3实现阶段)
- [阶段 4：优化阶段](#-阶段-4优化阶段)
- [常见调用模式](#-常见调用模式)
- [文件结构约定](#-文件结构约定)

---

## 🌆 全景流程

### 模式 A：从想法开始（旧流程）
```
想法阶段
   │
   │ 有 backlog 需要整理 → /triage
   │
   │ 需求不明确 → /grill-with-docs
   │
   ↓ 共识已达成

需求固化阶段
   │
   ├─→ 写 PRD → /to-prd
   │     ↓
   │   docs/prd/{功能名}-{YYYY-MM-DD}.md
   │
   └─→ 拆 Issue → /to-issues
         ↓
   docs/issues/{功能名}-{YYYY-MM-DD}/
   ├── README.md（总览 + 状态看板）
   ├── 001-{标题}.md（单个 Issue）
   ├── 002-{标题}.md
   └── ...

实现阶段
   │
   ├─→ 选一个 Issue（从 001 曳光弹开始）
   │     ↓
   │   有问题阻塞 → 创建 TODO
   │     ↓
   │   docs/todos/todo-{YYYY-MM-DD}-001-{标题}.md
   │
   ├─→ 一条龙实现 → /implement
   │     或
   ├─→ 分步走 → /tdd → /codex-review
   │
   ↓ Issue 完成，更新状态为 done

优化阶段
   │
   ├─→ 深化架构 → /improve-architecture
   │
   └─→ 月度巡检 → /doc-rot
```

---

### 模式 B：从原型图开始（新流程，推荐）
```
原型图 + 简要描述
   │
   ↓ 【新增】/prototype-to-business
   │
   docs/business/{功能名}-{YYYY-MM-DD}.md（业务梳理文档）
   │
   ↓ /grill-with-docs（可选，对齐共识）
   │
   CONTEXT.md（可选更新）
   │
   ↓ /to-prd（模式 B：从业务梳理文档生成）
   │
   docs/prd/{功能名}-{YYYY-MM-DD}.md（PRD）
   │
   ↓ /to-issues → Issues
   │
   ↓ /implement → 实现
```

---

## 🧠 阶段 1：理解阶段

### 📌 场景 A：有 backlog 需要整理

#### 调用 `/triage`

**输入**：
```
我有这些 issue 需要整理：
1. 用户登录后页面白屏
2. 加个导出 Excel 的功能
3. 这个 API 怎么用？
4. 更新一下 README
```

**输出**：
- `docs/reports/triage-{YYYY-MM-DD}.md` - Triage 报告
- 如果是新格式 issue，更新 frontmatter 的 labels

**关键动作**：
- 分类：bug / enhancement / question / docs
- 打状态标签：needs-triage / needs-info / ready-for-agent / ready-for-human / wontfix
- 标记 AFK/HITL
- 排序优先级

---

### 📌 场景 B：有原型图，需要生成业务梳理文档和架构图

#### 调用 `/prototype-to-business`

**输入**：
```
这是原型图描述 + 需求简要说明：
[原型图描述，或者截图说明]
需求简要说明：用户可以创建任务、更新状态、删除任务、按优先级筛选
```

**输出**：
- `docs/business/{功能名}-{YYYY-MM-DD}.md` - 业务梳理文档

#### 调用 `/archify`（可选，生成架构图）

**输入**：
```
用 archify 画这个系统的架构图：
React 前端 → Node API → PostgreSQL 数据库 → Redis 缓存
用户登录时调用认证服务
```

**输出**：
- `docs/diagrams/architecture-{YYYY-MM-DD}.html` - 可交互的架构图

---

### 📌 场景 C：需求不明确，需要对齐共识

#### 调用 `/grill-with-docs`

**输入**：
```
我想做个任务管理工具，大概就是能创建任务、更新状态...

[提供现有代码（如果有）]
```

**输出**：
- `CONTEXT.md` - 共享语言（项目根目录）
- `docs/reports/grill-{YYYY-MM-DD}.md` - Grill 报告

**关键问题**：
1. **目标层**：我们解决什么？为谁解决？
2. **概念层**：核心概念是什么？确切含义？
3. **边界层**：什么在范围内？什么不做？
4. **异常层**：边界情况怎么处理？

**记住**：不要跳过这一步！Grill 越充分，后面返工越少。

---

### 📌 场景 C：有原型图+简要描述（新流程）

#### 调用 `/prototype-to-business`

**输入**：
```
这是原型图和简要描述：

原型图：
[描述原型图，或提供图片链接]

简要描述：
[用户提供的简要描述]
```

**输出**：
- `docs/business/{功能名}-{YYYY-MM-DD}.md` - 业务梳理文档

**业务梳理文档包含**：
- 用户角色
- 业务流程（正常+异常）
- 功能清单
- 数据需求
- 界面描述
- 验收标准（初稿）
- 风险点
- 待确认问题

**下一步选择**：
- 如果还有不清楚的 → `/grill-with-docs`
- 如果已经清晰 → `/to-prd`（选择模式 B：从业务梳理文档生成）

---

## 📝 阶段 2：需求固化阶段

### 📌 步骤 1：写 PRD

#### 调用 `/to-prd`

**支持两种模式**：

##### 模式 A：从 CONTEXT.md 生成（旧方式）

**输入**：
```
我们刚才 Grill 完了，CONTEXT.md 在这里：
[读取 CONTEXT.md 的内容]

帮我生成 PRD。
```

**输出**：
- `docs/prd/{功能名}-{YYYY-MM-DD}.md` - PRD 文档

**PRD 包含**：
- 问题陈述
- 用户故事（作为 [角色]，我可以 [动作]，以便 [价值]）
- 验收标准
- 模块设计
- 深模块机会

---

##### 模式 B：从业务梳理文档生成（推荐，新方式）

**输入**：
```
业务梳理文档在这里：
[读取 docs/business/{功能名}-{YYYY-MM-DD}.md 的内容]

帮我生成 PRD。
```

**输出**：
- `docs/prd/{功能名}-{YYYY-MM-DD}.md` - PRD 文档

**PRD 包含**：
- 问题陈述（从业务梳理提炼）
- 用户故事（从功能清单转换）
- 验收标准（从业务梳理完善）
- 模块设计（从数据需求识别）
- 深模块机会

---

### 📌 步骤 2：拆 Issue

#### 调用 `/to-issues`

**输入**：
```
PRD 在这里：
[读取 docs/prd/{功能名}-{YYYY-MM-DD}.md 的内容]

帮我拆成 issue。
```

**输出**（双格式，向后兼容）：
1. **旧格式**（可选）：`docs/issues/{功能名}-{YYYY-MM-DD}.md`
2. **新格式**（推荐）：
   ```
   docs/issues/{功能名}-{YYYY-MM-DD}/
   ├── README.md（总览 + 状态看板）
   ├── 001-{标题}.md（单个 Issue）
   ├── 002-{标题}.md
   ├── 003-{标题}.md
   └── ...
   ```

**关键原则**：
- ✅ **垂直切片**：每个 issue 都是端到端的完整故事
- ✅ **曳光弹先行**：Issue 001 是最小但完整的
- ✅ **标记 AFK/HITL**：区分 AI 能做的和需要人的
- ✅ **明确依赖**：说明依赖哪些 issue

**Issue 001（曳光弹）示例**：
```markdown
---
title: "[Enhancement] 用户可以创建任务并看到在列表中"
labels: enhancement, HITL, P0, status/pending
assignees: ''
created: 2026-06-28
---

# Issue 001：用户可以创建任务并看到在列表中

> **状态**：🟣 pending
> **优先级**：P0
> **类型**：enhancement
> **AFK/HITL**：HITL
> **依赖**：无
> **阻塞的 TODO**：无
> **对应 PRD**：[任务管理系统](../prd/task-management-2026-06-28.md)

## 目标
用户可以创建任务（只传标题），然后在任务列表中看到它。

## 验收标准
- [ ] 调用 `createTask("买牛奶")` 可以创建任务
- [ ] 调用 `getTasks()` 可以看到刚创建的任务
- [ ] 任务有唯一 ID
- [ ] 任务状态是 `todo`
```

---

## 💻 阶段 3：实现阶段

### 📌 前置检查：Issue 状态

从 Issue 总览选择下一个要实现的 issue：
```
docs/issues/{功能名}-{YYYY-MM-DD}/README.md
```

**从 Issue 001（曳光弹）开始！**

---

### 📌 场景 X：有问题阻塞 Issue → 创建 TODO

当 issue 被某个问题阻塞时：

**创建 TODO 文件**：
```markdown
---
title: "确定持久化方案"
labels: todo, status/open, P1
created: 2026-06-28
---

# TODO：确定持久化方案

> **状态**：🔴 open
> **优先级**：P1
> **阻塞的 Issue**：#002, #003

## 描述
当前曳光弹用内存存储，但后续功能需要决定是否持久化。

## 需要确认的问题
- [ ] 任务数据需要持久化吗？
- [ ] 如果需要，用什么方式？（数据库/本地存储/文件）

## 建议解决方案
先继续用内存存储做曳光弹，验证后再决定。
```

**更新被阻塞的 Issue**：
```markdown
> **状态**：🚧 blocked
> **阻塞的 TODO**：[todo-2026-06-28-001](../todos/todo-2026-06-28-001-确定持久化方案.md)
```

---

### 📌 选项 A：一条龙实现（推荐）

#### 调用 `/implement`

**输入**：
```
实现这个 Issue：
[读取 docs/issues/{功能名}-{YYYY-MM-DD}/001-{标题}.md 的内容]

CONTEXT.md 在这里：
[读取 CONTEXT.md]
```

**输出**：
- `{测试目录}/{模块}.test.{ext}` - 测试代码
- `{源代码目录}/{模块}.{ext}` - 实现代码
- `docs/reports/implement-{issue}-{YYYY-MM-DD}.md` - Implement 报告
- **自动更新 Issue 状态**：pending → in-progress → done

**自动状态更新**：
- 开始时：状态从 🟣 pending → 🔵 in-progress，添加历史记录
- 完成时：状态从 🔵 in-progress → ✅ done，添加历史记录

---

### 📌 选项 B：分步走（更细致控制）

#### 步骤 1：调用 `/tdd`

**输入**：
```
开始实现这个 Issue：
[读取 docs/issues/{功能名}-{YYYY-MM-DD}/001-{标题}.md 的内容]

CONTEXT.md 在这里：
[读取 CONTEXT.md]
```

**输出**：
- `{测试目录}/{模块}.test.{ext}` - 测试代码
- `{源代码目录}/{模块}.{ext}` - 实现代码
- `docs/reports/tdd-{issue}-{YYYY-MM-DD}.md` - TDD 报告
- **自动更新 Issue 状态**：pending → in-progress

**TDD 循环**：
1. 🔴 红：写一个失败的测试（只一个！）
2. 🟢 绿：写刚好让测试通过的代码（不要过度设计！）
3. 🟠 重构：改进设计，保持测试通过（可选）
4. 重复：下一个测试

---

#### 步骤 2：调用 `/codex-review`

**输入**：
```
这是刚才写的代码，帮我审查一下：
[读取 {源代码目录}/{模块}.{ext}]
[读取 {测试目录}/{模块}.test.{ext}]
```

**输出**：
- `docs/reports/codex-review-{YYYY-MM-DD}.md` - 审查报告

**检查 6 维度**：
1. 违反约定？
2. 明显的 bug？
3. 测试覆盖？
4. 设计/架构？
5. 性能/资源？
6. 可维护性？

**问题分级**：
- **SEV-1**：必须修复
- **SEV-2**：建议修复
- **SEV-3**：可选改进

---

#### 步骤 3：更新 Issue 状态为 done

如果 `/tdd` 没有自动更新，手动更新：
```markdown
> **状态**：✅ done

---

## 历史记录

| 日期 | 状态变更 | 说明 |
|------|---------|------|
| 2026-06-28 | created → pending | Issue 创建 |
| 2026-06-28 | pending → in-progress | 开始 TDD 实现 |
| 2026-06-28 | in-progress → done | 实现完成，所有测试通过 |
```

---

### 📌 实现下一个 Issue

回到 Issue 总览：
```
docs/issues/{功能名}-{YYYY-MM-DD}/README.md
```

选择下一个 issue，重复上面的步骤！

---

## 🔧 阶段 4：优化阶段

### 📌 场景 A：深化架构

#### 调用 `/improve-architecture`

**输入**：
```
这个模块写得有点乱，帮我看看怎么改进：
[读取 {源代码目录}/{模块}.{ext}]
```

**输出**：
- `docs/reports/improve-architecture-{YYYY-MM-DD}.md` - 架构改进建议

**关键原则**：
- ❌ 不要重写！
- ✅ 渐进式改进
- ✅ 找深模块机会（简单接口 + 丰富实现）

---

### 📌 场景 B：月度巡检

#### 调用 `/doc-rot`

**输入**：
```
月底了，帮我做一次 doc-rot 巡检。
```

**输出**：
- `docs/reports/doc-rot-{YYYY-MM-DD}.md` - 巡检报告
- 健康度评分（0-100）

---

## 🎯 常见调用模式

### 📌 模式 1：完整新功能（推荐路径）

```
1. /grill-with-docs        ← 理解需求
   ↓
   CONTEXT.md

2. /to-prd                 ← 写 PRD
   ↓
   docs/prd/{功能名}-{YYYY-MM-DD}.md

3. /to-issues              ← 拆 Issue
   ↓
   docs/issues/{功能名}-{YYYY-MM-DD}/README.md
   docs/issues/{功能名}-{YYYY-MM-DD}/001-{标题}.md
   docs/issues/{功能名}-{YYYY-MM-DD}/002-{标题}.md
   ...

4. /implement              ← 实现 Issue 001（曳光弹）
   ↓
   代码 + 测试 + 报告
   Issue 状态：pending → in-progress → done

5. /implement              ← 实现 Issue 002
   ↓
   ...重复直到所有 Issue 完成...

6. /improve-architecture   ← 优化架构（可选）

7. /doc-rot                ← 月度巡检（每月一次）
```

---

### 📌 模式 2：快速修复 bug

```
1. /triage                 ← 整理 issue（可选）

2. /grill-with-docs        ← 理解问题（如果不明确）

3. /implement              ← 直接实现（一条龙）
   或
   /tdd → /codex-review
```

---

### 📌 模式 3：老项目接入

```
1. /doc-rot                ← 先做一次巡检，了解现状

2. /grill-with-docs        ← 建立共享语言

3. 新功能用完整流程：
   /to-prd → /to-issues → /implement

4. 每周：/improve-architecture

5. 每月：/doc-rot
```

---

## 📁 文件结构约定

### 完整项目结构

```
项目根目录/
├── 00-NAVIGATION.md              ← 不要复制，这是 Opus48 项目的
├── 01-AI-REFERENCE.md           ← 不要复制
├── 02-README.md                 ← 不要复制
├── 03-QUICKSTART.md             ← 不要复制
├── 04-CHECKLIST.md              ← 不要复制
├── 05-WORKFLOW.md              ← 不要复制（本文件）
├── 06-CONTEXT.md               ← 模板，复制到你的项目
├── CLAUDE.md
├── CONTEXT.md                   ← 你的项目共享语言
├── README.md                    ← 你的项目 README
├── skills/                      ← 不要复制
├── templates/                   ← 不要复制
├── examples/                    ← 不要复制
│
├── docs/                        ← 你的项目文档
│   ├── prd/
│   │   └── {功能名}-{YYYY-MM-DD}.md
│   │
│   ├── issues/
│   │   ├── {功能名}-{YYYY-MM-DD}/     ← 新格式（推荐）
│   │   │   ├── README.md
│   │   │   ├── 001-{标题}.md
│   │   │   ├── 002-{标题}.md
│   │   │   └── ...
│   │   └── {功能名}-{YYYY-MM-DD}.md    ← 旧格式（可选）
│   │
│   ├── todos/
│   │   ├── README.md
│   │   ├── todo-{YYYY-MM-DD}-001-{标题}.md
│   │   ├── todo-{YYYY-MM-DD}-002-{标题}.md
│   │   └── ...
│   │
│   └── reports/
│       ├── grill-{YYYY-MM-DD}.md
│       ├── triage-{YYYY-MM-DD}.md
│       ├── tdd-{issue}-{YYYY-MM-DD}.md
│       ├── implement-{issue}-{YYYY-MM-DD}.md
│       ├── codex-review-{YYYY-MM-DD}.md
│       ├── improve-architecture-{YYYY-MM-DD}.md
│       └── doc-rot-{YYYY-MM-DD}.md
│
├── src/                         ← 你的源代码
│   ├── models/
│   │   ├── {模块}.{ext}
│   │   └── {模块}.test.{ext}
│   └── ...
│
└── ...
```

---

## 📖 快速参考卡片

### Skill 选择速查

| 你想做什么 | 调用哪个 Skill |
|-----------|---------------|
| 理解代码生成文档 | `/grill-with-docs` |
| 根据简要需求生成 PRD | `/grill-with-docs` → `/to-prd` |
| 根据 PRD 拆分任务 | `/to-issues` |
| 开始实现（一条龙） | `/implement` |
| 开始实现（分步） | `/tdd` → `/codex-review` |
| 审查代码 | `/codex-review` |
| 优化架构 | `/improve-architecture` |
| 整理 backlog | `/triage` |
| 探索想法 | `/prototype` |
| 会话太长 | `/handoff` |
| 月度巡检 | `/doc-rot` |

---

### Issue 状态速查

| Emoji | 状态 | 说明 |
|-------|------|------|
| 🟣 | pending | 待开始 |
| 🔵 | in-progress | 进行中（`/tdd` 或 `/implement` 自动设置） |
| 🚧 | blocked | 被阻塞（被 TODO 或其他 issue） |
| ✅ | done | 已完成（`/tdd` 或 `/implement` 自动设置） |

---

### TODO 状态速查

| Emoji | 状态 | 说明 |
|-------|------|------|
| 🔴 | open | 待解决 |
| 🟢 | resolved | 已解决 |
| ⚫ | closed | 已关闭 |

---

## ⚠️ 重要提醒

### 🔴 绝对不要做

1. ❌ 跳过 Grill 直接写代码
2. ❌ 水平切片（先做数据库层，再做 API 层）
3. ❌ 一次写 10 个测试，再写实现
4. ❌ 测试私有方法
5. ❌ 重写（而不是渐进式改进）

### 🟡 小心做

1. ⚠️ 不要过度设计
2. ⚠️ 不要追求完美（80% 清楚就可以开始）
3. ⚠️ 不要让会话超过 120K tokens（接近变笨区就用 `/handoff`）

### 🟢 一定要做

1. ✅ 先 Grill，再动手
2. ✅ 垂直切片（每个 issue 都是端到端的完整故事）
3. ✅ 测试先行（红→绿→重构）
4. ✅ 曳光弹先行（从最小但完整的功能开始）
5. ✅ 通过公开接口测试
6. ✅ 在聪明区工作（< 120K tokens）

---

## 🎉 开始吧！

选择适合你的模式，从第一个 Skill 开始：

- **新手**：从 `03-QUICKSTART.md` 开始
- **老手**：从 `02-README.md` 开始
- **AI 专用**：从 `00-NAVIGATION.md` 开始
- **需要参考**：看 `01-AI-REFERENCE.md`

祝使用愉快！✨
