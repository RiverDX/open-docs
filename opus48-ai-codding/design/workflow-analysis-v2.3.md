# Opus48 v2.3 完整流程图分析

> **日期**：2026-07-10
> **版本**：v2.3
> **目的**：展示完整流程图，分析优化点

---

## 📊 全景流程图（两种模式）

```mermaid
flowchart TD
    Start([开始]) --> HasBacklog{有Backlog<br>需要整理?}
    HasBacklog -->|是| Triage[/to-triage\]
    HasBacklog -->|否| HasPrototype{有原型图<br>+简要描述?}

    Triage --> TriageOutput[docs/reports/triage-xxx.md<br>更新Issue Labels]
    TriageOutput --> HasPrototype

    HasPrototype -->|是| PrototypeToBusiness[/prototype-to-business\]
    HasPrototype -->|否| IsClear{需求是否<br>清晰明确?}

    PrototypeToBusiness --> BusinessDoc[docs/business/xxx-YYYY-MM-DD.md<br>业务梳理文档]
    BusinessDoc --> BusinessClear{业务梳理<br>是否清晰?}
    BusinessClear -->|否| GrillWithDocs[/grill-with-docs\]
    BusinessClear -->|是| ToPrDB[/to-prd<br>模式B:从业务梳理生成\]

    IsClear -->|否| GrillWithDocs
    IsClear -->|是| HasContext{是否有<br>CONTEXT.md?}

    GrillWithDocs --> Context[CONTEXT.md<br>共享语言]
    GrillWithDocs --> GrillReport[docs/reports/grill-xxx.md<br>Grill报告]
    Context --> ToPrDA[/to-prd<br>模式A:从CONTEXT生成\]
    HasContext -->|是| ToPrDA
    HasContext -->|否| GrillWithDocs

    ToPrDA --> PRD[docs/prd/xxx-YYYY-MM-DD.md<br>PRD文档]
    ToPrDB --> PRD

    PRD --> ToIssues[/to-issues\]
    ToIssues --> IssueList[docs/issues/xxx-YYYY-MM-DD.md<br>旧格式清单]
    ToIssues --> IssueDir[docs/issues/xxx-YYYY-MM-DD/<br>新格式目录]
    IssueDir --> IssueReadme[README.md<br>总览+状态看板]
    IssueDir --> Issue001[001-xxx.md<br>单个Issue]
    IssueDir --> Issue002[002-xxx.md<br>单个Issue]
    IssueDir --> IssueN[...more Issues]

    IssueReadme --> SelectNextIssue{选择下一个<br>Issue}
    SelectNextIssue --> IsBlocked{Issue是否被<br>阻塞?}
    IsBlocked -->|是| CreateTodo[创建TODO文档<br>docs/todos/todo-xxx.md]
    CreateTodo --> TodoResolved{TODO是否<br>解决?}
    TodoResolved -->|是| IsBlocked
    TodoResolved -->|否| Wait[等待用户确认]

    IsBlocked -->|否| IsAllDone{所有Issue<br>都完成?}
    IsAllDone -->|否| ImplementChoice{选择<br>实现方式}
    ImplementChoice -->|一条龙| Implement[/implement\]
    ImplementChoice -->|分步走| TDD[/tdd\]

    TDD --> UpdateStatus1[更新Issue状态<br>pending->in-progress]
    TDD --> TestCode[测试代码]
    TDD --> ImplementCode[实现代码]
    TDD --> TDDReport[docs/reports/tdd-xxx.md<br>TDD报告]

    Implement --> UpdateStatus2[更新Issue状态<br>pending->in-progress]
    Implement --> AutoTDD[自动TDD循环]
    Implement --> AutoReview[自动代码审查]
    Implement --> ImplementReport[docs/reports/implement-xxx.md<br>Implement报告]

    TDDReport --> CodeReview[/codex-review\]
    CodeReview --> ReviewReport[docs/reports/codex-review-xxx.md<br>审查报告]

    AutoReview --> HasSevere{有SEV-1<br>问题?}
    ReviewReport --> HasSevere
    HasSevere -->|是| FixSevere[修复SEV-1问题]
    FixSevere --> CodeReview
    HasSevere -->|否| IssueDone[更新Issue状态<br>in-progress->done]

    IssueDone --> IsAllDone

    IsAllDone -->|是| NeedImprove{是否需要<br>架构优化?}
    NeedImprove -->|是| ImproveArchitecture[/improve-architecture\]
    NeedImprove -->|否| NeedCheck{是否到了<br>月度巡检时间?}

    ImproveArchitecture --> ImproveReport[docs/reports/improve-architecture-xxx.md<br>架构改进建议]
    ImproveReport --> NeedCheck

    NeedCheck -->|是| DocRot[/doc-rot\]
    NeedCheck -->|否| NextProject[下一个项目<br>或需求]

    DocRot --> DocRotReport[docs/reports/doc-rot-xxx.md<br>巡检报告]
    DocRotReport --> HealthCheck{健康度<br>是否达标?}
    HealthCheck -->|否| ImproveDoc[改进文档]
    ImproveDoc --> DocRot
    HealthCheck -->|是| NextProject

    NextProject --> Start

    style Triage fill:#fff3cd,stroke:#d6b578
    style GrillWithDocs fill:#e7f5ff,stroke:#74c0fc
    style PrototypeToBusiness fill:#e7f5ff,stroke:#74c0fc
    style ToPrDA fill:#d3f9d8,stroke:#51cf66
    style ToPrDB fill:#d3f9d8,stroke:#51cf66
    style ToIssues fill:#d3f9d8,stroke:#51cf66
    style TDD fill:#fff3bf,stroke:#fab005
    style Implement fill:#fff3bf,stroke:#fab005
    style CodeReview fill:#ffe3e3,stroke:#ff6b6b
    style ImproveArchitecture fill:#e5dbff,stroke:#9775fa
    style DocRot fill:#e9ecef,stroke:#adb5bd
```

---

## 🔍 各阶段详细流程

### 阶段 1：需求输入
```mermaid
flowchart LR
    A([需求输入]) --> B{输入类型?}
    B -->|Backlog清单| C[/to-triage\]
    B -->|想法/模糊需求| D[/grill-with-docs\]
    B -->|原型图+简要描述| E[/prototype-to-business\]
    C --> F[Triage报告]
    D --> G[CONTEXT.md<br>共享语言]
    E --> H[业务梳理文档]
```

### 阶段 2：需求固化
```mermaid
flowchart LR
    A([需求固化]) --> B{输入源?}
    B -->|业务梳理文档| C[/to-prd<br>模式B\]
    B -->|CONTEXT.md| D[/to-prd<br>模式A\]
    C --> E[PRD文档]
    D --> E
    E --> F[/to-issues\]
    F --> G[Issue清单/目录]
```

### 阶段 3：实现执行
```mermaid
flowchart LR
    A([实现执行]) --> B{选择Issue}
    B --> C{有阻塞?}
    C -->|是| D[创建TODO]
    D --> E{TODO解决?}
    E -->|是| C
    E -->|否| F[等待确认]
    C -->|否| G{实现方式?}
    G -->|一条龙| H[/implement\]
    G -->|分步走| I[/tdd\]
    I --> J[/codex-review\]
    H --> K{有SEV-1?}
    J --> K
    K -->|是| L[修复问题]
    K -->|否| M[更新Issue状态]
    M --> N{还有Issue?}
    N -->|是| B
    N -->|否| O[完成]
```

### 阶段 4：优化巡检
```mermaid
flowchart LR
    A([优化巡检]) --> B{需要架构优化?}
    B -->|是| C[/improve-architecture\]
    B -->|否| D{到月度巡检?}
    C --> D
    D -->|是| E[/doc-rot\]
    E --> F{健康度达标?}
    F -->|否| G[改进文档]
    F -->|是| H[完成]
    G --> E
```

---

## ⚠️ 优化点分析

### 🔴 P0 高优先级

#### 1. Skill编号不连续
**问题**：
- 01-triage
- 02-grill-with-docs
- 02.5-prototype-to-business ← 小数点，不规范
- 03-handoff
- 04-prototype

**建议优化**：
```
选项A：重新编号
- 01-triage
- 02-grill-with-docs
- 03-prototype-to-business (新增)
- 04-handoff
- 05-prototype
- ...其余依次后移

选项B：保持现状，但添加说明
- 在文档中说明 02.5 是插入的中间阶段
```

**建议**：采用选项A，保持编号连续。

---

#### 2. Skill名称冲突
**问题**：
- 04-prototype（草稿探索）
- 03-prototype-to-business（原型转业务梳理）

这两个名字都有"prototype"，容易混淆。

**建议优化**：
```
重命名：
- 04-prototype → 05-spike（Spike探索，符合极限编程术语）
或
- 03-prototype-to-business → 03-design-to-requirements（设计转需求）
```

---

### 🟡 P1 中优先级

#### 3. /to-issues 生成双重格式
**问题**：
- 当前设计为同时生成旧格式和新格式
- 两个格式都存在，可能导致用户困惑

**建议优化**：
```
选项A：只生成新格式，旧格式保留模板但不主动生成
- 在Skill中添加参数，让用户选择生成哪种格式
- 默认生成新格式

选项B：明确说明新旧格式的区别和使用场景
- 在文档中说明：新项目用新格式，旧项目可以继续用旧格式
```

---

#### 4. 缺少TODO管理的Skill
**问题**：
- TODO文档需要手动创建和更新
- TODO状态变更需要手动修改历史记录
- TODO的创建和解决没有专门的Skill

**建议优化**：
```
新增 Skill：/manage-todos
功能：
- 创建TODO文档
- 关联阻塞的Issue
- 更新TODO状态（open -> resolved -> closed）
- 自动更新关联Issue的状态
- 生成TODO列表总览
```

---

#### 5. 缺少从PRD回退的分支
**问题**：
- 如果PRD生成后发现问题，没有明确的回退路径
- 需要重新走 Grill → PRD，但没有明确的说明

**建议优化**：
```
在 05-WORKFLOW.md 中添加回退流程说明
- 发现PRD问题 → 更新业务梳理文档 或 更新CONTEXT.md → 重新生成PRD
```

---

### 🟢 P2 低优先级

#### 6. 缺少可视化的进度看板
**问题**：
- Issue状态分散在各个文件中
- 没有整体的进度可视化

**建议优化**：
```
在 docs/issues/README.md 中添加更丰富的可视化看板
- 燃尽图
- 进度条
- 甘特图（可选）
```

---

#### 7. 缺少快速启动脚本
**问题**：
- 新手需要手动复制多个模板文件
- 没有一键初始化项目的脚本

**建议优化**：
```
新增 scripts/init-project.sh
功能：
- 复制CONTEXT.md.template到项目根目录
- 创建docs/business/, docs/prd/, docs/issues/, docs/todos/, docs/reports/ 目录
- 创建初始README
```

---

#### 8. 缺少示例的完整流程演示
**问题**：
- 当前示例项目只有PRD和Issue
- 缺少从原型图开始的完整示例

**建议优化**：
```
在 examples/ 目录下新增：
- examples/from-prototype/ - 从原型图开始的完整示例
- 包含原型图描述 → 业务梳理 → PRD → Issue → 实现的完整流程
```

---

## 📋 优化后推荐的完整流程

### 推荐的最佳实践路径
```mermaid
flowchart TD
    A([需求输入]) --> B{形式?}

    B -->|原型图+描述| C[/prototype-to-business\]
    C --> D[业务梳理文档]
    D --> E{是否清晰?}
    E -->|否| F[/grill-with-docs\]
    E -->|是| G

    B -->|想法/模糊| F
    F --> H[CONTEXT.md]
    H --> G

    B -->|已有PRD| I[/to-issues\]

    G[/to-prd<br>模式B\] --> J[PRD文档]
    F --> K[/to-prd<br>模式A\] --> J

    J --> I
    I --> L[Issue目录]

    L --> M{选Issue}
    M --> N{阻塞?}
    N -->|是| O[/manage-todos<br>创建TODO\]
    N -->|否| P

    O --> Q{TODO解决?}
    Q -->|否| R[等待]
    Q -->|是| N

    P[/implement<br>一条龙\]
    P --> S{SEV-1?}
    S -->|是| T[修复]
    S -->|否| U[Issue完成]

    U --> V{还有Issue?}
    V -->|是| M
    V -->|否| W{需要优化?}
    W -->|是| X[/improve-architecture\]
    W -->|否| Y{巡检时间?}

    Y -->|是| Z[/doc-rot\]
    Y -->|否| Done([完成])

    X --> Z
    Z --> AA{健康度达标?}
    AA -->|否| AB[改进文档]
    AA -->|是| Done
    AB --> Z
```

---

## 🎯 总结建议

### 立即处理（v2.3.1）
1. ✅ 重新编号 Skill，解决 02.5 的问题
2. ✅ 考虑重命名 prototype-to-business 或 prototype 避免冲突
3. ✅ 明确新旧格式的使用策略

### 下一个版本（v2.4）
1. 新增 /manage-todos Skill
2. 添加回退流程说明
3. 增加进度看板可视化

### 长期规划（v3.0）
1. 添加快速启动脚本
2. 完善示例项目
3. 添加更多集成点（GitHub Issues、Jira等）

---

## 📝 决策记录

| ID | 决策 | 状态 | 备注 |
|---|---|---|---|
| DECISION-001 | Skill重新编号方式 | 待确认 | 选项A vs 选项B |
| DECISION-002 | 命名冲突解决方案 | 待确认 | 重命名哪个? |
| DECISION-003 | 新旧格式策略 | 待确认 | 同时生成?二选一? |

---

**文档结束**
