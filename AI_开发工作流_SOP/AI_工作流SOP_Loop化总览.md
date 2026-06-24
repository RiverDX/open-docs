# AI 开发工作流 Loop 化总览

> **目的**：把 SOP 5 个阶段中已完成 Loop 化的 skill 汇总为一张可一眼看完的地图。  
> **创建日期**：2026-06-23  
> **关联文件**：`AI_开发工作流_流程性_SOP.md`、各阶段操作手册、各阶段 Loop skill 文档  
> **理论基础**：Loop Engineering（来源：Clippings/`Loop Engineering从 0 到 1 小白完整教程.md`）

---

## 1. 完整版图（截至 2026-06-23）

| 阶段 | Skill | 单次版 | Loop 版 | 状态 |
|---|---|---|---|---|
| 阶段 1 | 项目初始化 | – | – | 不需要 Loop |
| 阶段 2 | reverse-mapping | ✅ | **reverse-loop** ✅ | 已完成 |
| 阶段 3 | grill-deep | ✅ | **grill-deep-loop** ✅ | 已完成 |
| 阶段 3 | grill-light | ✅ | – | 已够轻，不需要 |
| 阶段 3 | to-prd / to-issues | ✅ | – | 输出结构已稳定，不需要 |
| 阶段 4 | tdd | ✅ | **tdd-loop** ✅ | 已完成 |
| 阶段 4 | codex-review | ✅ | **codex-review-loop** ✅ | 已完成 |
| 阶段 5 | doc-rot-inspection | ✅ | **doc-rot-loop** ✅ | 已完成 |

### 各 Loop skill 对应的独立文档

| Loop Skill | 独立文档路径 |
|---|---|
| reverse-loop | `AI_工作流SOP_阶段2_Skill_reverse-loop.md` |
| grill-deep-loop | `AI_工作流SOP_阶段3_Skill_grill-deep-loop.md` |
| tdd-loop | `AI_工作流SOP_阶段4_Skill_tdd-loop.md` |
| codex-review-loop | `AI_工作流SOP_阶段4_Skill_codex-review-loop.md` |
| doc-rot-loop | `AI_工作流SOP_阶段5_Skill_doc-rot-loop.md` |

### 每个 Loop 的核心验收维度速查

| Loop | 维度数 | 维度命名 | 关键防陷阱设计 |
|---|---|---|---|
| reverse-loop | 6 | AC1–AC6 | 不确定项强制打 `[待验证]` 标签 |
| grill-deep-loop | 6 + 2 | GQ1–GQ6（维度）+ GQ7–GQ8（问题质量） | 每问必须有锚点 + 不答的后果 |
| tdd-loop | 6 | TC1–TC6 | TC6 禁止 `assertNotNull(result)` 等恒真断言 |
| codex-review-loop | 6 + 6 | RC1–RC6（维度）+ AC1–AC6（自查）+ SEV1/2/3 | SEV1 上限 5 条，避免淹没真问题 |
| doc-rot-loop | 4 | DR1–DR4 + P0/P1/P2 | P0 上限 5 条 + 健康度评分公式 |

---

## 2. 五个 Loop 之间的衔接关系

### 2.1 数据流图

```
                ┌─ reverse-loop ──────────────┐
                │  （梳理代码 → 模块文档）     │
                ▼                              │
          grill-deep-loop ──────► 优先级 5 问 │
       （演练 review，杀伤力提问）             │
                ▼                              │
              [阶段 3 共识确认]                 │
                ▼                              │
           tdd-loop ──────► 测试 + TC6         │
       （写测试，断言可证伪）                  │
                ▼                              │
        codex-review-loop ──► RC3 直接读 TC6  │
       （PR 前预审，6 维 + SEV1/2/3）          │
                ▼                              │
                 PR 合并                       │
                ▼                              │
            doc-rot-loop ◄────────────────────┘
       （每月巡检 4 类文档，DR2/DR3 回触 reverse-loop）
```

### 2.2 衔接关系详表

| 上游 Loop | 输出物 | 下游 Loop | 输入位置 |
|---|---|---|---|
| reverse-loop | 模块文档 `docs/modules/{模块}.md` | grill-deep-loop | "已有理解材料" |
| reverse-loop | "需人工确认清单" | 阶段 3 共识确认 | review 议题 |
| reverse-loop | `[待验证]` 项 | grill-deep-loop | 重点提问目标 |
| grill-deep-loop | "优先级 5 问" | 阶段 3 步骤 2 review | 会议议程 |
| grill-deep-loop | "业务方专属问题" | 阶段 3 业务方 review | 会前发送清单 |
| grill-deep-loop | 已确认答案 | to-prd | PRD"待确认项"已答覆 |
| tdd-loop | 测试矩阵 + TC6 评分 | codex-review-loop | RC3「测试覆盖与质量」 |
| tdd-loop | "需人工确认清单" | PR 描述 | 评审者需关注点 |
| codex-review-loop | SEV1 问题 | PR 内 | 必须修复后合并 |
| codex-review-loop | SEV3 问题 | issue 跟进 | 下个迭代 |
| doc-rot-loop | DR2 / DR3 腐化 | reverse-loop | 触发模块文档局部更新 |
| doc-rot-loop | DR4 腐化 | skill 季度 review | 优化 prompt |
| doc-rot-loop | 加权总分 | 月度健康报告 | SOP §9 度量指标 |

### 2.3 闭环说明

整个工作流形成**两层闭环**：

**第一层（单功能开发闭环）**：
```
reverse-loop → grill-deep-loop → 共识确认 → tdd-loop → codex-review-loop → PR 合并
```
每次新功能开发都按这条路径推进一次。

**第二层（项目演化闭环）**：
```
PR 合并 → doc-rot-loop（月度） → 发现腐化 → 回触 reverse-loop / skill 更新
```
通过 doc-rot-loop 每月一次的"反向触发"，保证文档不会与代码失同步。

---

## 3. 共同遵守的 Loop Engineering 4 模块

所有 Loop skill 都按 Loop Engineering 的 4 模块设计：

| 模块 | 落地形式 |
|---|---|
| **目标** | 每个 skill §1 都明确写出与单次版的差异 + 解决的具体问题 |
| **步骤** | 每个 skill §5 的 prompt 中"# 流程"段落，强制 6 步执行 |
| **检查** | 每个 skill 强制输出"自查表"，按 AC / TC / RC / GQ / DR 维度打 ✅/⚠️/❌ |
| **停止** | 统一规则：全 ✅ 立即停 / 最多 2 轮自查 / 超时输出"需人工确认清单" |

---

## 4. 使用建议

### 4.1 新项目接入顺序

按阶段顺序逐个引入，不要一次全部启用：

1. **第 1 周**：用 reverse-loop 跑通 1 个核心模块
2. **第 2 周**：在 review 前用 grill-deep-loop 演练
3. **第 3-4 周**：新功能开发用 tdd-loop + codex-review-loop
4. **首月末**：跑一次 doc-rot-loop 做基线评分

### 4.2 老项目接入顺序

老项目"上下文负债"重，建议反向接入：

1. **首周**：跑一次 doc-rot-loop 做体检，识别最腐化的模块
2. **第 2-3 周**：对最腐化的模块跑 reverse-loop + grill-deep-loop
3. **第 4 周起**：新功能采用 tdd-loop + codex-review-loop
4. **以后每月**：doc-rot-loop 巡检 + 按 P0/P1 修复

### 4.3 适配自定义 AC / TC / RC / GQ / DR

每个 Loop skill 都预留了"项目可加的自定义维度"段落（如 tdd-loop 的 TC7-TC10、grill-deep-loop 的 GQ9-GQ12）。  
按项目特性追加，不必拘泥默认 6 条。

---

## 5. 版本历史

| 版本 | 日期 | 变更 |
|---|---|---|
| V1.0 | 2026-06-23 | 初始版本，汇总 5 个已完成 Loop skill |
