# Skill 01：/triage —— 画布整理

> **何时启动**：有杂乱的 backlog 需要整理；刚拿到一堆 issue 需要分类；不确定从哪个开始。
> **目标**：把混乱变成可执行的任务，标记清楚哪些 Agent 能自己做，哪些需要人。

---

## 输入清单（缺即停）

| 项 | 必需 | 缺失时动作 |
|---|---|---|
| Issue / backlog 列表 | 必需 | 反问"你要整理哪些 issue？提供链接或清单" |
| 项目现有 label 分类 | 建议 | 缺时用本 Skill 建议的标准标签 |
| .out-of-scope/ 目录（如有） | 建议 | 检查是否有已决定不做的事项 |

---

## 输出文件（2 个，缺一不可）

| 文件 | 路径模板 | 包含段落 | 寿命 |
|---|---|---|---|
| **Triage 报告** | `docs/reports/triage-{YYYY-MM-DD}.md` | 分流结果概览 + 标签统计 + 建议执行顺序 | **短期**（任务归档） |
| **Issue 更新** | 直接更新 issue 标签（或输出建议标签清单） | 每个 issue 的标签建议 | **长期**（应用到真实 issue） |

---

## 流程（6 步，禁止跳步）

1. **扫**：列出所有待分流的 issue，输出清单
2. **分类**：给每个 issue 打**类别标签**（bug / enhancement / question / docs）
3. **定状态**：给每个 issue 打**状态标签**（needs-triage / needs-info / ready-for-agent / ready-for-human / wontfix）
4. **出初稿**：按下方"输出格式"写 Triage 报告
5. **自查**：按 PASS 条件 AC1–AC6 填自查表，每条给证据
6. **终输出**：确认 2 个文件都已生成

---

## 标签系统（严格使用）

### 类别标签（每个 issue 选一个）

| 标签 | 含义 | 例子 |
|---|---|---|
| `bug` | 现有功能坏了，需要修 | "点击提交按钮没反应" |
| `enhancement` | 新功能或改进 | "增加导出 Excel 功能" |
| `question` | 需要回答的问题 | "这个接口应该怎么用？" |
| `docs` | 文档相关 | "补充 API 文档" |

### 状态标签（每个 issue 选一个）

| 标签 | 含义 | 后续动作 |
|---|---|---|
| `needs-triage` | 刚进来，还没看 | 需要维护者再看一次 |
| `needs-info` | 信息不足，问用户 | 等用户补充信息后再继续 |
| `ready-for-agent` | 信息完整，Agent 能做 | 可以直接给 AI 实现 |
| `ready-for-human` | 需要人来做 | 涉及设计、架构决策、高风险 |
| `wontfix` | 不做 | 引用 ADR 说明原因 |

### 辅助标签（可选）

| 标签 | 含义 |
|---|---|
| `AFK` | Agent 可以自己做（Away From Keyboard） |
| `HITL` | 需要人盯着（Human In The Loop） |
| `good-first-issue` | 适合新手 |
| `P0/P1/P2` | 优先级 |

---

## PASS 条件（自查标准，严格解释）

### AC1 分类完整
- ✅ 所有 issue 都有类别标签（bug / enhancement / question / docs）
- ⚠️ 个别 issue 类别有歧义，但已标记
- ❌ 有 issue 没打类别标签

### AC2 状态合理
- ✅ 所有 issue 都有状态标签，且标签与 issue 内容匹配
- ⚠️ 个别 issue 状态有争议，但已记录理由
- ❌ 有 issue 没打状态标签

### AC3 AFK/HITL 标记正确
- ✅ `ready-for-agent` 的 issue 有清晰的验收标准
- ✅ `ready-for-human` 的 issue 说明了为什么需要人
- ⚠️ 部分 issue 标记不明确
- ❌ 有 high-risk 任务标记为 AFK

### AC4 wontfix 有理由
- ✅ 所有 wontfix issue 都引用了 ADR 或明确说明原因
- ⚠️ 理由不够清晰
- ❌ wontfix 没有理由

### AC5 建议执行顺序
- ✅ 按依赖关系和优先级排了顺序
- ⚠️ 顺序不够合理
- ❌ 没有顺序

### AC6 没有太大的 issue
- ✅ 所有 issue 都能在 1–2 天内完成
- ⚠️ 有几个较大，但已建议拆分
- ❌ 有超过 1 周的大 issue 没拆分

---

## 输出格式

### 文件 1：`docs/reports/triage-{YYYY-MM-DD}.md`

```markdown
# Triage 报告：{YYYY-MM-DD}

## 概览
- 本次分流：{N} 个 issue
- Bug：{N} | Enhancement：{N} | Question：{N} | Docs：{N}
- Ready-for-agent：{N} | Ready-for-human：{N}

## 分流结果详情

| Issue | 标题 | 类别 | 状态 | AFK/HITL | 优先级 |
|---|---|---|---|---|---|
| #123 | {标题} | bug | ready-for-agent | AFK | P1 |
| #124 | {标题} | enhancement | ready-for-human | HITL | P0 |
| ... | ... | ... | ... | ... | ... |

## 建议执行顺序（按依赖关系）

1. {Issue A} —— 原因：无依赖，优先做
2. {Issue B} —— 原因：依赖 A
3. ...

## 建议拆分的大 issue

- {Issue C} —— 建议拆成：{子任务 1}、{子任务 2}
- ...

## 一、主产物
（上方的分流结果详情 + 建议执行顺序）

## 二、自查表
| AC | 评分 | 证据 |
|---|---|---|
| AC1 分类完整 | ✅/⚠️/❌ | ... |
| AC2 状态合理 | ✅/⚠️/❌ | ... |
| AC3 AFK/HITL 标记正确 | ✅/⚠️/❌ | ... |
| AC4 wontfix 有理由 | ✅/⚠️/❌ | ... |
| AC5 建议执行顺序 | ✅/⚠️/❌ | ... |
| AC6 没有太大的 issue | ✅/⚠️/❌ | ... |

## 三、需人工确认清单
- [ ] {卡点 1} —— 建议：...
- [ ] {不确定项 1} —— 建议：...

## 四、迭代信息
- 轮次：{1 / 2}
- 是否达到停止条件：{是 / 否（原因）}
```

---

## 禁用模式（出现即扣分）

| 禁用做法 | 应改为 |
|---|---|
| "这个 issue 很大，先做着看" | 拆分成小 issue |
| 所有 issue 都标记为 HITL | 区分真正需要人的和 AFK 的 |
| wontfix 只写"不做" | 必须说明为什么不做，引用 ADR |
| 把"重构整个系统"当成一个 issue | 拆成可管理的小改进 |

---

## 完成后

建议下一步：
- `ready-for-agent` 的 → `/to-issues`（如果还没拆）→ `/tdd`
- `ready-for-human` 的 → `/grill-with-docs` 对齐共识
- `needs-info` 的 → 等用户补充信息
