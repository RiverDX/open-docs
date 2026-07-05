# 示例项目：任务管理系统

> 展示 Opus48 工作流的完整应用：从想法 → 实现

---

## 📚 本示例包含的内容

```
sample-project/
├── README.md                    # 本文档
├── CONTEXT.md                   # 共享语言（由 /grill-with-docs 生成）
├── docs/
│   ├── reports/
│   │   ├── grill-2026-06-28.md  # Grill 报告
│   │   ├── implement-create-task-2026-06-28.md  # Implement 报告
│   │   └── codex-review-2026-06-28.md  # 审查报告
│   ├── prd/
│   │   └── task-management-2026-06-28.md  # PRD
│   └── issues/
│       └── task-management-2026-06-28.md  # Issue 清单
└── src/                        # 示例代码
    ├── models/
    │   ├── Task.js
    │   └── Task.test.js
    └── index.js
```

---

## 🎯 项目背景

我们要做一个简单的**任务管理系统**，用来展示 Opus48 工作流的完整应用。

---

## 📖 完整流程记录

### 第 1 步：/grill-with-docs —— 对齐共识

**启动原因**：有想法但需求不清晰，概念需要澄清。

**核心问题**：
1. 我们解决什么问题？为谁解决？
2. 核心概念是什么？（Task、Status、Priority）
3. 边界在哪里？什么在范围内？什么不做？
4. 异常场景有哪些？

**输出**：
- `CONTEXT.md` —— 共享语言
- `docs/reports/grill-2026-06-28.md` —— Grill 报告

**关键决策**：
- Task 有 3 个状态：`todo` / `in-progress` / `done`
- Task 有 3 个优先级：`low` / `medium` / `high`
- 范围：只做核心 CRUD，不做用户认证、协作功能

---

### 第 2 步：/to-prd —— 定稿需求

**启动原因**：Grill 完成，共识已达成。

**输出**：
- `docs/prd/task-management-2026-06-28.md` —— PRD

**用户故事**：
1. 作为用户，我可以创建任务，以便记录要做的事
2. 作为用户，我可以查看任务列表，以便知道有什么事
3. 作为用户，我可以更新任务状态，以便跟踪进度
4. 作为用户，我可以删除任务，以便清理不需要的

**深模块机会**：
- `Task` 模块：封装状态机逻辑，提供简单接口

---

### 第 3 步：/to-issues —— 垂直切片

**启动原因**：PRD 已写，需要拆成可执行的任务。

**输出**：
- `docs/issues/task-management-2026-06-28.md` —— Issue 清单

**执行顺序**：
1. **曳光弹**：用户可以创建任务并看到在列表中（HITL）
2. 用户可以更新任务状态（AFK）
3. 用户可以删除任务（AFK）
4. 用户可以按优先级筛选（AFK）

---

### 第 4 步：/implement —— 实现一条龙

**启动原因**：Issue 已拆，开始实现第一个任务。

**输出**：
- `src/models/Task.js` —— 实现代码
- `src/models/Task.test.js` —— 测试代码
- `docs/reports/implement-create-task-2026-06-28.md` —— Implement 报告

**TDD 循环**：
1. 🔴 测试：`createTask` 应该创建一个任务
2. 🟢 实现：最简单的代码
3. 🟠 重构：提取状态机
4. 重复...

---

### 第 5 步：/codex-review —— 画布审查

**启动原因**：实现完成，提交 PR 前。

**输出**：
- `docs/reports/codex-review-2026-06-28.md` —— 审查报告

**结果**：
- SEV-1：0 条
- SEV-2：1 条（建议增加错误处理）
- SEV-3：1 条（变量名可以更好）

---

## 📂 关键文件解读

### CONTEXT.md

看看[共享语言](./CONTEXT.md)，这是整个项目的基础：
- 核心概念定义
- 状态机说明
- 范围内/外
- 测试策略

### PRD

看看[PRD](./docs/prd/task-management-2026-06-28.md)，这是需求的固化：
- 用户故事
- 验收标准
- 模块设计

### Issue 清单

看看[Issue 清单](./docs/issues/task-management-2026-06-28.md)，这是垂直切片的结果：
- 每个 issue 都是端到端的完整故事
- 标记了 AFK/HITL
- 有执行顺序

---

## 🎨 关键理念展示

### 1. 垂直切片，不是水平切片

❌ 不好（水平）：
- "先做数据库层"
- "再做 API 层"
- "最后做前端"

✅ 好（垂直）：
- "用户可以创建任务并看到在列表中"（端到端）
- "用户可以更新任务状态"（端到端）

### 2. 深模块

看看 [`Task.js`](./src/models/Task.js)：
- 简单接口：`createTask()`、`updateStatus()`、`getTasks()`
- 内部封装了复杂的状态机逻辑
- 调用方不需要知道状态怎么流转

### 3. TDD 循环

看看 [`Task.test.js`](./src/models/Task.test.js)：
- 测试读起来像规格说明
- 通过公开接口测试
- 不测试私有方法

---

## 🚀 怎么用这个示例？

### 新手路径

1. 先看 `CONTEXT.md` —— 理解共享语言怎么建立
2. 再看 PRD —— 理解需求怎么固化
3. 再看 Issue 清单 —— 理解怎么垂直切片
4. 最后看代码 + 测试 —— 理解 TDD 怎么应用

### 老项目接入

参考这个示例，对你的老项目：
1. 先跑 `/grill-with-docs` 建立共享语言
2. 再跑 `/doc-rot` 检查现有文档
3. 新功能用完整流程

---

## 💡 关键收获

1. **先 Grill，再动手** —— 充分理解比快速编码更重要
2. **垂直切片** —— 一次一个完整故事，能独立验证
3. **TDD** —— 测试先行，测试读起来像规格说明
4. **深模块** —— 简单接口，丰富实现
5. **渐进改进** —— 不要重写，要小步前进

---

## 🔗 相关文档

- [Opus48 工作流 README](../../02-README.md)
- [Quickstart](../../03-QUICKSTART.md)
