/**
 * Task 测试
 *
 * TDD 示例：
 * - 通过公开接口测试，不测试私有方法
 * - 测试读起来像规格说明
 * - 覆盖正常路径 + 边界条件 + 异常场景
 */

const {
  createTask,
  getTasks,
  updateStatus,
  deleteTask,
  _resetForTest
} = require("./Task");

// 每个测试前重置数据
beforeEach(() => {
  _resetForTest();
});

describe("Task 模块", () => {

  describe("创建任务", () => {

    test("用户可以只传标题创建任务", () => {
      const task = createTask("买牛奶");
      expect(task.title).toBe("买牛奶");
      expect(task.description).toBe("");
      expect(task.status).toBe("todo");
      expect(task.priority).toBe("medium");
      expect(task.id).toBe(1);
      expect(task.createdAt).toBeDefined();
    });

    test("用户可以创建带描述的任务", () => {
      const task = createTask("买牛奶", "买低脂牛奶");
      expect(task.title).toBe("买牛奶");
      expect(task.description).toBe("买低脂牛奶");
    });

    test("用户可以创建带优先级的任务", () => {
      const task = createTask("买牛奶", "", "high");
      expect(task.priority).toBe("high");
    });

    test("标题不能为空", () => {
      expect(() => createTask("")).toThrow("标题不能为空");
      expect(() => createTask("   ")).toThrow("标题不能为空");
    });

    test("优先级必须有效", () => {
      expect(() => createTask("买牛奶", "", "invalid")).toThrow("无效的优先级");
    });

  });

  describe("查看任务列表", () => {

    test("用户可以看到刚创建的任务", () => {
      createTask("买牛奶");
      const tasks = getTasks();
      expect(tasks.length).toBe(1);
      expect(tasks[0].title).toBe("买牛奶");
    });

    test("任务按创建时间倒序排列", () => {
      createTask("任务 1");
      createTask("任务 2");
      createTask("任务 3");
      const tasks = getTasks();
      expect(tasks[0].title).toBe("任务 3");
      expect(tasks[1].title).toBe("任务 2");
      expect(tasks[2].title).toBe("任务 1");
    });

  });

  describe("更新任务状态", () => {

    test("用户可以把任务从 todo 改成 in-progress", () => {
      const task = createTask("买牛奶");
      const updated = updateStatus(task.id, "in-progress");
      expect(updated.status).toBe("in-progress");
    });

    test("用户可以把任务从 in-progress 改成 done", () => {
      const task = createTask("买牛奶");
      updateStatus(task.id, "in-progress");
      const updated = updateStatus(task.id, "done");
      expect(updated.status).toBe("done");
    });

    test("用户可以把任务从 todo 直接改成 done", () => {
      const task = createTask("买牛奶");
      const updated = updateStatus(task.id, "done");
      expect(updated.status).toBe("done");
    });

    test("状态必须有效", () => {
      const task = createTask("买牛奶");
      expect(() => updateStatus(task.id, "invalid")).toThrow("无效的状态");
    });

    test("状态转换不允许时会报错", () => {
      const task = createTask("买牛奶");
      updateStatus(task.id, "done");
      expect(() => updateStatus(task.id, "todo")).toThrow("状态转换不允许");
    });

    test("更新不存在的任务会报错", () => {
      expect(() => updateStatus(999, "done")).toThrow("任务不存在");
    });

    test("更新状态后，任务列表里能看到新状态", () => {
      const task = createTask("买牛奶");
      updateStatus(task.id, "in-progress");
      const tasks = getTasks();
      expect(tasks[0].status).toBe("in-progress");
    });

  });

  describe("按优先级筛选任务", () => {

    test("用户可以只看高优先级任务", () => {
      createTask("高优先级任务", "", "high");
      createTask("中优先级任务", "", "medium");
      createTask("低优先级任务", "", "low");
      const tasks = getTasks({ priority: "high" });
      expect(tasks.length).toBe(1);
      expect(tasks[0].title).toBe("高优先级任务");
    });

    test("用户可以只看低优先级任务", () => {
      createTask("高优先级任务", "", "high");
      createTask("低优先级任务", "", "low");
      const tasks = getTasks({ priority: "low" });
      expect(tasks.length).toBe(1);
      expect(tasks[0].title).toBe("低优先级任务");
    });

    test("不传筛选条件返回所有任务", () => {
      createTask("任务 1", "", "high");
      createTask("任务 2", "", "medium");
      createTask("任务 3", "", "low");
      const tasks = getTasks();
      expect(tasks.length).toBe(3);
    });

    test("无效的优先级会报错", () => {
      expect(() => getTasks({ priority: "invalid" })).toThrow("无效的优先级");
    });

  });

  describe("删除任务", () => {

    test("用户可以删除任务", () => {
      const task = createTask("买牛奶");
      deleteTask(task.id);
      const tasks = getTasks();
      expect(tasks.length).toBe(0);
    });

    test("删除不存在的任务会报错", () => {
      expect(() => deleteTask(999)).toThrow("任务不存在");
    });

  });

});
