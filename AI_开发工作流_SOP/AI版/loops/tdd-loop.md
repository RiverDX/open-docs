# tdd-loop —— 测试驱动开发（AI 执行版）

> **何时启动**：用户要"写测试 / TDD / 补单测 / 写 unit test"。  
> **禁止**：恒真断言；只写 happy path；mock 被测类本身；为覆盖率堆砌无意义测试。

---

## 输入清单（缺即停）

| 项 | 必需 | 缺失时动作 |
|---|---|---|
| PRD / 需求描述 | 必需 | 反问 |
| 验收标准 AC 列表 | 必需 | 反问"PRD 中的 AC 是什么" |
| 被测类代码 | 必需 | Read 或要路径 |
| 依赖接口代码 | 必需 | Read 或要路径 |
| 根 CLAUDE.md | 必需 | 缺时标"无约束"，按 JUnit 5 + Mockito 通用最佳实践 |
| 现有测试样例 | 建议 | 缺时按通用风格 |

---

## 流程（6 步，禁止跳步）

1. **读 AC**：列出 PRD 中每条 AC，编号 AC-1, AC-2, ...
2. **建矩阵**：按 TC1–TC6 维度，每条 AC 至少对应 1 个测试用例
3. **写测试**：按矩阵生成完整 JUnit 5 + Mockito 代码，每个 @Test 含 // Arrange // Act // Assert 注释
4. **自查**：按 PASS 条件 TC1–TC6 填自查表
5. **补缺**：仅对 ⚠️/❌ 维度补测试（最多 1 轮）
6. **终输出**：4 段（矩阵 + 测试代码 + 自查表 + 待确认清单）

---

## PASS 条件（自查标准，严格解释）

### TC1 happy path（每条 AC ≥ 1 测试）
- ✅ PRD 每条 AC 都至少对应 1 个测试方法
- ⚠️ 缺 1 条 AC 的覆盖
- ❌ 缺 ≥ 2 条 AC 的覆盖

### TC2 异常路径
- ✅ 被测代码中每个 try/catch / throw / Optional.orElseThrow 至少 1 条测试
- ⚠️ 漏 1 处
- ❌ 漏 ≥ 2 处

### TC3 边界条件
- ✅ 含全部：null 入参测试 + 空集合 / 空字符串测试 + 边界数值测试
- ⚠️ 含 2 类
- ❌ 含 ≤ 1 类

### TC4 并发与幂等
- ✅ 若被测代码涉及共享状态 / 外部回调 → 至少 1 条并发或重复请求测试；若不涉及，本项自动 ✅
- ⚠️ 应有但缺
- ❌ 涉及但完全无测试

### TC5 事务与失败
- ✅ 若被测代码有多步写入 → 至少 1 条"中途失败 + 期望回滚"测试；不涉及自动 ✅
- ⚠️ 应有但 mock 不到位（如未真实抛异常）
- ❌ 涉及但完全无测试

### TC6 断言可证伪
- ✅ 全部断言都是 具体值比较（assertEquals/assertThat with hamcrest）或 verify(mock, times(N))
- ⚠️ 出现 ≤ 2 处 assertNotNull(result) / assertTrue(条件不严格)
- ❌ 出现 ≥ 3 处恒真断言，或捕获异常无后续断言

---

## 输出格式（严格遵循）

```markdown
## 一、测试矩阵
| TC | 维度 | 用例描述 | 对应 AC | 测试方法名 |
|---|---|---|---|---|
| TC1 | happy | {场景} | AC-1 | should_xxx_when_yyy |
| TC2 | 异常 | {场景} | - | should_throw_when_xxx |
| TC3 | 边界 | null 入参 | - | should_returnError_when_userIdIsNull |
| TC4 | 并发 | {场景} | AC-? | should_beIdempotent_when_concurrentXxx |
| TC5 | 事务 | {场景} | AC-? | should_rollback_when_xxxFails |

## 二、测试代码

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock private InventoryClient inventoryClient;
    @InjectMocks private OrderService orderService;

    @Test
    void should_cancelOrder_when_timeoutAndUnpaid() {
        // Arrange
        Order order = new Order(1L, OrderStatus.UNPAID, LocalDateTime.now().minusMinutes(31));
        when(inventoryClient.release(any())).thenReturn(true);

        // Act
        orderService.cancelTimeoutOrder(order);

        // Assert
        assertThat(order.getStatus()).isEqualTo(OrderStatus.CANCELLED);
        verify(inventoryClient, times(1)).release(eq(1L));
    }

    // ... 其他测试
}
```

## 三、自查表
| TC | 评分 | 证据（测试方法名） |
|---|---|---|
| TC1 happy | ✅/⚠️/❌ | should_cancelOrder_when_timeoutAndUnpaid, ... |
| TC2 异常 | ✅/⚠️/❌ | ... |
| TC3 边界 | ✅/⚠️/❌ | ... |
| TC4 并发 | ✅/⚠️/❌ | ... |
| TC5 事务 | ✅/⚠️/❌ | ... |
| TC6 可证伪 | ✅/⚠️/❌ | 全部用 assertThat/verify，无 assertNotNull(result) |

## 四、需人工确认清单
- [ ] {场景} 用 Mock 模拟并发，建议跑一次 Testcontainers 真实 DB 集成测试
- [ ] {依赖} 当前 mock 行为是否反映真实
- [ ] [待验证] ...

## 五、迭代信息
- 轮次：{1 / 2}
- 是否达到停止条件：{是 / 否（原因）}
```

---

## 禁用写法（出现即扣分，对应 TC6）

| 禁用 | 替换 |
|---|---|
| `assertNotNull(result);` | `assertThat(result.getStatus()).isEqualTo(...)` |
| `assertTrue(true);` | 删除或改成具体断言 |
| `assertTrue(result.getList().size() > 0);` | `assertThat(result.getList()).hasSize(N).contains(...)` |
| `try { method(); } catch (Exception e) {}` | `assertThatThrownBy(() -> method()).isInstanceOf(...)` |
| `verify(mock);` 无 times 限定 | `verify(mock, times(N)).method(eq(...))` |
| `@SpringBootTest` 用于纯单元测试 | `@ExtendWith(MockitoExtension.class)` |
| `Mockito.mock(被测类.class)` | 只 mock 直接依赖，禁 mock 被测类 |

---

## 测试命名规范（强制）

格式：`should_<期望结果>_when_<触发条件>`

示例：
- ✅ `should_cancelOrder_when_timeoutAndUnpaid`
- ✅ `should_throwNotFound_when_orderIdInvalid`
- ✅ `should_releaseInventory_when_orderCancelledSuccessfully`
- ❌ `test1()`, `testOrder()`, `cancelTest()`

---

## 完成后

```bash
python ../check-output.py tdd-loop {输出文件路径}
```

不通过 → 回流程第 4 步重新自查。
