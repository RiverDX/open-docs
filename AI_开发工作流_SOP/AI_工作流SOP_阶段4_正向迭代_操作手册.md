# 阶段 4：正向迭代 —— 操作手册

> **目标**：在共识确认的基础上，用 AI 辅助完成新功能开发、测试和代码审查。  
> **前提**：阶段 3 已完成，存在经过 review 的 PRD 和明确的开发任务。  
> **预计耗时**：单个任务约 2–8 小时，取决于复杂度。

---

## 1. 所需工具

| 工具 | 用途 | 是否必需 |
|---|---|---|
| **AI 工具**（Claude Code / Cursor / Copilot / 通义灵码） | 需求澄清、生成测试、生成代码、代码审查 | 是 |
| **Git / Git Worktree** | 代码版本管理、并行开发隔离 | 是 |
| **IntelliJ IDEA** | 编码、运行测试、调试 | 强烈建议 |
| **Maven / Gradle** | 构建、测试、依赖管理 | 是 |
| **Docker / Docker Compose** | 隔离数据库、Redis、Kafka 等中间件 | 使用 Worktree 时建议 |
| **JUnit 5 / Mockito / Testcontainers** | 单元测试与集成测试 | 是 |
| **CI/CD**（GitHub Actions / GitLab CI / Jenkins） | 自动化构建、测试、代码检查 | 建议 |
| **API 测试工具**（curl / Postman / IDEA HTTP Client） | 手动验证接口 | 建议 |

---

## 2. 环境准备

### 2.1 确认 PRD 和任务

- 打开 `docs/prd/{功能名}.md`；
- 确认要开发的 Issue 编号和验收标准；
- 确认根 `CLAUDE.md` 和模块级 `CLAUDE.md` 已就位。

### 2.2 确认项目可构建


---

## 3. 操作步骤

### 步骤 1：判断是否使用 Git Worktree

| 场景 | 是否使用 Worktree | 说明 |
|---|---|---|
| 修一行 typo / 注释 | 否 | 直接在主目录改 |
| 单个独立 bug | 可选 | 小改动可不起 |
| 新功能开发 | 是 | 避免污染主目录 |
| 多 AI 会话并行开发 | 是 | 必须隔离 |
| 长期实验性分支 | 是 | 必须隔离 |

---

### 步骤 2：创建独立开发环境（Worktree）

#### 2.1 创建 Worktree

```bash
# 在项目主目录执行
git worktree add ../{project}-{feature} -b feat/{feature}

# 进入工作区
cd ../{project}-{feature}
```

例如：

```bash
git worktree add ../shop-order-timeout -b feat/order-timeout
cd ../shop-order-timeout
```

#### 2.2 配置隔离的运行环境

复制环境配置模板：

编辑 ：

启动时指定 profile：


> **注意**：Worktree 只隔离代码，环境隔离对于开发来说还是很难做到，先做到代码隔离就可以了。

---

### 步骤 3：需求澄清（/grill-light 或 /grill-deep）

在写代码前，先用 AI 对 PRD 进行反向提问，澄清遗漏点。

使用 `docs/ai-skills/grill-light.md`：

```markdown
# 角色
你是一名需求分析师。请根据以下 PRD 和项目约定，向我提出 5–10 个关键问题，以澄清需求。

# 约束
- 每个问题必须具体、可回答；
- 优先关注边界条件、异常场景、权限、性能、并发；
- 不要问已经明确写在 PRD 中的内容。

# 输入
PRD：{粘贴 docs/prd/{功能名}.md}

## 根 CLAUDE.md
{粘贴}

## 模块级 CLAUDE.md（如有）
{粘贴}

# 输出
按优先级列出问题，并说明每个问题为什么重要。
```

把回答补充到 PRD 或模块文档中。如果问题涉及架构变更，返回阶段 3 重新确认。

---

### 步骤 4：生成测试（TDD）

使用 `docs/ai-skills/tdd.md`：

```markdown
# 角色
你是一名 Java / SpringBoot 测试工程师。请为以下功能先写测试，再写实现。

# 约束
- 优先写单元测试；
- 涉及数据库、缓存、外部服务时，使用 @MockBean 或 Testcontainers；
- 每个测试必须明确 Arrange / Act / Assert；
- 不要只测 happy path，必须覆盖边界条件；
- 输出完整的 JUnit 5 + Mockito 测试代码。

# 输入
PRD：{粘贴}

## 根 CLAUDE.md
{粘贴}

## 模块级 CLAUDE.md
{粘贴}

## 相关现有代码
{粘贴相关类}

# 任务
1. 列出需要测试的用例（含边界条件）；
2. 写出第一个失败的测试（RED）；
3. 写出让测试通过的最小实现（GREEN）；
4. 如果有必要，建议重构方向。
```

#### 测试生成后的审查要点

- 是否使用了 `@ExtendWith(MockitoExtension.class)` 而不是直接 new 对象；
- 是否使用了 `@MockBean` 正确注入 Spring 管理的依赖；
- 数据库相关测试是否使用了 `@DataJpaTest` 或 Testcontainers；
- 边界条件是否覆盖：空集合、null、最大值、重复请求、并发；
- 测试名称是否清晰表达意图。

#### 启用 Loop 模式（推荐新功能、核心模块）

> **原则**：tdd 是「单次提问」，AI 跑完就停，容易出现"测试很多但全是 happy path"或"断言恒真"；tdd-loop 是「闭环」，AI 自己按 TC1–TC6 测试矩阵自查并补齐边界、并发、事务回滚等关键用例。  
> **配套 skill**：`AI_工作流SOP_阶段4_Skill_tdd-loop.md`（已在本 SOP 中提供完整模板）。

| 场景 | 推荐模式 |
|---|---|
| 纯函数 / 修 typo / 复用已有测试结构 | tdd 即可 |
| 新功能 / 新接口 / 新业务规则 | **tdd-loop** |
| 旧模块第一次补测试（覆盖率从 0 起步） | **tdd-loop** |
| 涉及事务、并发、外部调用、幂等性 | **tdd-loop** |
| 跑过一次 tdd 但只测了 happy path | **tdd-loop** |

**TC1–TC6 测试矩阵（人工抽查也用这套）**：

| TC | 标准 | 抽查方式 |
|---|---|---|
| TC1 | happy path：每条 AC 至少 1 个测试 | 对照 PRD AC 列表 |
| TC2 | 异常路径：每个 try/catch 至少 1 条 | grep 业务代码的 throw / catch |
| TC3 | 边界：null / 空集合 / 最大值 | 看测试方法名是否有 `null`/`empty`/`max` 关键字 |
| TC4 | 并发与幂等 | 找有无 CompletableFuture / 重复调用同方法的测试 |
| TC5 | 事务回滚：中途失败的多步写入 | 找 mock 中途抛异常的测试 |
| TC6 | 断言可证伪：不是恒真 | 全文搜 `assertNotNull(result)`、`assertTrue(true)`，应为 0 |

**调用方式**：

- 通用 prompt（任何 AI 工具）：见 `AI_工作流SOP_阶段4_Skill_tdd-loop.md` § 5；
- Claude Code 命令：`/tdd-loop ISSUE-003-order-timeout`；
- Cursor：见 skill 文档 § 7。

**停止条件**：TC1–TC6 全 ✅ 立即停 / 最多自查 2 轮 / 不让 AI 为提升覆盖率堆砌无意义测试。

---

### 步骤 5：实现代码

在 AI 生成测试后，可以让 AI 继续生成实现代码，也可以自己写。如果选择 AI 生成：

```markdown
# 角色
你是一名 Java / SpringBoot 开发者。请基于以上测试和 PRD，写出最小实现让测试通过。

# 约束
- 严格遵循 CLAUDE.md 中的分层和包结构约定；
- 不要过度设计，先让测试通过；
- 禁止跨层调用；
- 涉及数据库操作时，必须使用 Repository；
- 涉及外部调用时，必须通过 Client/Adapter 封装。

# 输入
PRD：{粘贴}
测试：{粘贴}
CLAUDE.md：{粘贴}

# 输出
完整的 Java 实现代码，包含所有新建/修改的文件。
```

#### 实现后的人工审查

- 是否违反 CLAUDE.md 中的分层约定；
- 是否有空指针、并发、事务问题；
- 是否有魔法值、硬编码字符串；
- 命名是否一致；
- 是否引入不必要的依赖。

---

### 步骤 6：AI 预审查（Codex Review 前移）

使用 `docs/ai-skills/codex-review.md`：

```markdown
# 角色
你是一名 Java 代码审查员。请审查以下代码变更，重点关注：
1. 是否违反 CLAUDE.md 中的约定；
2. 是否有明显的并发、空指针、事务、安全问题；
3. 测试是否覆盖了关键路径；
4. 命名和包结构是否一致；
5. 是否有重复代码或可以提取的公共逻辑。

# 输入
## CLAUDE.md
{粘贴}

## 变更 diff
{粘贴 git diff 内容}

# 输出
| 问题级别 | 位置 | 问题描述 | 建议修复 | 是否必须修复 |
|---|---|---|---|---|
| 严重 / 建议 / 提示 | 文件名:行号 | ... | ... | 是/否 |
```

#### 处理 AI 审查意见

- **严重**：必须修复，否则不进入人工审查；
- **建议**：评估后决定是否修复，不修复需说明原因；
- **提示**：记录，后续迭代中考虑。

#### 启用 Loop 模式（推荐核心模块、大 diff、PR 前最后一关）

> **原则**：codex-review 是「单次提问」，AI 倾向罗列大量建议但严重度全部相同；codex-review-loop 强制按 RC1–RC6 六维度组织、按 SEV1/SEV2/SEV3 三级严重度分级、每条问题必须给文件:行号 + 代码片段 + 置信度。  
> **配套 skill**：`AI_工作流SOP_阶段4_Skill_codex-review-loop.md`。

| 场景 | 推荐模式 |
|---|---|
| diff < 50 行的小改 | codex-review 即可 |
| 只改测试或文档 | codex-review 即可 |
| diff > 200 行 | **codex-review-loop** |
| 改动涉及核心模块（订单/支付/用户/权限） | **codex-review-loop** |
| 跑过一次 codex-review 但建议太散 | **codex-review-loop** |
| PR 前最后一道关 | **codex-review-loop** |

**6 维度（RC1–RC6）**：
- RC1 PRD 一致性
- RC2 CLAUDE.md 约定遵循
- RC3 测试覆盖与质量（直接读 tdd-loop 自查表的 TC6）
- RC4 并发 / 事务 / 空指针 / 安全
- RC5 命名 / 分层 / 重复代码
- RC6 文档同步（CLAUDE.md / docs/）

**严重度分级**：
- **SEV1（阻断合并）**：bug、安全漏洞、违反核心约束、必然导致线上事故
- **SEV2（应在本 PR 修）**：可能出问题、违反一般约定、明显代码异味
- **SEV3（可下个 PR 跟）**：可读性、命名、轻微重复、文档优化

**调用方式**：

- 通用 prompt：见 `AI_工作流SOP_阶段4_Skill_codex-review-loop.md` § 5；
- Claude Code 命令：`/codex-review-loop`（自动取 `git diff main...HEAD`）；
- Cursor：见 skill 文档 § 7。

**停止条件**：AC1–AC6 全 ✅ 立即停 / 最多自查 2 轮 / SEV1 不超过 5 条（超过说明分级偏严，需降级或合并）。

---

### 步骤 7：本地验证

#### 7.1 运行测试

```bash
# Maven
mvn test

```

确保所有测试通过，包括 AI 生成的测试和你手动补充的测试。

#### 7.2 运行静态检查

```bash
# 使用 Maven 插件（如 Checkstyle、SpotBugs、PMD）
mvn checkstyle:check spotbugs:check

# 或使用 SonarQube 扫描
mvn sonar:sonar
```

#### 7.3 手动验证接口

```bash
curl -X POST http://localhost:8081/api/v1/orders/{id}/timeout \
  -H "Content-Type: application/json"
```

检查数据库状态、日志输出是否符合预期。

---

### 步骤 8：人工审查与合并

#### 8.1 提交代码

```bash
git add .
git commit -m "feat(order): 订单超时自动取消

- 新增 OrderTimeoutJob 定时任务
- 新增超时取消业务逻辑与测试
- 更新 PRD 和术语表

ISSUE-003"
```

#### 8.2 推送并创建 PR / MR

```bash
git push origin feat/order-timeout
```

在 GitHub / GitLab 创建 PR，并关联 Issue。

#### 8.3 人工审查关注点

| 维度 | 关注点 |
|---|---|
| 业务正确性 | 实现是否与 PRD 和共识一致？ |
| 测试质量 | 测试是否覆盖关键路径和边界？是否有“假绿”？ |
| 架构影响 | 是否引入新的依赖？是否破坏分层？ |
| 性能与安全 | 是否有 N+1 查询、SQL 注入、并发问题？ |
| 文档同步 | 是否更新了 PRD、CLAUDE.md、术语表？ |

#### 8.4 合并

- 所有 CI 检查通过后合并；
- 使用 `merge --no-ff` 保留 feature 分支历史；
- 合并后删除远程 feature 分支（如果不再需要）。

---

### 步骤 9：清理 Worktree

```bash
# 回到主目录
cd ../{project}

# 合并分支后删除 worktree
git worktree remove ../{project}-{feature}

# 删除远程分支（可选）
git push origin --delete feat/{feature}
```

---

## 4. 检查清单

- [ ] 已判断是否需要 Worktree，并已配置隔离环境（如使用）；
- [ ] 已使用 `/grill-light` 或 `/grill-deep` 澄清需求；
- [ ] 已选择 tdd（单次）或 tdd-loop（Loop 模式），且模式选择有理由；
- [ ] 如使用 tdd-loop，已检查 TC1–TC6 自查表，且抽查至少 2 项断言可证伪性；
- [ ] 已生成测试，且覆盖关键路径和边界条件；
- [ ] 已实现代码，且符合 CLAUDE.md 的分层与命名约定；
- [ ] 已选择 codex-review（单次）或 codex-review-loop（Loop 模式），且模式选择有理由；
- [ ] 如使用 codex-review-loop，SEV1 问题已全部修复，SEV2 已评估处理；
- [ ] 本地测试全部通过；
- [ ] 静态检查无严重问题；
- [ ] 已提交 PR / MR 并通过 CI；
- [ ] 已进行人工审查并处理反馈；
- [ ] 已合并代码并清理 Worktree；
- [ ] 如有新术语/新入口/新约定，已同步更新 `docs/` 和 `CLAUDE.md`；
- [ ] Loop 模式产出的「需人工确认清单」已逐项处理或转入下一阶段。

---

## 5. 常见问题

### Q1：AI 生成的测试无法运行怎么办？

**答**：先检查是否是 Spring 上下文注入问题（如缺少 `@SpringBootTest`、`@MockBean` 用错）。如果是测试逻辑错误，人工修正测试，并把修正点记录到 `docs/ai-skills/tdd.md` 的“注意事项”中，持续优化 prompt。

### Q2：Worktree 构建太慢，每次都要重新下载依赖？

**答**：Maven/Gradle 的本地仓库是共享的，但构建缓存和 `target/`/`build/` 不共享。可以：
1. 使用 `mvn -o` 离线模式；
2. 配置 Gradle 构建缓存共享；
3. 使用预编译的 CI 镜像。

### Q3：多模块项目中一个功能涉及多个模块，怎么开发？

**答**：
1. 先在主目录创建整体工作分支；
2. 对改动最大的模块创建 Worktree；
3. 通过 `mvn install` 或 `gradle publishToMavenLocal` 让其他模块引用本地快照；
4. 最后统一在一个 PR 中合并，但提交记录保持清晰。

### Q4：AI 建议的架构改动太大，要不要采纳？

**答**：在迭代中，AI 倾向于“improve architecture”。如果改动超出本次 PRD 范围，应拒绝，并告知 AI 只解决当前任务。把重构建议记录到 `docs/adr/` 或 `docs/prd/` 的“未来优化”中，后续单独立项。

---

## 6. 模板速查

### Worktree 创建脚本

```bash
#!/bin/bash
# scripts/wt-new.sh
PROJECT_NAME=$1
FEATURE=$2

if [ -z "$PROJECT_NAME" ] || [ -z "$FEATURE" ]; then
  echo "Usage: wt-new.sh <project-name> <feature-name>"
  exit 1
fi

git worktree add ../${PROJECT_NAME}-${FEATURE} -b feat/${FEATURE}
cd ../${PROJECT_NAME}-${FEATURE}

cp src/main/resources/application-dev.yml src/main/resources/application-worktree.yml

echo "Worktree created at ../${PROJECT_NAME}-${FEATURE}"
echo "Next steps:"
echo "1. Edit application-worktree.yml to use isolated ports/database"
echo "2. docker-compose -f docker-compose.${FEATURE}.yml up -d"
echo "3. Start coding"
```

### tdd 通用 prompt

```markdown
# 角色
你是一名 Java / SpringBoot 测试工程师。请为以下功能先写测试，再写实现。

# 约束
- 优先单元测试；
- 数据库/缓存/外部服务用 @MockBean 或 Testcontainers；
- 覆盖边界条件；
- 输出 JUnit 5 + Mockito 代码。

# 输入
PRD：{粘贴}
CLAUDE.md：{粘贴}
相关代码：{粘贴}

# 任务
1. 列出测试用例；
2. 写出 RED 测试；
3. 写出 GREEN 实现；
4. 建议重构方向。
```

### codex-review 通用 prompt

```markdown
# 角色
你是一名 Java 代码审查员。请审查以下 diff。

# 关注
1. 是否违反 CLAUDE.md 约定；
2. 并发、空指针、事务、安全问题；
3. 测试覆盖；
4. 命名与包结构；
5. 重复代码。

# 输入
CLAUDE.md：{粘贴}
diff：{粘贴}

# 输出
| 级别 | 位置 | 问题 | 建议 | 是否必须修复 |
```

### tdd-loop / codex-review-loop（Loop 版）

> 完整模板分别见独立 skill 文档：  
> · `AI_工作流SOP_阶段4_Skill_tdd-loop.md` § 5  
> · `AI_工作流SOP_阶段4_Skill_codex-review-loop.md` § 5  
>
> 与单次版差异：  
> · tdd-loop —— 6 条测试矩阵 TC1–TC6 + 最多 2 轮自查 + 强制输出"测试矩阵 + 自查表 + 需人工确认清单"  
> · codex-review-loop —— 6 维度 RC1–RC6 + 3 级严重度 SEV1/2/3 + 每条问题强制带文件:行号 + 置信度  
>
> 何时切换：见步骤 4、步骤 6 中的场景对照表。

---

*上一阶段：[阶段 3：共识确认](./AI_工作流SOP_阶段3_共识确认_操作手册.md)*  
*下一阶段：[阶段 5：持续演化](./AI_工作流SOP_阶段5_持续演化_操作手册.md)*
