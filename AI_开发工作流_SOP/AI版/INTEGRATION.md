# 项目集成示例：CLAUDE.md 中加入 Loop 引导

> **作用**：把这段加到项目的 `CLAUDE.md` 顶部，AI 每次会话都会自动加载，
> 就能在用户说"梳理 X 模块"时主动按 Loop 工作流执行，而不是自由发挥。

---

## 推荐复制片段

```markdown
## AI 工作流（必读）

本项目使用结构化 AI 工作流。当用户请求命中下列关键词时，**先读对应 Loop 文档再执行**：

| 关键词 | 启动 | 文档路径 |
|---|---|---|
| 梳理/逆向/理解/还原 X 模块 | reverse-loop | docs/ai-workflow/loops/reverse-loop.md |
| 演练 review/帮我想问题/grill | grill-deep-loop | docs/ai-workflow/loops/grill-deep-loop.md |
| 写测试/TDD/补单测 | tdd-loop | docs/ai-workflow/loops/tdd-loop.md |
| 审 PR/code review/预审 | codex-review-loop | docs/ai-workflow/loops/codex-review-loop.md |
| 巡检文档/检查腐化 | doc-rot-loop | docs/ai-workflow/loops/doc-rot-loop.md |

**通用规则**：
1. 必须按 Loop 文档的"流程"分步执行，禁止跳步
2. 自查必须严格按 PASS 条件，倾向严格不倾向宽松
3. 行号/引用必须用 Read/grep 验证过，禁止编造
4. 最多 2 轮自查，超时输出"需人工确认清单"
5. 输出 4 段：主产物 + 自查表 + 待确认清单 + 迭代信息
6. 完成后跑校验脚本：`python docs/ai-workflow/check-output.py <loop> <输出文件>`

详细路由表见 `docs/ai-workflow/README.md`。
```

---

## 部署步骤

### 步骤 1：复制 AI版 到项目

```bash
# 在项目根目录
mkdir -p docs/ai-workflow
cp -r /path/to/AI版/* docs/ai-workflow/

# 检查
ls docs/ai-workflow/
# 应有: README.md, check-output.py, loops/
```

### 步骤 2：编辑 CLAUDE.md

把本文件的"推荐复制片段"加到项目根 `CLAUDE.md` 中（建议放在文件开头的"AI 工作约束"段）。

### 步骤 3：验证

启动新的 AI 会话，问："帮我梳理 order 模块"

AI 应该：
1. 识别关键词 "梳理 X 模块"
2. 主动读 `docs/ai-workflow/loops/reverse-loop.md`
3. 按其中 6 步流程执行
4. 输出 4 段结构化产物
5. 提示你跑校验脚本

如果 AI 没这么做，说明 CLAUDE.md 没被加载，或片段位置太靠后。把片段挪到 CLAUDE.md 最前面。

---

## 自定义建议

### 路径调整

如果项目 docs 结构不同，把表格中的 `docs/ai-workflow/` 改成实际路径即可。

### 关键词扩充

按团队习惯加更多触发词。例如：

| 用户说... | 启动 |
|---|---|
| 走查 X 模块 | reverse-loop |
| 找 bug 风险 | grill-deep-loop + codex-review-loop |
| 重构前看一下 | reverse-loop |

### Loop 维度扩充

每个 Loop 文件的 PASS 条件可以追加项目特有的：

- tdd-loop 加 TC7 "所有金额计算用 BigDecimal"（金融项目）
- codex-review-loop 加 RC7 "性能维度"
- doc-rot-loop 加 DR5 "数据库 schema 与 Entity 一致性"

直接编辑对应 loop 文件即可，AI 下次会用新规则。

---

## 与现有 SOP 文档的关系

| 文档 | 目标读者 | 用途 |
|---|---|---|
| `AI_开发工作流_流程性_SOP.md` 等阶段手册 | 团队成员（人） | 学习方法论、流程培训 |
| `AI_工作流SOP_阶段X_Skill_*.md` | 人 + AI | 完整 skill 文档（含背景、案例、注意事项） |
| **`AI版/` 目录（本文件所在）** | **AI** | 精简、机械化、自包含，AI 执行时直接读 |

人看人版（详细），AI 跑 AI 版（精炼）。两套并行不冲突。
