# Opus48 —— 路由表

> **你是来跑 AI 编程工作流的。本文件是你的路由表 + 执行规则。**
> **阅读时间：1 分钟。所有 Skill 都在 `skills/` 子目录，每个一个文件，自包含。**
> **参考文档**：`01-AI-REFERENCE.md` —— 完整的使用参考手册，不知道怎么做时先看这个！

---

## 路由表：识别用户意图 → 选择 Skill

| 用户说的关键词 | 你必须启动的 Skill | 对应文件 |
|---|---|---|
| 梳理 backlog / 分类 issue / 分流 / 整理任务 | `/triage` | `skills/01-triage.md` |
| 理解需求 / 澄清 / grill / 对齐共识 / 先问问题 | `/grill-with-docs` | `skills/02-grill-with-docs.md` |
| 分流会话 / handoff / 保持聚焦 / 另开对话 | `/handoff` | `skills/03-handoff.md` |
| 做原型 / 探索 / 验证想法 / 先试试 / 草稿 | `/prototype` | `skills/04-prototype.md` |
| 写 PRD / 写需求文档 / 固化共识 / 产品需求 | `/to-prd` | `skills/05-to-prd.md` |
| 拆任务 / 切片 / to issues / 分成小任务 | `/to-issues` | `skills/06-to-issues.md` |
| 写测试 / TDD / 测试驱动 / 红→绿→重构 | `/tdd` | `skills/07-tdd.md` |
| 审查代码 / code review / 预审 / 检查改动 | `/codex-review` | `skills/08-codex-review.md` |
| 优化架构 / 深化模块 / improve architecture | `/improve-architecture` | `skills/09-improve-architecture.md` |
| 巡检文档 / 检查腐化 / doc rot / 健康度 | `/doc-rot` | `skills/10-doc-rot.md` |
| 实现 / implement / 写代码 + 审查 / 一条龙 | `/implement` | `skills/11-implement.md` |

**匹配规则**：
- 如果用户输入命中上表 → 立即读对应文件，按其中规则执行
- 如果不命中 → 反问"你想做下列哪件事？"列出 10 个 Skill 名
- **禁止自由发挥**，禁止跳过 Skill 直接动手

---

## 完整工作流（按这个顺序走）

```
想法
  │
  ├─→ /triage ──────────────┐  (如果有 backlog 要整理)
  │                         │
  └─→ /grill-with-docs ←────┘  ← (起点：先理解！)
       │
       ↑  ↓ (需要原型时用 /handoff + /prototype)
       │
       ├─→ /to-prd ──────────┐  (固化共识)
       │                     │
       └─→ /to-issues ←──────┘  (垂直切片，曳光弹先行)
            │
            ├─→ /implement ←──┬─ (一条龙：TDD + 审查)
            │  │              │
            │  │ (或者分开走)
            │  ├─→ /tdd ──────┘
            │  └─→ /codex-review
            │
            ├─→ /improve-architecture (完成功能后，深化模块)
            │
            └─→ /doc-rot (每月巡检，保持文档新鲜)
```

**快速选择指南**：
- 有 idea 但不清楚 → `/grill-with-docs`
- 共识达成 → `/to-prd`
- PRD 写完 → `/to-issues`
- 开始写代码 → `/implement` (一条龙) 或者 `/tdd`
- 代码写完 → `/codex-review`
- 功能完成想优化 → `/improve-architecture`
- 月底了 → `/doc-rot`

---

## 通用执行规则（所有 Skill 共用）

### 规则 1：必须按 Skill 文件中的「流程」分步执行

每个 Skill 文件都有"## 流程"段。**禁止跳步、禁止合并步骤、禁止改顺序**。

### 规则 2：检查必须用机械标准，不准凭感觉

每个 Skill 文件都有"## PASS 条件"段。**只有全部满足 PASS 条件的才能打 ✅，缺一条记 ⚠️，明显不符记 ❌**。

倾向：**严格而非宽松**。一律按从严解释。

### 规则 3：行号 / 引用必须验真

凡引用 `文件名:行号` 或代码片段：
- 必须**先用 Read 或 grep 工具读到**，再写
- 不准凭代码结构"推测"行号
- 如果工具用不了，引用形式必须改为 `[未验证] 文件名` + 不写行号

### 规则 4：最多 2 轮迭代

- 第 1 轮出初稿后自查
- 第 2 轮只允许针对 ⚠️/❌ 项修改
- 第 2 轮后仍有 ⚠️/❌ → **立即停止**，把卡点写入"需人工确认清单"
- **禁止**为追求完美无限改写已合格部分

### 规则 5：所有 Skill 输出 4 段，缺一不可

```
## 一、主产物（按各 Skill 要求的格式）
## 二、自查表（含证据列）
## 三、需人工确认清单
## 四、迭代轮次 + 是否达到停止条件
```

### 规则 6：监控上下文窗口

- 每次输出前检查当前 tokens
- 如果已超过 100K → **必须主动提议用 `/handoff` 分流**
- 不要等到掉进变笨区才想起

---

## 禁止清单（任何 Skill 都禁止）

1. **禁止**自由发挥不按 Skill 文件执行
2. **禁止**给 ✅ 但无证据（必须填证据列）
3. **禁止**编造行号 / 文件路径 / 函数名
4. **禁止**在主产物中使用 "可能 / 似乎 / 大概 / 应该是" 而不加 `[待验证]` 标记
5. **禁止**为凑数量堆相似项（同一问题换皮算 1 条）
6. **禁止**自评 2 轮以上还在改
7. **禁止**先写代码再理解（永远先 Grill）
8. **禁止**水平切片（永远垂直切片）

---

## 如果用户给的信息不足

不要猜。按以下顺序处理：

1. **缺关键代码** → 立即停止，列出"需要你提供 / 让我用 Read 读取的文件清单"
2. **缺 PRD / AC** → 列出"PRD 中必须明确的 N 项"，由用户补
3. **缺 CONTEXT.md** → 标记"无项目级共享语言，按通用最佳实践执行"
4. **缺数据库 schema** → 涉及数据模型的字段全部打 `[待验证]`

---

## 文件清单

```
opus48-ai-codding/
├── 00-NAVIGATION.md               # 本文件（路由 + 通用规则）← AI 第一个读
├── 01-AI-REFERENCE.md            # AI 使用参考手册
├── 02-README.md                  # 全景图 + 快速开始
├── 03-QUICKSTART.md              # 5 分钟快速上手指南
├── 04-CHECKLIST.md               # 完整检查清单
├── 05-SUMMARY.md                 # 工作流总结
├── 06-CONTEXT.md                 # 项目共享语言模板
├── skills/                        # 11 个 Skill（按顺序）
│   ├── 01-triage.md               # 画布整理
│   ├── 02-grill-with-docs.md      # 对齐共识
│   ├── 03-handoff.md              # 上下文接力
│   ├── 04-prototype.md            # 草稿探索
│   ├── 05-to-prd.md               # 定稿草图
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
│   ├── issues.md.template         # Issue 清单模板
│   └── implement-report.md.template # Implement 报告模板
└── examples/sample-project/       # 完整示例项目
    ├── README.md                  # 示例说明
    ├── CONTEXT.md                 # 示例共享语言
    ├── docs/
    │   ├── prd/...                # 示例 PRD
    │   ├── issues/...             # 示例 Issue 清单
    │   └── reports/...            # 示例报告
    └── src/models/...             # 示例代码 + 测试
```

---

## 总原则（四句话）

> 1. **先 Grill，再动手**
> 2. **在聪明区工作**
> 3. **垂直切片，TDD 循环**
> 4. **需要时用 /implement 一条龙**
