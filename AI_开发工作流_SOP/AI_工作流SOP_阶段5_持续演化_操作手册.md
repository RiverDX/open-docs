# 阶段 5：持续演化 —— 操作手册

> **目标**：防止项目上下文（`CLAUDE.md`、模块文档、术语表）与代码再次脱节，让 AI 辅助工作流能够长期有效。  
> **前提**：前四个阶段已至少跑过一次，项目已存在 `docs/` 和 `CLAUDE.md`。  
> **预计耗时**：PR 级检查约 10–30 分钟；每月巡检约 2–4 小时。

---

## 1. 所需工具

| 工具 | 用途 | 是否必需 |
|---|---|---|
| **Git** | 版本控制、diff 分析、变更追踪 | 是 |
| **Python / Shell** | 编写文档引用检查、同步检测脚本 | 建议 |
| **CI/CD**（GitHub Actions / GitLab CI / Jenkins） | 在 PR 流程中自动运行轻量检查 | 建议 |
| **AI 工具** | 深度文档腐化巡检、语义一致性检查 | 是 |
| **Markdown 编辑器** | 查看和更新文档 | 是 |
| **SonarQube / 静态分析工具** | 代码质量趋势监测 | 可选 |

---

## 2. 环境准备

### 2.1 确认脚本目录

```bash
mkdir -p scripts
```

### 2.2 确认报告目录

```bash
mkdir -p docs/reports
```

### 2.3 确认变更日志文件

```bash
touch docs/claude-md-changelog.md
```

---

## 3. 操作步骤

### 步骤 1：PR 级轻量检查（每次合并前）

在 CI 或本地提交前运行，检查文档与代码的机械一致性。

#### 1.1 检查 CLAUDE.md 引用的文件是否仍然存在

创建脚本 `scripts/check_claude_md_refs.py`：

```python
#!/usr/bin/env python3
import re
import os
import sys
from pathlib import Path

CLAUDE_FILES = ["CLAUDE.md"] + list(Path(".").rglob("*/CLAUDE.md"))
REF_PATTERNS = [
    r"`?docs/([a-zA-Z0-9_\-/]+\.md)`?",
    r"\[.*?\]\(docs/([a-zA-Z0-9_\-/]+\.md)\)",
    r"docs/([a-zA-Z0-9_\-/]+\.md)",
]

def find_refs(content):
    refs = set()
    for pattern in REF_PATTERNS:
        refs.update(re.findall(pattern, content))
    return refs

errors = []
for claude_file in CLAUDE_FILES:
    content = claude_file.read_text(encoding="utf-8")
    refs = find_refs(content)
    for ref in refs:
        target = Path("docs") / ref
        if not target.exists():
            errors.append(f"{claude_file}: 引用不存在 {target}")

if errors:
    print("发现 CLAUDE.md 引用问题：")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
else:
    print("CLAUDE.md 引用检查通过。")
```

运行：

```bash
python scripts/check_claude_md_refs.py
```

#### 1.2 检查入口地图是否与实际 Controller 一致

创建脚本 `scripts/check_api_doc_sync.py`：

```python
#!/usr/bin/env python3
import re
import os
import sys
from pathlib import Path

CONTROLLER_DIR = Path("src/main/java")
ENTRY_POINTS_FILE = Path("docs/entry-points.md")

def extract_controller_paths():
    paths = set()
    for file in CONTROLLER_DIR.rglob("*.java"):
        content = file.read_text(encoding="utf-8")
        # 匹配 @RequestMapping、@GetMapping、@PostMapping 等
        mappings = re.findall(r'@(?:Get|Post|Put|Delete|Patch|Request)Mapping\(["\']([^"\']+)["\']', content)
        paths.update(mappings)
    return paths

def extract_doc_paths():
    if not ENTRY_POINTS_FILE.exists():
        return set()
    content = ENTRY_POINTS_FILE.read_text(encoding="utf-8")
    # 匹配表格中的路径，如 /api/v1/orders
    return set(re.findall(r'\| (/[^ |]+)', content))

controller_paths = extract_controller_paths()
doc_paths = extract_doc_paths()

missing_in_doc = controller_paths - doc_paths
missing_in_code = doc_paths - controller_paths

if missing_in_doc or missing_in_code:
    print("发现入口地图不一致：")
    for p in sorted(missing_in_doc):
        print(f"  - 代码中有但入口地图缺失: {p}")
    for p in sorted(missing_in_code):
        print(f"  - 入口地图中有但代码缺失: {p}")
    sys.exit(1)
else:
    print("入口地图同步检查通过。")
```

运行：

```bash
python scripts/check_api_doc_sync.py
```

#### 1.3 集成到 CI

**GitHub Actions 示例**（`.github/workflows/doc-check.yml`）：

```yaml
name: Documentation Consistency Check

on:
  pull_request:
    branches: [main]

jobs:
  doc-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Check CLAUDE.md references
        run: python scripts/check_claude_md_refs.py
      - name: Check API doc sync
        run: python scripts/check_api_doc_sync.py
```

**GitLab CI 示例**（`.gitlab-ci.yml`）：

```yaml
doc-check:
  image: python:3.11
  script:
    - python scripts/check_claude_md_refs.py
    - python scripts/check_api_doc_sync.py
  only:
    - merge_requests
```

---

### 步骤 2：每月文档腐化巡检

每月运行一次深度巡检，检查语义一致性、文档新鲜度、skill 有效性。

#### 2.1 准备巡检输入

收集以下材料：

- 当前 `CLAUDE.md`（根 + 模块级）；
- `docs/entry-points.md`；
- `docs/glossary.md`；
- `docs/modules/` 下所有模块文档；
- 最近一个月的 `git log --oneline`；
- 最近一个月合并的 PR diff（`git log --since="30 days ago" --name-only`）。

#### 2.2 运行 AI 深度巡检

使用以下 prompt（可放在 `docs/ai-skills/doc-rot-inspection.md`）：

```markdown
# 角色
你是该 Java 项目的知识管理专员。请检查以下文档与代码的一致性，并输出腐化检测报告。

# 检查项
1. `CLAUDE.md` 中提到的关键类/接口是否仍然存在；
2. `docs/entry-points.md` 中的接口是否与代码一致；
3. `docs/glossary.md` 中的术语是否仍被代码使用；
4. 过去一个月合并的 PR 中，是否有变更未同步到文档；
5. `docs/modules/` 中的模块文档是否与当前代码一致；
6. `docs/ai-skills/` 中的 prompt 是否仍适用于当前模型版本；
7. 是否有新的业务术语、入口、状态机未更新到文档。

# 输入
## 根 CLAUDE.md
{粘贴}

## 模块级 CLAUDE.md 列表
{粘贴}

## docs/entry-points.md
{粘贴}

## docs/glossary.md
{粘贴}

## 最近一个月变更文件列表
{粘贴 git log --since="30 days ago" --name-only 输出}

## 关键代码片段（可选）
{粘贴最近变更的核心代码}

# 输出格式
## 总体健康度（优秀 / 良好 / 一般 / 差）
## 发现的不一致项（按优先级 P0/P1/P2 分类）
| 编号 | 优先级 | 文档位置 | 问题描述 | 建议修复 | 是否自动可修复 |
|---|---|---|---|---|---|
## 建议修复动作
## 需要人工确认的区域
```

#### 2.3 保存巡检报告

把 AI 输出保存到 `docs/reports/doc-rot-{YYYY-MM-DD}.md`。

#### 2.4 启用 Loop 模式 doc-rot-loop（推荐月度 / 季度巡检）

> **原则**：单次 prompt 容易产出"50 条 P2 nitpick + 0 条可落地动作"的报告。doc-rot-loop 强制按 DR1–DR4 四类分组、P0/P1/P2 严格分级、每条腐化必须带"修复成本 + 修复方式 + 责任人方向"，直接可转 issue。  
> **配套 skill**：`AI_工作流SOP_阶段5_Skill_doc-rot-loop.md`。

| 场景 | 推荐模式 |
|---|---|
| 临时对单个文件做一致性检查 | doc-rot-inspection 即可 |
| 月度全量巡检 | **doc-rot-loop** |
| 季度 OKR review 前盘点 | **doc-rot-loop** |
| 接手老项目首次盘点 | **doc-rot-loop** |
| "文档与代码严重不一致"事故复盘 | **doc-rot-loop** |

**4 类文档（DR1–DR4）**：
- DR1 CLAUDE.md & 全局配置
- DR2 入口地图 & API 契约
- DR3 模块文档 & 术语表
- DR4 AI Skill 模板

**优先级判定标准**：
- **P0（本周修）**：文档与代码冲突且会误导开发者；已废弃接口仍在文档推荐使用；关键约束已无人遵守
- **P1（本月修）**：偏差较小但需修正；新增功能未同步术语表/入口地图
- **P2（下季度前修）**：可读性、风格不统一、可优化但不影响 AI 工作流

**健康度评分公式**：

```
单类健康度 = 100 - (P0数 × 15) - (P1数 × 5) - (P2数 × 1)
加权总分 = DR1×0.3 + DR2×0.25 + DR3×0.3 + DR4×0.15
```

参考标准：≥90 优秀 / 75-89 良好 / 60-74 一般 / <60 差（建议暂停部分新功能开发先修文档）

**调用方式**：
- 通用 prompt：见 `AI_工作流SOP_阶段5_Skill_doc-rot-loop.md` § 5
- Claude Code 命令：`/doc-rot-loop`（默认 30 天）/ `/doc-rot-loop "90 days ago"`（季度）
- Cursor：见 skill 文档 § 7

**停止条件**：AC1–AC6 全 ✅ 立即停 / 最多 2 轮自查 / P0 上限 5 条（超过说明分级偏严）。

**输出衔接**：
- 行动清单 P0 → 同步到团队周会议程，立即分配负责人
- 行动清单 P1 → 进入本阶段 §3 「更新文档并记录变更日志」
- DR2 / DR3 问题 → 回触 reverse-loop 局部更新对应模块文档
- DR4 问题 → 触发本阶段 §4 「优化 AI skill」
- 加权总分 → 进入本阶段 §5 月度健康报告

---

### 步骤 3：更新文档并记录变更日志

#### 3.1 根据巡检结果更新文档

- 只修正确实已变更的内容；
- 不要一次性大规模重写，避免引入新的错误；
- 如果某个术语已废弃，标注为“已废弃，保留供历史参考”。

#### 3.2 记录 `CLAUDE.md` 变更日志

每次更新 `CLAUDE.md` 时，在 `docs/claude-md-changelog.md` 中追加：

```markdown
## 2026-06-19
- 变更文件：CLAUDE.md
- 变更原因：新增订单模块后补充包结构约定
- 影响范围：所有新模块必须遵循 `com.example.{模块}.domain` 分包
- 审批人：张三
- Diff 摘要：新增“包结构约定”章节；删除过时的 Swagger 配置说明。
```

#### 3.3 把腐化项转化为具体任务

对于 P0/P1 问题，创建 issue：

```markdown
- [ ] DOC-001: 更新 docs/entry-points.md，补充 /api/v2/orders
- [ ] DOC-002: 修正术语表“订单状态”的英文命名
- [ ] DOC-003: 补充 payment 模块的幂等性说明
```

---

### 步骤 4：优化 AI skill

#### 4.1 收集失败案例

在每次使用 AI skill 后，记录以下情况：

- AI 输出不符合预期的地方；
- 需要多次往返才能澄清的问题；
- 生成的代码/测试需要大量人工修正的地方。

#### 4.2 每季度 review skill

每季度召开一次 30 分钟 skill review 会议（或异步 review），讨论：

- 哪些 prompt 效果最好？
- 哪些 prompt 已过时？
- 是否需要新增 skill？
- 是否需要根据模型版本调整措辞？

#### 4.3 更新 skill 文件

直接修改 `docs/ai-skills/{skill}.md` 中的通用 prompt 和注意事项，并记录更新日志：

```markdown
## 更新历史
- 2026-06-19: 增加对 @MockBean 的明确要求，避免 AI 生成无法运行的测试。
```

---

### 步骤 5：度量与汇报

#### 5.1 计算核心指标

| 指标 | 计算方式 | 目标 |
|---|---|---|
| 文档覆盖率 | 有 `docs/modules/` 的核心模块数 / 总核心模块数 | ≥ 80% |
| CLAUDE.md 新鲜度 | 最近 30 天更新过的 `CLAUDE.md` 占比 | ≥ 70% |
| AI 生成测试通过率 | AI 生成测试首次运行通过率 | ≥ 60%（逐步提升） |
| AI 预审查问题采纳率 | 被采纳的 AI 建议 / AI 总建议数 | ≥ 50% |
| 文档腐化检出率 | 每月巡检发现的不一致项数 / 检查项总数 | 趋于 0 |
| 正向迭代闭环率 | 完成文档同步的交付功能数 / 总功能数 | ≥ 80% |

#### 5.2 生成月度健康报告

创建 `docs/reports/workflow-health-{YYYY-MM-DD}.md`：

```markdown
# AI 开发工作流健康报告：2026-06

## 核心指标
| 指标 | 本月 | 上月 | 目标 | 状态 |
|---|---|---|---|---|
| 文档覆盖率 | 75% | 60% | 80% | 🟡 |
| CLAUDE.md 新鲜度 | 85% | 70% | 70% | ✅ |
| AI 测试通过率 | 55% | 40% | 60% | 🟡 |
| 腐化检出率 | 5 | 12 | 0 | 🟡 |

## 本月主要问题
1. ...

## 下月改进计划
1. ...
```

---

## 4. 检查清单

- [ ] PR 流程中已集成 `check_claude_md_refs.py`；
- [ ] PR 流程中已集成 `check_api_doc_sync.py`（或等价的静态检查）；
- [ ] 每月已运行一次 AI 深度文档腐化巡检（建议优先 doc-rot-loop）；
- [ ] 如使用 doc-rot-loop，已检查 P0 条目 ≤ 5 且全部已分配负责人；
- [ ] 巡检报告已保存到 `docs/reports/doc-rot-{日期}.md`；
- [ ] `CLAUDE.md` 每次更新都已记录到 `docs/claude-md-changelog.md`；
- [ ] 发现的腐化项已转化为具体 issue 并分配负责人；
- [ ] `docs/ai-skills/` 已根据实战经验迭代；
- [ ] 每月已生成工作流健康报告（含 doc-rot-loop 加权总分趋势）。

---

## 5. 常见问题

### Q1：文档腐化检查脚本只能查机械一致性，语义不一致怎么办？

**答**：机械一致性用脚本，语义一致性用 AI 月度巡检。不要试图用脚本解决所有问题，否则维护成本过高。

### Q2：团队太忙，每月巡检做不完怎么办？

**答**：从最小版本开始：只检查 `CLAUDE.md` 是否超过 200 行、`docs/entry-points.md` 是否与代码一致。后续逐步扩展。

### Q3：AI 巡检报告太泛，不落地怎么办？

**答**：在 prompt 中明确要求输出“P0/P1/P2 分类 + 具体文件位置 + 建议修复动作 + 是否自动可修复”。报告必须转化为 issue 才算落地。

### Q4： skill 优化谁来负责？

**答**：建议指定一名“AI 工作流负责人”（可以是技术负责人兼职），每季度组织一次 skill review。也可以把优化任务分摊给每个使用 AI 的开发者，每次使用后反馈问题。

---

## 6. 模板速查

### check_claude_md_refs.py

```python
#!/usr/bin/env python3
import re
import sys
from pathlib import Path

CLAUDE_FILES = ["CLAUDE.md"] + list(Path(".").rglob("*/CLAUDE.md"))
REF_PATTERNS = [
    r"`?docs/([a-zA-Z0-9_\-/]+\.md)`?",
    r"\[.*?\]\(docs/([a-zA-Z0-9_\-/]+\.md)\)",
    r"docs/([a-zA-Z0-9_\-/]+\.md)",
]

def find_refs(content):
    refs = set()
    for pattern in REF_PATTERNS:
        refs.update(re.findall(pattern, content))
    return refs

errors = []
for claude_file in CLAUDE_FILES:
    content = claude_file.read_text(encoding="utf-8")
    refs = find_refs(content)
    for ref in refs:
        target = Path("docs") / ref
        if not target.exists():
            errors.append(f"{claude_file}: 引用不存在 {target}")

if errors:
    print("发现 CLAUDE.md 引用问题：")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print("CLAUDE.md 引用检查通过。")
```

### check_api_doc_sync.py

```python
#!/usr/bin/env python3
import re
import sys
from pathlib import Path

CONTROLLER_DIR = Path("src/main/java")
ENTRY_POINTS_FILE = Path("docs/entry-points.md")

def extract_controller_paths():
    paths = set()
    for file in CONTROLLER_DIR.rglob("*.java"):
        content = file.read_text(encoding="utf-8")
        mappings = re.findall(r'@(?:Get|Post|Put|Delete|Patch|Request)Mapping\(["\']([^"\']+)["\']', content)
        paths.update(mappings)
    return paths

def extract_doc_paths():
    if not ENTRY_POINTS_FILE.exists():
        return set()
    content = ENTRY_POINTS_FILE.read_text(encoding="utf-8")
    return set(re.findall(r'\| (/[^ |]+)', content))

controller_paths = extract_controller_paths()
doc_paths = extract_doc_paths()

missing_in_doc = controller_paths - doc_paths
missing_in_code = doc_paths - controller_paths

if missing_in_doc or missing_in_code:
    print("发现入口地图不一致：")
    for p in sorted(missing_in_doc):
        print(f"  - 代码中有但入口地图缺失: {p}")
    for p in sorted(missing_in_code):
        print(f"  - 入口地图中有但代码缺失: {p}")
    sys.exit(1)
print("入口地图同步检查通过。")
```

### doc-rot-inspection prompt

```markdown
# 角色
你是该 Java 项目的知识管理专员。请检查以下文档与代码的一致性，并输出腐化检测报告。

# 检查项
1. CLAUDE.md 中提到的关键类/接口是否仍然存在；
2. docs/entry-points.md 中的接口是否与代码一致；
3. docs/glossary.md 中的术语是否仍被代码使用；
4. 过去一个月合并的 PR 中，是否有变更未同步到文档；
5. docs/modules/ 中的模块文档是否与当前代码一致；
6. docs/ai-skills/ 中的 prompt 是否仍适用于当前模型版本；
7. 是否有新的业务术语、入口、状态机未更新到文档。

# 输入
{粘贴相关材料}

# 输出格式
## 总体健康度
## 不一致项（P0/P1/P2）
## 建议修复动作
## 需要人工确认的区域
```

### doc-rot-loop（Loop 版，强烈推荐月度/季度巡检使用）

> 完整模板见独立 skill 文档：`AI_工作流SOP_阶段5_Skill_doc-rot-loop.md` § 5  
> 与 doc-rot-inspection 差异：4 类 DR1–DR4 严格分组 + P0/P1/P2 判定标准 + 每条腐化必带修复成本/方式/责任人 + 健康度评分公式 + 最多 2 轮自查  
> 何时切换：见步骤 2 §2.4 场景对照表。

---

*上一阶段：[阶段 4：正向迭代](./AI_工作流SOP_阶段4_正向迭代_操作手册.md)*  
*回到总览：[AI 开发工作流 SOP](./AI_开发工作流_流程性_SOP.md)*
