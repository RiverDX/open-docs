# 模板目录

> 复制这些模板到你的项目，快速开始使用 Opus48 工作流

---

## 📂 模板列表

| 模板 | 用途 | 复制到 |
|---|---|---|
| `CONTEXT.md.template` | 共享语言模板 | 项目根目录的 `CONTEXT.md` |
| `grill-report.md.template` | Grill 报告模板 | `docs/reports/grill-YYYY-MM-DD.md` |
| `prd.md.template` | PRD 模板 | `docs/prd/xxx-YYYY-MM-DD.md` |
| `issues.md.template` | Issue 清单模板 | `docs/issues/xxx-YYYY-MM-DD.md` |
| `implement-report.md.template` | Implement 报告模板 | `docs/reports/implement-xxx-YYYY-MM-DD.md` |

---

## 🚀 快速开始

### 新项目启动

1. 复制 `CONTEXT.md.template` 到项目根目录，重命名为 `CONTEXT.md`
2. 运行 `/grill-with-docs`，用对话填充 CONTEXT.md
3. 复制 `prd.md.template`，运行 `/to-prd`
4. 复制 `issues.md.template`，运行 `/to-issues`
5. 开始实现！

### 老项目接入

1. 复制 `CONTEXT.md.template` 到项目根目录
2. 运行 `/grill-with-docs` 梳理现有概念
3. 运行 `/doc-rot` 检查现有文档
4. 新功能用完整流程

---

## 📝 使用说明

### CONTEXT.md.template

这是共享语言的模板，包含：
- 项目概览
- 核心概念（带表格）
- ADR（架构决策记录）
- 接口契约
- 范围内/范围外
- 测试策略
- 未知区域

**重要**：这是活文档，持续更新！

### grill-report.md.template

Grill 完成后生成的报告，包含：
- 对话摘要
- 达成的决策
- 高保真问题识别
- 自查表

### prd.md.template

PRD 模板，包含：
- 问题陈述
- 用户故事
- 验收标准
- 模块设计
- 范围外
- 风险

### issues.md.template

Issue 清单模板，包含：
- 执行顺序
- Issue 详情
- 依赖关系
- AFK/HITL 标记

### implement-report.md.template

Implement 报告模板，包含：
- TDD 循环记录
- 测试矩阵
- 代码审查结果

---

## 💡 最佳实践

1. **不要修改模板** —— 复制后修改副本
2. **持续更新 CONTEXT.md** —— 这是团队的共享语言
3. **每个功能一个 PRD** —— 不要把所有东西放一个 PRD
4. **每个 Issue 垂直切片** —— 端到端，可独立验证
5. **报告归档** —— 报告存在 `docs/reports/`，不要删除
