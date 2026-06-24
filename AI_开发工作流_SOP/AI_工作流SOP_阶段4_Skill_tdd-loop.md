# Skill：tdd-loop —— 测试驱动开发的 Loop 版本

> **定位**：把 SOP 阶段 4 中的 `tdd`（单次提问版）升级为 **Loop 版本** —— 让 AI 自己按测试质量验收标准自查、修正、停止，避免「测试看起来很多但全是 happy path」「测试通过但实际没测到关键路径」的常见陷阱。  
> **关联文件**：`AI_工作流SOP_阶段4_正向迭代_操作手册.md`、`AI_工作流SOP_阶段2_Skill_reverse-loop.md`  
> **理论基础**：Loop Engineering 4 模块（目标 / 步骤 / 检查 / 停止）+ TDD 红绿重构循环。  
> **版本**：V1.0（2026-06-23）

---

## 1. 目标

让 AI 在为新功能写测试时，**不只是"写一堆 @Test 方法"**，而是按测试质量标准自查并补全：边界条件、异常路径、并发场景、事务回滚、幂等性。最终输出一份「能让人放心合并」的测试代码，而不是"看起来通过但漏测一片"的假绿。

与 `tdd`（单次版）的差异：

| 对比项 | tdd（旧） | tdd-loop（新） |
|---|---|---|
| 交互模式 | 单次提问 → 单次输出 | 多轮自查 → 收敛输出 |
| 用例覆盖 | 看 AI 心情，多以 happy path 为主 | 强制按 TC1–TC6 测试矩阵覆盖 |
| 假绿防御 | 无（容易写"恒真"断言） | 强制要求每个断言写明"为什么这条断言能 fail" |
| 边界条件 | 经常漏 null、空集合、并发 | TC4 强制覆盖 |
| 越界控制 | 无（可能生成 200 行不必要的测试） | 最多 2 轮，超时即输出"卡点报告" |
| 适合人群 | 已熟悉 TDD 的开发者 | 小白与新手 |

---

## 2. 触发条件

满足任一条即可启用 tdd-loop 而不是 tdd：

- 写新功能、新接口、新业务规则的测试；
- 旧模块第一次补测试（覆盖率从 0 起步）；
- 已经跑过一次 tdd，但测试明显只测了 happy path；
- 该功能涉及事务、并发、外部调用、幂等性等容易出错的场景；
- 进入 PR 前的最后一道测试质量关。

不需要 Loop 的场景（用 tdd 即可）：

- 给一个纯函数（无副作用、无并发、无状态）补单测；
- 修一个 typo / 注释，不涉及行为变更；
- 复用现有测试结构、只是新增一个相似断言。

---

## 3. 输入

| 输入项 | 是否必需 | 说明 |
|---|---|---|
| PRD / 需求描述 | 必需 | `docs/prd/{功能名}.md` 或等价描述 |
| 验收标准（AC） | 必需 | PRD 里的 AC 列表 |
| 相关现有代码 | 必需 | 至少包含被测类、依赖接口 |
| 根 `CLAUDE.md` | 必需 | 测试策略、技术栈 |
| 模块级 `CLAUDE.md` | 可选 | 模块的特殊约定 |
| 现有测试样例 | 强烈建议 | 让 AI 学项目风格 |
| 数据库 schema | 涉及持久化时必需 | 字段约束、唯一索引、默认值 |

---

## 4. 输出

跑完一次 Loop，AI 必须输出 **3 段**：

### 4.1 完整测试代码

- 含所有 `@Test` 方法（含边界、异常、并发）；
- 测试名清晰表达意图：`should_returnError_when_userIdIsNull` 风格；
- 每个测试明确 Arrange / Act / Assert 三段。

### 4.2 测试质量自查表（核心新增产物）

```markdown
| 验收标准 | 评分 | 证据 / 卡点 |
|---|---|---|
| TC1 happy path 覆盖（每个 AC 至少 1 条） | ✅ / ⚠️ / ❌ | 测试方法名 |
| TC2 异常路径覆盖（每个 try/catch 至少 1 条） | ✅ / ⚠️ / ❌ | ... |
| TC3 null / 空集合 / 最大值边界 | ✅ / ⚠️ / ❌ | ... |
| TC4 并发 / 幂等 / 重复请求 | ✅ / ⚠️ / ❌ | ... |
| TC5 事务回滚 / 部分失败 | ✅ / ⚠️ / ❌ | ... |
| TC6 断言可证伪（不是恒真） | ✅ / ⚠️ / ❌ | ... |
```

### 4.3 需人工确认清单

```markdown
- [ ] 需要业务方确认的边界规则：xxx
- [ ] 需要 Testcontainers 或集成测试才能验证的部分：xxx
- [ ] 当前 mock 是否反映真实依赖行为：xxx
```

---

## 5. 通用 Prompt（核心模板，小白可直接复制粘贴）

```markdown
# 角色
你是一名严格的 Java / SpringBoot 测试工程师，目标是用 Loop 方式自我闭环地为以下功能写测试。
你的工作不是"写出测试"，而是"写出能让 reviewer 放心合并的测试"。

# 任务
为功能 {功能名} 编写测试代码（JUnit 5 + Mockito，必要时用 Testcontainers）。

# 流程（必须按此顺序，不要跳步）
1. 读懂 PRD 和 AC，列出本功能要测的"测试矩阵"（按 TC1–TC6 维度）
2. 按矩阵生成完整测试代码（先 RED 后 GREEN）
3. 按下方"验收标准"逐项自查并填入自查表（✅/⚠️/❌ + 证据）
4. 对 ⚠️/❌ 项补充缺失测试（最多 2 轮）
5. 输出最终测试代码 + 自查表 + 需人工确认清单

# 验收标准（每项必须有具体测试方法名作证据）
- TC1 happy path：PRD 中每条 AC 至少对应 1 个测试方法
- TC2 异常路径：业务代码中每个 try/catch、throw 至少对应 1 条测试
- TC3 边界条件：null 入参、空集合、最大值/最小值至少各 1 条
- TC4 并发与幂等：涉及共享状态、外部调用回调时，至少 1 条并发或重复请求测试
- TC5 事务与失败：涉及多步写入时，至少 1 条"中途失败 → 期望回滚"测试
- TC6 断言可证伪：每个断言必须能被一个错误实现 fail；禁止用 assertNotNull(result) 这种"几乎恒真"的断言

# 测试代码硬性约束
- 不要测试框架代码（如 Spring 自动注入）；只测业务逻辑
- Mock 必须只 mock 直接依赖，不 mock 被测类本身
- 数据库相关：优先 @DataJpaTest 或 Testcontainers，禁止 @SpringBootTest 用于纯单元测试
- 每个 @Test 必须有 // Arrange // Act // Assert 注释或等效结构
- 测试名格式：should_<结果>_when_<条件>，或 <方法名>_<场景>_<预期>

# 停止条件
- 全部 TC1–TC6 评为 ✅ → 立即停止，输出最终结果
- 已自查修改 2 轮仍有 ⚠️/❌ → 停止，不要继续猜
  · 在"需人工确认清单"里明确写出：卡在哪里 + 缺什么信息 + 建议如何确认
- 严禁为"提升覆盖率"而堆砌无意义的测试

# 输入
## PRD
{粘贴 docs/prd/{功能名}.md}

## 根 CLAUDE.md
{粘贴}

## 模块级 CLAUDE.md
{粘贴；无写"无"}

## 相关现有代码
{粘贴被测类、依赖接口}

## 现有测试样例（供学习项目风格）
{粘贴 1–2 个本项目已有的测试}

# 输出格式（严格遵循）
## 一、测试矩阵（先输出，再写代码）
| TC | 维度 | 用例描述 | 对应 AC | 测试方法名 |
|---|---|---|---|---|

## 二、完整测试代码
{Java 代码块，含所有 @Test 方法}

## 三、自查表
| 验收标准 | 评分 | 证据（测试方法名） |
|---|---|---|
| TC1 happy path | ✅/⚠️/❌ | ... |
| TC2 异常路径 | ✅/⚠️/❌ | ... |
| TC3 边界条件 | ✅/⚠️/❌ | ... |
| TC4 并发与幂等 | ✅/⚠️/❌ | ... |
| TC5 事务与失败 | ✅/⚠️/❌ | ... |
| TC6 断言可证伪 | ✅/⚠️/❌ | ... |

迭代轮次：{1 / 2}
是否达到停止条件：{是 / 否（原因）}

## 四、需人工确认清单
- [ ] ...
```

---

## 6. Claude Code 适配

把上面的通用 prompt 保存为 `.claude/commands/tdd-loop.md`：

```markdown
---
description: 用 Loop 方式为指定功能生成高质量测试
argument-hint: <功能名 / Issue ID>
---

请用 tdd-loop 模式为 $1 写测试。

# 步骤
1. 读 docs/prd/$1.md（或 Issue $1），抽出全部 AC
2. 读相关代码（被测类 + 依赖接口）
3. 按 docs/ai-skills/tdd-loop.md 的 TC1–TC6 测试矩阵覆盖
4. 最多自查 2 轮，超出即停并输出"卡点报告"
5. 测试文件写入 src/test/java/.../ 下对应位置
6. 自查表写入 docs/test-reports/$1-tdd-loop.md
```

使用方式：

```
/tdd-loop ISSUE-003-order-timeout
```

---

## 7. Cursor 适配

`.cursorrules` 片段：

```text
当用户输入以 "写测试" "tdd" "tdd-loop" 开头时，按以下规则执行：

1. 默认调用 docs/ai-skills/tdd-loop.md 中的通用 prompt
2. 必须遵守 TC1–TC6 测试矩阵和 2 轮上限
3. 禁止只写 happy path
4. 禁止 assertNotNull(result) / assertTrue(true) 这种几乎恒真的断言
5. 输出必须包含：测试矩阵、测试代码、自查表、需人工确认清单
```

---

## 8. 注意事项 / 常见陷阱

### 8.1 AI 写测试最容易掉的 5 个坑

| 坑 | 表现 | 应对 |
|---|---|---|
| **假绿断言** | `assertNotNull(result)`、`assertTrue(true)`、捕获异常后没断言 | TC6 强制要求"断言可证伪" |
| **过度 mock** | mock 被测类自己，或 mock 静态方法绕过逻辑 | prompt 里限定"只 mock 直接依赖" |
| **happy path 堆砌** | 5 个测试全是正向，0 个边界 | TC1 + TC3 强制比例 |
| **Spring 上下文滥用** | 给纯函数也加 @SpringBootTest，启动 10 秒 | 测试代码硬性约束第 3 条 |
| **测试名空洞** | `test1()`、`testOrder()` | 强制 should_xxx_when_yyy 命名 |

### 8.2 项目可加的自定义 TC（按需追加）

- **TC7**：DDD 项目—— 所有领域事件必须有 1 条"事件被发布"测试；
- **TC8**：金融/支付项目—— 所有金额计算必须用 BigDecimal，且至少 1 条精度测试；
- **TC9**：消息系统—— 所有 Kafka/RabbitMQ 消费者必须有 1 条"重复消息幂等"测试；
- **TC10**：缓存场景—— 所有写 DB+写缓存的操作必须有 1 条"缓存失效"测试。

### 8.3 与其他 Skill 的衔接

- **跑完 tdd-loop 后** → 直接进入「步骤 5：实现代码」让 AI 写最小实现让测试通过；
- **如果 tdd-loop 报 ⚠️/❌ 太多** → 说明 PRD 不清晰，回阶段 3 grill-deep 重新澄清；
- **PR 合并前** → tdd-loop 的自查表可以作为 codex-review-loop 的输入项之一。

---

## 9. 一次最小可用示例

**输入**：

```
功能：订单 30 分钟未支付自动取消
PRD：docs/prd/order-timeout.md
AC：
  AC1 30 分钟未支付的订单自动取消并释放库存
  AC2 已支付的订单不被误取消
  AC3 取消失败时记录日志并重试 3 次
代码：OrderTimeoutJob.java, OrderService.java, InventoryClient.java
```

**期待 AI 输出（节选）**：

```markdown
## 一、测试矩阵
| TC | 用例 | AC | 方法名 |
|---|---|---|---|
| TC1 | 30 分钟未支付订单被取消 | AC1 | should_cancelOrder_when_timeoutAndUnpaid |
| TC1 | 库存被释放 | AC1 | should_releaseInventory_when_orderCancelled |
| TC2 | 已支付订单不被取消 | AC2 | should_notCancel_when_orderPaid |
| TC3 | 不存在的订单 ID | - | should_throwNotFound_when_orderIdInvalid |
| TC3 | 空订单列表 | - | should_doNothing_when_noTimeoutOrders |
| TC4 | 同一订单被两个 Job 同时取消 | AC1 | should_beIdempotent_when_concurrentCancel |
| TC5 | 库存释放失败应回滚订单状态 | AC1 | should_rollbackOrderStatus_when_inventoryReleaseFails |
| TC5 | 重试 3 次后仍失败 | AC3 | should_recordFailLog_when_retry3TimesFail |

## 三、自查表
| TC | 评分 | 证据 |
|---|---|---|
| TC1 happy path | ✅ | should_cancelOrder_when_timeoutAndUnpaid, should_releaseInventory_when_orderCancelled |
| TC2 异常路径 | ✅ | should_throwNotFound_when_orderIdInvalid |
| TC3 边界 | ✅ | should_doNothing_when_noTimeoutOrders |
| TC4 并发幂等 | ⚠️ | 有测试但用了 @Transactional，未真实模拟并发，建议改 CompletableFuture + 共享 Mock |
| TC5 事务回滚 | ✅ | should_rollbackOrderStatus_when_inventoryReleaseFails |
| TC6 断言可证伪 | ✅ | 全部使用 verify() 和具体值断言，无 assertNotNull/assertTrue(true) |

迭代轮次：2
是否达到停止条件：是（仅 TC4 一项保留为 ⚠️ 并已写入"需人工确认清单"）

## 四、需人工确认清单
- [ ] TC4 并发测试用 @Transactional 模拟，建议在 PR 前补一次 Testcontainers + 真实数据库的并发集成测试
- [ ] InventoryClient.releaseInventory() 重试策略目前 mock 为 3 次失败，需确认实际配置（@Retryable 还是手动 try-catch 循环）
```

这就是一次合格的 tdd-loop 输出 —— **不光给了代码，还把"哪里没测透、为什么没测透"讲清楚了**。

---

## 10. 版本历史

| 版本 | 日期 | 变更 |
|---|---|---|
| V1.0 | 2026-06-23 | 初始版本，基于 Loop Engineering 改造 tdd |
