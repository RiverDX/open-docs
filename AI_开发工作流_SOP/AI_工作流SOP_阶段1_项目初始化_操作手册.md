# 阶段 1：项目初始化 —— 操作手册

> **目标**：为 Java / SpringBoot 项目建立可复用的 AI 上下文，让后续所有 AI 会话都能基于统一、准确、稳定的项目约定进行。  
> **前提**：你已经拿到项目源码仓库，或准备启动一个新项目。  
> **预计耗时**：新项目约 2–4 小时；老项目约 4–8 小时（取决于复杂度）。

---

## 1. 所需工具

| 工具 | 用途 | 是否必需 |
|---|---|---|
| **Git** | 版本控制、查看历史提交与分支 | 是 |
| **IntelliJ IDEA** | 阅读代码、运行测试、查看依赖图 | 强烈建议 |
| **Maven / Gradle** | 构建项目、生成依赖树 | 是 |
| **AI 工具**（Claude Code / Cursor / Copilot / 通义灵码等） | 生成 CLAUDE.md、分析技术栈、生成 skill prompt | 是 |
| **终端 / 命令行** | 运行命令、创建目录、操作 Git | 是 |
| **Markdown 编辑器**（Obsidian / VS Code） | 编写和查看 `docs/` 文档 | 是 |
| **JavaParser（可选）** | 批量解析代码结构，自动生成入口地图 | 可选 |

---

## 2. 环境准备

### 2.1 确认本地环境

```bash
# 检查 Java 版本
java -version

# 检查 Maven / Gradle
mvn -v
# 或
gradle -v

# 检查 Git
git --version

# 检查 AI 工具（以 Claude Code 为例）
claude --version
```

### 2.2 克隆/打开项目

```bash
# 老项目
git clone <仓库地址>
cd <项目名>

# 新项目
mkdir <项目名>
cd <项目名>
git init
```

### 2.3 构建项目

```bash
# Maven
mvn clean compile -DskipTests

# Gradle
gradle clean compileJava
```

如果构建失败，先解决环境问题，再继续后续步骤。否则 AI 分析会基于不完整的信息。

---

## 3. 操作步骤

### 步骤 1：收集项目基础信息

打开 `pom.xml` 或 `build.gradle`，记录以下内容：

| 信息项 | 示例值 | 记录位置 |
|---|---|---|
| 项目类型 | 单体 / 多模块 / 微服务 | 临时笔记 |
| Spring Boot 版本 | 3.2.0 | 临时笔记 |
| JDK 版本 | 17 | 临时笔记 |
| 构建工具 | Maven / Gradle | 临时笔记 |
| 数据库 | MySQL 8.0 / PostgreSQL 15 | 临时笔记 |
| ORM | MyBatis-Plus / JPA | 临时笔记 |
| 缓存 | Redis / Caffeine | 临时笔记 |
| 消息队列 | Kafka / RabbitMQ / 无 | 临时笔记 |
| 主要中间件 | Nacos / Sentinel / OpenFeign | 临时笔记 |
| 安全框架 | Spring Security / Sa-Token | 临时笔记 |
| 测试框架 | JUnit 5 + Mockito / Testcontainers | 临时笔记 |
| 包结构约定 | `com.example.{模块}.domain` | 临时笔记 |
| 团队红线 | 不允许手写 SQL / 不允许跨层调用 | 临时笔记 |

同时查看 `README.md`、`docs/`、`src/main/resources/application.yml` 等文件，补充信息。

---

### 步骤 2：生成依赖树

```bash
# Maven
mvn dependency:tree > dependency-tree.txt

# Gradle
gradle dependencies > dependency-tree.txt
```

这个文件用于帮助 AI 快速理解项目技术栈。

---

### 步骤 3：生成项目根 `CLAUDE.md`

在项目根目录创建 `CLAUDE.md`。

使用以下 prompt 向 AI 请求生成初稿（可复用，粘贴到任何 AI 工具）：

```markdown
# 角色
你是一名熟悉 Java / SpringBoot 的资深技术写手。请根据以下项目信息，生成一份简洁的 `CLAUDE.md` 初稿。

# 约束
- 总行数不超过 200 行；
- 只包含全局性、长期稳定的约定；
- 不展开具体业务规则，只保留指针；
- 输出为 Markdown 格式，适合放在项目根目录；
- 使用中文输出。

# 项目信息
- 项目类型：{单体 / 多模块 / 微服务}
- Spring Boot 版本：{x.y.z}
- JDK 版本：{xx}
- 构建工具：Maven / Gradle
- 数据库与 ORM：{MySQL + MyBatis-Plus / PostgreSQL + JPA}
- 缓存：{Redis / Caffeine / 无}
- 消息队列：{Kafka / RabbitMQ / 无}
- 服务发现/配置：{Nacos / Consul / 无}
- 安全框架：{Spring Security / Sa-Token / 无}
- 包结构约定：{com.example.xxx}
- 测试框架：{JUnit 5 + Mockito + Testcontainers}
- 代码审查红线：{不允许跨层调用 / 不允许手写 SQL / 所有接口必须写测试}

# 输出格式
---
# 项目概览
## 技术栈
## 分层与包结构
## 核心约定（不可违反）
## 测试策略
## 文档与上下文指针
## 禁用清单
## 未知区域（待补）
---
```

**生成后人工审查要点**：
- 是否包含过时的技术栈？
- 是否把业务细节错误地写入了全局约定？
- 是否超过 200 行？如果超过，删除具体业务描述，改为指针。

---

### 步骤 4：创建目录结构

```bash
mkdir -p docs/ai-skills
mkdir -p docs/modules
mkdir -p docs/prd
mkdir -p docs/adr
mkdir -p docs/reports
mkdir -p scripts
```

目录说明：

| 目录 | 用途 |
|---|---|
| `docs/ai-skills/` | 工具无关的 AI skill prompt 模板 |
| `docs/modules/` | 每个模块的逆向理解文档 |
| `docs/prd/` | 每个功能/需求的 PRD 文档 |
| `docs/adr/` | 架构决策记录 |
| `docs/reports/` | 文档腐化检测报告等 |
| `scripts/` | 自动化检查脚本 |

---

### 步骤 5：创建分层 `CLAUDE.md`

`CLAUDE.md` 采用分层结构：

1. **根 `CLAUDE.md`**：全局技术栈、分层约定、核心红线、文档指针；
2. **物理模块级 `CLAUDE.md`**：多模块项目时，每个 Maven/Gradle 模块一个；
3. **业务域级 `CLAUDE.md`**：单模块多业务域项目时，每个业务域一个；
4. **过程梳理文档**：`docs/modules/`、`docs/domains/` 中的详细业务知识文档。

> **核心原则**：`CLAUDE.md` 只放对 AI 行为有**直接约束**且**长期稳定**的信息；具体业务规则、流程细节、接口列表放在过程梳理文档中，`CLAUDE.md` 只保留指针。

---

#### 场景 A：多模块项目

在每个 Maven/Gradle 模块根目录下创建 `CLAUDE.md`。

```bash
# 多模块 Maven 项目示例
touch auth/CLAUDE.md
touch order/CLAUDE.md
touch payment/CLAUDE.md
```

物理模块级 `CLAUDE.md` 内容示例：

```markdown
---
# 模块：{模块名}

## 职责
一句话说明该模块负责什么。

## 依赖
- 依赖模块：[[order]]、[[payment]]
- 外部服务：用户中心、支付网关
- 数据库：db_order

## 关键入口
- HTTP：/api/v1/orders、/api/v1/orders/{id}/pay
- 消息：order.created、order.paid
- 定时任务：OrderTimeoutJob

## 领域实体
- Order、OrderItem、PaymentRecord

## 模块级约定
- 本模块所有 Service 必须通过 OrderRepository 操作数据库；
- 不允许直接调用 payment 模块的数据库表；
- 订单状态变更必须通过 OrderStateMachine 进行。

## 详细业务规则
见 `docs/modules/{模块名}.md`。
```

---

#### 场景 B：单模块多业务域（按 Controller 划分业务）

如果只有一个 Maven/Gradle 模块，但内部按 Controller/Service 划分为多个业务域（如订单域、用户域、库存域），**不要为每个 Controller 创建 `CLAUDE.md`**，而是按业务域创建域级 `CLAUDE.md`。

**推荐位置**：`docs/domains/`

```bash
mkdir -p docs/domains
touch docs/domains/订单域.md
touch docs/domains/用户域.md
touch docs/domains/库存域.md
```

域级 `CLAUDE.md` 内容示例：

```markdown
---
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
- 订单状态变更必须通过 OrderStateMachine 进行；
- 订单域不能直接操作库存表，必须通过库存域接口；
- 订单超时逻辑统一由 OrderTimeoutJob 触发，禁止在 Controller 中写超时判断。

## 详细业务规则
见 `docs/domains/订单域.md` 或 `docs/modules/订单域.md`。
```

> **选择建议**：如果未来可能拆分为独立模块或微服务，优先用 `docs/domains/`，拆分时可直接升级为物理模块；如果长期保持单模块，用 `docs/modules/` 也可以，但要在根 `CLAUDE.md` 中明确说明这是“逻辑域”而非物理模块。

---

#### 场景 C：小到中型单模块项目

如果项目规模小、业务域清晰且稳定，可以只在根 `CLAUDE.md` 中保留 `docs/domains/` 或 `docs/modules/` 的指针，不单独创建域级 `CLAUDE.md`。当某个业务域足够复杂（超过 3 个 Controller 或涉及复杂状态机）时，再拆分出域级 `CLAUDE.md`。

---
---

### 步骤 6：创建工具无关的 AI skill 目录

在 `docs/ai-skills/` 下创建至少以下 skill 文件：

```bash
touch docs/ai-skills/grill-light.md
touch docs/ai-skills/grill-deep.md
touch docs/ai-skills/to-prd.md
touch docs/ai-skills/to-issues.md
touch docs/ai-skills/tdd.md
touch docs/ai-skills/codex-review.md
touch docs/ai-skills/reverse-mapping.md
touch docs/ai-skills/wt-new.md
```

每个 skill 文件结构如下（以 `grill-light.md` 为例）：

```markdown
---
type: ai-skill
skill: grill-light
---

# grill-light

## 目标
在功能开发前快速澄清需求，识别边界条件和隐藏约束。

## 触发条件
- 拿到一个 PRD 或需求描述后；
- 准备进入 `/to-prd` 或 `/to-issues` 前。

## 输入
- PRD / 需求描述
- 根 CLAUDE.md
- 模块级 CLAUDE.md（如适用）

## 输出
- 5–10 个澄清问题
- 边界条件清单
- 风险点提示

## 通用 prompt
```markdown
# 角色
你是一名需求分析师。请根据以下 PRD 和项目约定，向我提出 5–10 个关键问题，以澄清需求。

# 约束
- 每个问题必须具体、可回答；
- 优先关注边界条件、异常场景、权限、性能、并发；
- 不要问已经明确写在 PRD 中的内容。

# 输入
PRD：{粘贴}
CLAUDE.md：{粘贴}

# 输出
按优先级列出问题，并说明每个问题为什么重要。
```

## Claude Code 适配
创建 `.claude/commands/grill-light.md`，内容同“通用 prompt”。

## Cursor 适配
在 `.cursorrules` 中加入该 skill 的摘要，或作为自定义指令保存。

## 注意事项
- 不要问“是否需要测试”这种笼统问题；
- 如果需求涉及多个模块，应分模块提问。
```

---

### 步骤 7：创建入口地图和术语表

#### `docs/entry-points.md`

```markdown
# 入口地图

## HTTP 接口
| 路径 | 方法 | 模块 | 说明 |
|---|---|---|---|
| /api/v1/orders | POST | order | 创建订单 |
| /api/v1/orders/{id}/pay | POST | order | 支付订单 |

## 消息消费者
| 主题 | 消费者 | 模块 | 说明 |
|---|---|---|---|
| order.created | OrderCreatedListener | payment | 收到订单创建消息后初始化支付单 |

## 定时任务
| 任务类 | 模块 | 触发频率 | 说明 |
|---|---|---|---|
| OrderTimeoutJob | order | 每 5 分钟 | 扫描超时订单 |

## 外部回调
| 来源 | 入口 | 模块 | 说明 |
|---|---|---|---|
| 支付网关 | /webhook/payment | payment | 支付结果通知 |
```

#### `docs/glossary.md`

```markdown
# 术语表

| 术语 | 英文 | 含义 | 相关模块 |
|---|---|---|---|
| 订单 | Order | 用户购买商品的请求 | order |
| 支付单 | PaymentRecord | 对应一次支付尝试的记录 | payment |
| 订单状态 | OrderStatus | 待支付 / 已支付 / 已发货 / 已完成 / 已取消 | order |
```

---

### 步骤 8：配置 AI 工具指向统一目录

#### 如果使用 Claude Code

```bash
# 创建 .claude/commands 软链接到 docs/ai-skills
# 或直接在 .claude/commands 中引用 docs/ai-skills 中的文件
ln -s docs/ai-skills .claude/commands
```

更推荐：把 `.claude/commands/` 中的文件作为轻量包装，实际 prompt 内容放在 `docs/ai-skills/`，方便其他工具复用。

```markdown
# .claude/commands/grill-light.md
参考并执行 `docs/ai-skills/grill-light.md` 中的通用 prompt。
```

#### 如果使用 Cursor

在 `.cursorrules` 中加入：

```markdown
当进行需求澄清时，参考 `docs/ai-skills/grill-light.md` 中的流程和 prompt。
当进行代码审查时，参考 `docs/ai-skills/codex-review.md`。
```

#### 其他工具

把 `docs/ai-skills/` 作为 prompt 库，复制通用 prompt 到对应工具的自定义指令中。

---

## 4. 检查清单

- [ ] 项目已成功构建；
- [ ] 已生成 `dependency-tree.txt` 或类似依赖清单；
- [ ] 项目根 `CLAUDE.md` 已创建，且 ≤ 200 行；
- [ ] `docs/ai-skills/` 已创建至少 6 个 skill 文件；
- [ ] `docs/modules/` 目录已创建；
- [ ] `docs/entry-points.md` 已创建并包含关键接口/入口；
- [ ] `docs/glossary.md` 已创建并包含关键术语；
- [ ] 多模块项目已为每个核心 Maven/Gradle 模块创建模块级 `CLAUDE.md`；
- [ ] 单模块多业务域项目已按业务域创建域级 `CLAUDE.md`（`docs/domains/` 或 `docs/modules/`）；
- [ ] AI 工具已配置指向统一的 `docs/ai-skills/` 目录。

---

## 5. 常见问题

### Q1：200 行根本写不完项目约定怎么办？

**答**：只写全局、长期稳定的约定。具体业务规则、模块细节、接口文档分别放到 `docs/modules/`、`docs/prd/`、`docs/api/` 中。`CLAUDE.md` 只保留指针。

### Q2：项目完全没有文档，怎么初始化？

**答**：先通过依赖树和目录结构让 AI 生成一份“初稿”，然后人工修正。把不确定性标记为“待验证”。后续在逆向理解阶段补充。

### Q3：AI 生成的 CLAUDE.md 质量不高怎么办？

**答**：分两轮生成。第一轮让 AI 只列出应该包含哪些条目；第二轮让 AI 基于你的反馈逐条生成。避免一次性让 AI 写完整文档。

---

## 6. 模板速查

### 根 `CLAUDE.md` 模板

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
  ├── application      # 应用服务，编排领域对象
  ├── domain           # 领域层：实体、值对象、领域服务
  ├── infrastructure   # 基础设施：Repository 实现、外部客户端
  ├── interfaces       # 接口层：Controller、Listener、Job
  └── common           # 通用工具
```

## 核心约定
1. 不允许跨层调用；
2. 不允许在 Service 中直接写 SQL；
3. 所有 Controller 必须返回统一响应体；
4. 所有接口变更必须同步更新测试和接口文档；
5. 涉及分布式事务必须使用 Saga / 事务消息。

## 测试策略
- 单元测试：JUnit 5 + Mockito，覆盖 Service 核心逻辑；
- 集成测试：@SpringBootTest + Testcontainers，覆盖数据库/缓存；
- 接口测试：MockMvc 或 HTTP 测试，覆盖 Controller；
- 所有 bug 修复必须附带回归测试。

## 文档指针
- 模块文档：`docs/modules/`
- 术语表：`docs/glossary.md`
- 入口地图：`docs/entry-points.md`
- PRD：`docs/prd/`
- ADR：`docs/adr/`
- AI skill：`docs/ai-skills/`

## 禁用清单
- 禁止使用 `java.util.Date`，统一使用 `java.time`；
- 禁止在领域层引入 Spring 注解；
- 禁止手动拼接 SQL 字符串；
- 禁止在循环中调用外部 HTTP 接口。

## 未知区域
- 微服务间的熔断降级策略待补充；
- 部分历史模块的分层不清晰，待重构。
```

---

*上一阶段：无（本阶段为起点）*  
*下一阶段：[阶段 2：逆向理解](./AI_工作流SOP_阶段2_逆向理解_操作手册.md)*
