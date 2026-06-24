# CLAUDE.md 使用指南：Java 项目 AI 上下文管理

> **目标**：让 CLAUDE.md 成为 Java / SpringBoot 项目中 AI 辅助开发的“上下文配置文件”，既约束 AI 行为，又不过度膨胀。  
> **适用场景**：使用 Claude Code、Cursor、GitHub Copilot、通义灵码等 AI 工具辅助开发的 Java 项目。  
> **配套文件**：`AI_开发工作流_流程性_SOP.md`、`AI_工作流SOP_阶段1_项目初始化_操作手册.md`、`AI_工作流SOP_阶段3_共识确认_操作手册.md`

---

## 1. 什么是 CLAUDE.md

`CLAUDE.md` 是放在项目中的 Markdown 文件，用来向 AI 传递**长期、稳定、项目专属**的上下文信息。

它告诉 AI：

- 这个项目用的是什么技术栈；
- 代码应该按什么分层和包结构写；
- 哪些事情绝对不能做；
- 测试应该怎么写；
- 业务规则和详细文档在哪里找。

你可以把它理解为：

> **AI 的新成员入职手册**——不是项目百科全书，而是让 AI 快速知道“在这个项目里该怎么干活”的最小必要信息。

---

## 2. 为什么要分层

一个 Java 项目的信息量很大。如果把所有信息都塞进根 `CLAUDE.md`，很快会超过 AI 的有效上下文窗口，导致：

- AI 抓不住重点；
- 每次会话都加载大量无关信息；
- 具体业务规则更新后，根文档也要频繁改动。

**分层的目的**：让 AI 在不同粒度上看到不同的约束。

```
根 CLAUDE.md          → 全局约束（所有 AI 会话都读）
模块级/域级 CLAUDE.md  → 局部约束（进入该模块/域时读）
过程梳理文档          → 业务知识（需要时查，不常驻上下文）
```

---

## 3. 三层结构详解

### 3.1 根 CLAUDE.md

**位置**：项目根目录 `CLAUDE.md`

**作用**：所有 AI 会话的默认上下文。AI 工具启动时通常会自动读取项目根目录的 `CLAUDE.md`。

**内容约束**：

- **< 200 行**（约 5k tokens）；
- 只包含**全局、长期稳定**的信息；
- 不包含具体业务规则，只保留**指针**；
- 用条目式，便于 AI 快速扫描。

**应包含的内容**：

| 章节 | 写什么 | 不写什么 |
|---|---|---|
| 项目类型 | 单体 / 多模块 / 微服务 | 每个模块的职责细节 |
| 技术栈 | Spring Boot 版本、JDK、数据库、ORM、缓存、消息队列 | 依赖版本变更历史 |
| 分层与包结构 | 包结构示例、各层职责 | 每个类的具体位置 |
| 核心约定 | 分层规则、数据访问规则、接口返回规则 | 具体业务规则 |
| 测试策略 | 单元测试、集成测试、Mock 规则 | 具体测试用例 |
| 文档指针 | 模块/域文档、术语表、入口地图、PRD 目录 | 具体业务内容 |
| 禁用清单 | 禁止跨层调用、禁止手写 SQL 等 | 理由说明（可简要） |
| 未知区域 | 暂时没搞清楚、需要谨慎处理的部分 | 猜测性结论 |

**示例**：

```markdown
# 项目名

## 项目类型
单体 SpringBoot 项目，单模块多业务域。

## 技术栈
- Spring Boot 3.2.0
- JDK 17
- Maven 3.9
- MySQL 8.0 + MyBatis-Plus
- Redis 7
- Kafka 3.x

## 分层与包结构
```
com.example
  ├── application       # 应用服务，编排领域对象
  ├── domain            # 领域层：实体、值对象、领域服务
  ├── infrastructure    # 基础设施：Repository 实现、外部客户端
  ├── interfaces        # 接口层：Controller、Listener、Job
  └── common            # 通用工具
```

## 核心约定
1. 不允许跨层调用（Controller 不能直接用 Repository）；
2. 不允许在 Service 中直接写 SQL；
3. 所有 Controller 必须返回统一响应体 `ApiResponse<T>`；
4. 涉及分布式事务必须使用 Saga 或事务消息；
5. 订单状态变更必须通过 StateMachine。

## 测试策略
- 单元测试：JUnit 5 + Mockito，覆盖 Service 核心逻辑；
- 集成测试：@SpringBootTest + Testcontainers，覆盖数据库/缓存；
- 接口测试：MockMvc；
- 所有 bug 修复必须附带回归测试。

## 文档指针
- 业务域文档：`docs/domains/`
- 术语表：`docs/glossary.md`
- 入口地图：`docs/entry-points.md`
- PRD：`docs/prd/`
- 架构决策：`docs/adr/`
- AI skill：`docs/ai-skills/`

## 禁用清单
- 禁止使用 `java.util.Date`，统一使用 `java.time`；
- 禁止在领域层引入 Spring 注解；
- 禁止手动拼接 SQL 字符串；
- 禁止在循环中调用外部 HTTP 接口。

## 未知区域
- 部分历史模块的分层不清晰，待重构；
- 微服务拆分策略尚未确定。
```

---

### 3.2 物理模块级 CLAUDE.md

**位置**：每个 Maven/Gradle 模块的根目录下，例如 `order/CLAUDE.md`。

**作用**：当 AI 会话进入某个 Maven/Gradle 模块时，加载该模块的专属约束。

**适用场景**：多模块项目（如 `auth`、`order`、`payment` 等模块）。

**内容约束**：

- **< 150 行**；
- 包含该模块的**结构性约定**；
- 不包含详细业务规则，只保留指针。

**应包含的内容**：

| 章节 | 写什么 |
|---|---|
| 职责 | 该模块负责什么 |
| 依赖 | 依赖的其他模块、外部服务、数据库 |
| 关键入口 | HTTP、消息、定时任务、外部回调 |
| 领域实体 | 核心实体名称 |
| 模块级约定 | 该模块内的红线（如不能直接调用其他模块的数据库） |
| 详细业务规则 | 指向 `docs/modules/{模块名}.md` |

**示例**：

```markdown
# 模块：order

## 职责
负责订单生命周期管理：创建、支付、发货、完成、取消。

## 依赖
- 依赖模块：user、inventory、payment
- 外部服务：用户中心、支付网关
- 数据库：db_order

## 关键入口
- HTTP：/api/v1/orders、/api/v1/orders/{id}/pay
- 消息：order.created、order.paid
- 定时任务：OrderTimeoutJob

## 领域实体
- Order、OrderItem、OrderPaymentRecord

## 模块级约定
- 本模块所有 Service 必须通过 OrderRepository 操作数据库；
- 不允许直接调用 payment 模块的数据库表；
- 订单状态变更必须通过 OrderStateMachine。

## 详细业务规则
见 `docs/modules/order.md`。
```

---

### 3.3 业务域级 CLAUDE.md

**位置**：`docs/domains/订单域.md` 或 `docs/modules/订单域.md`。

**作用**：当项目只有一个 Maven/Gradle 模块，但内部按 Controller/Service 划分为多个业务域时，为每个业务域提供上下文约束。

**适用场景**：单模块多业务域项目（最常见于中小型 SpringBoot 项目）。

**关键原则**：

- **不要为每个 Controller 创建一个 `CLAUDE.md`**；
- 按**业务域**划分，而不是按代码文件划分；
- 业务域的边界通常对应一个或多个 Controller、一组 Service、一个 DDD 聚合。

**内容约束**：

- **< 150 行**；
- 包含该业务域的**结构性约定**和**高度概括的业务约束**；
- 具体业务规则保留指针。

**应包含的内容**：

| 章节 | 写什么 |
|---|---|
| 职责 | 该业务域负责什么 |
| 包位置 | Controller、Service、Domain 所在的包路径 |
| 关键入口 | HTTP 路径、消息主题、定时任务、外部回调 |
| 依赖域 | 依赖的其他业务域或外部服务 |
| 域级约定 | 该域内的红线（如状态变更必须通过 StateMachine） |
| 详细业务规则 | 指向 `docs/domains/订单域.md` 或 `docs/modules/订单域.md` |

**示例**：

```markdown
# 域：订单域

## 职责
负责订单生命周期管理：创建、支付、发货、完成、取消。

## 包位置
- Controller: `com.example.controller.order`
- Service: `com.example.service.order`
- Domain: `com.example.domain.order`

## 关键入口
- HTTP: /api/v1/orders、/api/v1/orders/{id}/pay
- 消息: order.created、order.paid
- 定时任务: OrderTimeoutJob

## 依赖域
- 用户域：查询用户地址、账户状态
- 库存域：预占库存、释放库存
- 支付域：发起支付、接收回调

## 域级约定
- 订单状态变更必须通过 OrderStateMachine；
- 订单域不能直接操作库存表，必须通过库存域接口；
- 订单超时逻辑统一由 OrderTimeoutJob 触发，禁止在 Controller 中写超时判断。

## 详细业务规则
见 `docs/domains/订单域.md`。
```

---

## 4. CLAUDE.md 写什么、不写什么

### 4.1 写入 CLAUDE.md 的内容

判断标准：**长期稳定 + 对 AI 行为有直接约束**。

| 类型 | 示例 |
|---|---|
| 技术栈 | Spring Boot 3.2、JDK 17、MySQL + MyBatis-Plus |
| 分层与包结构 | `com.example.domain` 放实体，`com.example.interfaces` 放 Controller |
| 核心约定 | 禁止跨层调用、禁止手写 SQL、所有接口返回统一响应体 |
| 测试策略 | 单元测试用 JUnit 5 + Mockito，集成测试用 Testcontainers |
| 安全/性能红线 | 禁止在循环中调用外部接口、所有支付操作必须记录审计日志 |
| 文档指针 | 订单状态机定义见 `docs/domains/订单域.md` |
| 禁用清单 | 禁止用 `java.util.Date`、禁止在领域层用 Spring 注解 |
| 未知区域 | 部分历史模块分层不清晰，AI 修改时需谨慎 |

### 4.2 不写入 CLAUDE.md 的内容

判断标准：**具体业务规则 + 频繁变化 + 详细实现细节**。

| 类型 | 示例 | 应放哪里 |
|---|---|---|
| 具体业务规则 | 订单超时 30 分钟自动取消 | `docs/domains/订单域.md` |
| 状态机详细定义 | 待支付 → 已支付 → 已发货 → 已完成 | `docs/domains/订单域.md` |
| 接口字段列表 | `/api/v1/orders` 的 request/response 字段 | `docs/entry-points.md` |
| 数据库字段含义 | `orders.status` 每个取值含义 | `docs/glossary.md` |
| 具体实现细节 | `OrderService.createOrder` 先校验库存再创建订单 | `docs/modules/order.md` |
| 需求变更历史 | 为什么把超时时间从 30 分钟改为 60 分钟 | `docs/adr/XXX.md` 或 PRD |

---

## 5. CLAUDE.md 与过程梳理文档的关系

```
CLAUDE.md          → 上下文配置文件（Constraint + Pointer）
      ↓ 指向
docs/domains/     → 业务知识文档（Knowledge）
docs/modules/
docs/glossary.md
docs/entry-points.md
docs/adr/
```

**类比**：

- `CLAUDE.md` 像是餐厅的《员工手册》：告诉服务员怎么接待客人、什么不能说、制服要求；
- 过程梳理文档像是《菜单和食材说明》：告诉服务员每道菜怎么做、有什么忌口、原料来源。

**规则**：

- `CLAUDE.md` 中只保留对 AI 行为有直接约束的信息；
- 具体业务规则、流程、接口、数据模型写在过程梳理文档中；
- `CLAUDE.md` 通过**指针**引用过程梳理文档，不复制内容；
- 如果某条业务规则足够稳定且影响 AI 行为，可以在 `CLAUDE.md` 中保留**高度概括**的一句话，并指向详细文档。

**正确示例**：

```markdown
## 核心约定
- 订单状态变更必须通过 OrderStateMachine；
- 详细状态机定义见 `docs/domains/订单域.md`。
```

**错误示例**：

```markdown
## 核心约定
- 订单创建后 30 分钟未支付自动取消；
- 取消后发送短信通知用户，短信模板为 TPL_001；
- 订单状态流转：待支付 → 已支付 → 已发货 → 已完成；
- 已支付订单在 24 小时内未发货自动触发退款流程。
```

（这些具体规则应该放在过程梳理文档中。）

---

## 6. 初始化流程

### 6.1 新项目

1. 创建项目根 `CLAUDE.md`；
2. 根据项目类型决定是否需要模块级/域级 `CLAUDE.md`：
   - 多模块项目 → 每个核心模块根目录一个 `CLAUDE.md`；
   - 单模块多业务域 → 在 `docs/domains/` 下按业务域创建；
   - 小项目 → 可以只保留根 `CLAUDE.md` + 文档指针。
3. 创建 `docs/ai-skills/`、`docs/glossary.md`、`docs/entry-points.md`；
4. 配置 AI 工具读取 `CLAUDE.md`。

### 6.2 老项目

1. 构建项目，确保能编译通过；
2. 生成依赖树，分析技术栈；
3. 用 AI 生成根 `CLAUDE.md` 初稿；
4. 人工 review 并修正；
5. 在逆向理解过程中逐步补充模块级/域级 `CLAUDE.md`；
6. 把不确定性标记为“未知区域”，不要写入未确认内容。

---

## 7. 更新与演化

### 7.1 何时更新

- 技术栈升级（如 Spring Boot 版本变更）；
- 新增核心约定或红线；
- 新增业务域或模块；
- 发现 AI 经常犯某类错误，需要补充约束；
- 文档指针需要更新（如新增了 `docs/domains/库存域.md`）。

### 7.2 何时不更新

- 具体业务规则变更（应更新过程梳理文档，而非 `CLAUDE.md`）；
- 临时性需求（应放在本次会话或 PRD 中）；
- 某一次性的实现细节。

### 7.3 更新流程

1. 打开对应层级的 `CLAUDE.md`；
2. 只修改相关章节，避免大改；
3. 检查行数是否仍然符合约束：
   - 根 `CLAUDE.md` ≤ 200 行；
   - 模块级/域级 `CLAUDE.md` ≤ 150 行；
4. 如果超出，把内容移到过程梳理文档，保留指针；
5. 在 `docs/claude-md-changelog.md` 中记录变更原因。

```bash
wc -l CLAUDE.md
wc -l {模块}/CLAUDE.md
wc -l docs/domains/{域}.md
```

### 7.4 文档腐化检测

每月检查：

- `CLAUDE.md` 中引用的文档是否仍然存在；
- `CLAUDE.md` 中的技术栈是否仍然准确；
- 行数是否超标。

可使用 `scripts/check_claude_md_refs.py` 自动检查引用有效性。

---

## 8. 在不同 AI 工具中的使用

### 8.1 Claude Code

Claude Code 会自动读取项目根目录的 `CLAUDE.md`。

**模块级/域级加载**：

- 在 `.claude/commands/` 中创建 skill，显式提示 AI 读取对应模块/域的 `CLAUDE.md`：

```markdown
# .claude/commands/grill-light.md

执行以下步骤：
1. 读取项目根 `CLAUDE.md`；
2. 如果需求涉及某个业务域，读取 `docs/domains/{域}.md`；
3. 根据 PRD 向我提出澄清问题。
```

**推荐**：把核心 prompt 放在 `docs/ai-skills/`，`.claude/commands/` 只作为轻量包装引用它们。

### 8.2 Cursor

Cursor 使用 `.cursorrules` 文件作为项目级上下文。

**配置方式**：

1. 在项目根创建 `.cursorrules`；
2. 在 `.cursorrules` 中引用 `CLAUDE.md` 和 `docs/ai-skills/`：

```markdown
# 项目约定
请优先遵守项目根目录 `CLAUDE.md` 中的约定。

# 需求澄清
当需要澄清需求时，参考 `docs/ai-skills/grill-light.md`。

# 代码审查
当审查代码时，参考 `docs/ai-skills/codex-review.md`。
```

> 注意：Cursor 的 `.cursorrules` 不会自动读取 `CLAUDE.md` 内容，需要显式引用或复制关键约束。

### 8.3 GitHub Copilot / 通义灵码 / CodeGeeX

这些工具通常不自动读取项目文件，需要：

1. 在编辑器中打开 `CLAUDE.md`；
2. 或把关键约束整理成 snippets / 自定义提示词；
3. 在开始对话时，把 `CLAUDE.md` 的核心内容粘贴到 prompt 中。

### 8.4 通用做法

无论使用哪种工具，都建议：

1. 把 `CLAUDE.md` 作为项目级上下文文件；
2. 把 `docs/ai-skills/` 作为 prompt 库；
3. 在进入具体模块/域时，显式加载对应的模块级/域级 `CLAUDE.md`；
4. 不要把所有信息都塞进一个 prompt，而是分层加载。

---

## 9. 模板速查

### 9.1 根 CLAUDE.md 模板

```markdown
# 项目名

## 项目类型
单体 / 多模块 / 微服务

## 技术栈
- Spring Boot {x.y.z}
- JDK {xx}
- Maven / Gradle
- 数据库：{MySQL / PostgreSQL}
- ORM：{MyBatis-Plus / JPA}
- 缓存：{Redis / Caffeine}
- 消息队列：{Kafka / RabbitMQ}
- 安全：{Spring Security / Sa-Token}

## 分层与包结构
```
com.example
  ├── application      # 应用服务
  ├── domain           # 领域层
  ├── infrastructure   # 基础设施
  ├── interfaces       # 接口层
  └── common           # 通用工具
```

## 核心约定
1. 不允许跨层调用；
2. 不允许在 Service 中直接写 SQL；
3. 所有 Controller 必须返回统一响应体；
4. 涉及分布式事务必须使用 Saga / 事务消息。

## 测试策略
- 单元测试：JUnit 5 + Mockito；
- 集成测试：@SpringBootTest + Testcontainers；
- 接口测试：MockMvc；
- 所有 bug 修复必须附带回归测试。

## 文档指针
- 模块/域文档：`docs/modules/` 或 `docs/domains/`
- 术语表：`docs/glossary.md`
- 入口地图：`docs/entry-points.md`
- PRD：`docs/prd/`
- ADR：`docs/adr/`
- AI skill：`docs/ai-skills/`

## 禁用清单
- 禁止使用 `java.util.Date`；
- 禁止在领域层引入 Spring 注解；
- 禁止手动拼接 SQL 字符串；
- 禁止在循环中调用外部 HTTP 接口。

## 未知区域
- 待补充。
```

### 9.2 模块级 CLAUDE.md 模板

```markdown
# 模块：{模块名}

## 职责
一句话说明该模块负责什么。

## 依赖
- 依赖模块：
- 外部服务：
- 数据库：

## 关键入口
- HTTP：
- 消息：
- 定时任务：

## 领域实体
-

## 模块级约定
-

## 详细业务规则
见 `docs/modules/{模块名}.md`。
```

### 9.3 业务域级 CLAUDE.md 模板

```markdown
# 域：{域名称}

## 职责
一句话说明该业务域负责什么。

## 包位置
- Controller:
- Service:
- Domain:

## 关键入口
- HTTP:
- 消息:
- 定时任务:

## 依赖域
-

## 域级约定
-

## 详细业务规则
见 `docs/domains/{域名称}.md`。
```

---

## 10. 常见错误

### 错误 1：把 CLAUDE.md 写成项目百科全书

**表现**：根 `CLAUDE.md` 超过 500 行，包含每个接口的字段、每个状态机的细节。

**后果**：AI 上下文过载，抓不住重点；业务规则一变，根文档也要改。

**修正**：只保留约束和指针，细节移到 `docs/`。

### 错误 2：业务规则直接写进 CLAUDE.md

**表现**：`CLAUDE.md` 里写“订单超时 30 分钟自动取消”。

**后果**：需求一变就要改 `CLAUDE.md`，违反“长期稳定”原则。

**修正**：在 `CLAUDE.md` 中写“订单超时逻辑统一由 OrderTimeoutJob 触发，详细规则见 `docs/domains/订单域.md`”。

### 错误 3：为每个 Controller 创建 CLAUDE.md

**表现**：`docs/claude/OrderController.md`、`docs/claude/UserController.md` 等。

**后果**：文件过多，维护成本高，AI 不知道该读哪个。

**修正**：按业务域聚合，一个业务域一份域级 `CLAUDE.md`。

### 错误 4：CLAUDE.md 与代码不一致

**表现**：`CLAUDE.md` 说禁止跨层调用，但代码里大量跨层调用；AI 据此生成的代码与现有代码风格冲突。

**后果**：AI 输出与项目实际脱节，人工审查成本增加。

**修正**：要么先重构代码，要么在 `CLAUDE.md` 中标注“历史代码存在跨层调用，新代码必须遵循本约定”。

### 错误 5：从不更新 CLAUDE.md

**表现**：项目技术栈升级了，但 `CLAUDE.md` 还是旧的；新增业务域后，没有对应的域级 `CLAUDE.md`。

**后果**：AI 基于过期上下文生成代码，质量下降。

**修正**：在持续演化阶段定期 review 和更新 `CLAUDE.md`。

---

## 11. 最佳实践

1. **保持精简**：根 `CLAUDE.md` < 200 行，模块级/域级 < 150 行。
2. **指针优先**：用文档指针代替复制内容。
3. **分层加载**：全局约束用根 `CLAUDE.md`，局部约束用模块级/域级 `CLAUDE.md`，业务细节查过程文档。
4. **约束明确**：用“必须/禁止/只能”等强约束词，少用“建议/可以”。
5. **示例具体**：包结构、命名约定给出真实示例，不要只说“按分层架构”。
6. **标记未知**：没搞清楚的内容明确标注为“未知区域”，不要让 AI 猜测。
7. **定期 review**：每月检查 `CLAUDE.md` 是否过期、行数是否超标、引用是否有效。
8. **版本控制**：`CLAUDE.md` 必须纳入 Git 管理，每次更新记录变更原因。

---

## 12. 检查清单

### 初始化时

- [ ] 根 `CLAUDE.md` 已创建，且 ≤ 200 行；
- [ ] 多模块项目已为每个核心模块创建模块级 `CLAUDE.md`；
- [ ] 单模块多业务域项目已按业务域创建域级 `CLAUDE.md`（`docs/domains/` 或 `docs/modules/`）；
- [ ] `CLAUDE.md` 中只包含约束和指针，没有具体业务规则；
- [ ] 文档指针指向的文档已存在；
- [ ] AI 工具已配置读取 `CLAUDE.md` 和 `docs/ai-skills/`。

### 更新时

- [ ] 只修改相关章节，避免大改；
- [ ] 更新后检查行数是否仍然符合约束；
- [ ] 超出的内容已移到过程梳理文档并保留指针；
- [ ] 已在 `docs/claude-md-changelog.md` 中记录变更原因；
- [ ] 引用的过程文档路径仍然有效。

### 每月 review 时

- [ ] `CLAUDE.md` 中引用的文档仍然存在；
- [ ] 技术栈信息仍然准确；
- [ ] 行数未超标；
- [ ] 新增业务域/模块已补充对应 `CLAUDE.md`；
- [ ] AI 频繁犯错的地方是否需要在 `CLAUDE.md` 中增加约束。

---

## 13. 相关文件

- `AI_开发工作流_流程性_SOP.md` —— 工作流总览
- `AI_工作流SOP_阶段1_项目初始化_操作手册.md` —— 初始化阶段详细操作
- `AI_工作流SOP_阶段3_共识确认_操作手册.md` —— 如何更新 CLAUDE.md
- `AI_工作流SOP_阶段5_持续演化_操作手册.md` —— 文档腐化检测与 skill 迭代

---

*版本：V1.0*  
*更新日期：2026-06-19*
