# Opus48 工作流总结

> 已完成！基于 Matt Pocock Agent Skills 理念的 AI 编程工作流

---

## 🎨 已创建内容

新文件夹位置：`open-docs/opus48-ai-codding/`

### 📚 核心文档

1. **README.md** —— 全景图、快速开始、设计理念
2. **00-NAVIGATION.md** —— AI 的路由表 + 通用执行规则（AI 先读这个）
3. **CONTEXT.md** —— 共享语言模板
4. **CHECKLIST.md** —— 完整检查清单
5. **QUICKSTART.md** —— 5 分钟快速上手指南
6. **SUMMARY.md** —— 本文档

### 🛠️ 10 个技能

| # | Skill | 说明 |
|---|---|---|
| 1 | `/triage` | 画布整理（backlog 分类、AFK/HITL 标记） |
| 2 | `/grill-with-docs` | 对齐共识（无情提问、CONTEXT.md） |
| 3 | `/handoff` | 上下文接力（保持在聪明区） |
| 4 | `/prototype` | 草稿探索（一次性代码验证） |
| 5 | `/to-prd` | 定稿需求（固化共识、不重新提问） |
| 6 | `/to-issues` | 垂直切片（曳光弹先行） |
| 7 | `/tdd` | 红→绿→重构循环（测试先行） |
| 8 | `/codex-review` | 画布审查（PR 前预审） |
| 9 | `/improve-architecture` | 深化模块（不要重写、要渐进改进） |
| 10 | `/doc-rot` | 月度巡检（健康度评分） |

---

## 🎯 设计理念（艺术化总结）

### 编码如作画

- **意在笔先** —— `/grill-with-docs` 充分理解再动手
- **小步作画** —— 垂直切片，一次一个完整故事
- **红→绿→重构** —— 像打草稿，先画出轮廓再上色
- **定期打磨** —— `/improve-architecture` 让模块变深
- **每月检视** —— `/doc-rot` 保证文档不腐化

### 极简之道

- 永远在聪明区工作（<120K tokens），需要时用 `/handoff`
- 垂直切片，不要水平切片
- 深模块：简单接口，丰富实现
- 不要重写，要渐进改进

---

## 🚀 完整流程图

```
想法
  |
  ├─→ /triage ──────────────┐  整理 backlog
  |                          |
  └─→ /grill-with-docs ←────┘  对齐共识，建立共享语言
       |
       ↑  ↓ (需要原型时用 /handoff + /prototype)
       |
       ├─→ /to-prd ──────────┐  定稿需求
       |                      |
       └─→ /to-issues ←──────┘  垂直切片，曳光弹先行
            |
            ├─→ /tdd ─────────┐  红→绿→重构循环
            |                 |
            └─→ /codex-review←┘  PR 预审
                 |
                 ├─→ 合并 PR
                 |
                 ├─→ /improve-architecture (每周/完成功能后)  深化模块
                 |
                 └─→ /doc-rot (每月)  巡检文档，回触前面技能
```

---

## 📋 什么时候用哪个 Skill？

| 场景 | 用哪个 Skill |
|---|---|
| 有一堆 idea/issue 需要整理 | `/triage` |
| 需求不清晰，概念有歧义 | `/grill-with-docs` |
| 对话太长，接近变笨区 | `/handoff` |
| 遇到高保真问题，需要验证想法 | `/prototype` |
| 共识已达成，需要写 PRD | `/to-prd` |
| PRD 已写，需要拆成任务 | `/to-issues` |
| 开始实现，要保证代码质量 | `/tdd` |
| 代码写完，提交 PR 前 | `/codex-review` |
| 功能完成，想改进架构 | `/improve-architecture` |
| 定期检查文档是否过时 | `/doc-rot` |

---

## 🧠 核心概念

### 聪明区 vs 变笨区
- **聪明区**：<120K tokens，AI 专注、有创造力
- **变笨区**：>120K tokens，注意力分散、决策质量下降
- **怎么办**：用 `/handoff` 分流

### 深模块 vs 浅模块
- **深模块** ✅：简单接口，丰富实现（调用方不需要知道内部）
- **浅模块** ❌：复杂接口，简单实现（调用方需要知道所有细节）
- **目标**：让模块变深

### 垂直切片 vs 水平切片
- **垂直切片** ✅：用户可以端到端做一件事
- **水平切片** ❌：只做一层（如"先做数据库层"）
- **永远用垂直切片**

### AFK vs HITL
- **AFK**（Away From Keyboard）：Agent 能自己做
- **HITL**（Human In The Loop）：需要人盯着

---

## 🏁 从哪里开始？

推荐路径：
1. 先读 `QUICKSTART.md` —— 5 分钟了解
2. 拿一个小需求练练手，从 `/grill-with-docs` + `/tdd` 开始
3. 习惯后再加其他技能

**记住**：这是你的工具，不是枷锁。用对你有用的部分，剩下的放一边。
