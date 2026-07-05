/**
 * Task 模块
 *
 * 深模块示例：简单接口，丰富实现
 *
 * 公开接口：
 * - createTask(title, description?, priority?)
 * - getTasks(filter?)
 * - updateStatus(taskId, newStatus)
 * - deleteTask(taskId)
 *
 * 隐藏的复杂性：
 * - 状态机规则
 * - ID 生成
 * - 任务存储
 * - 按优先级筛选
 */

let tasks = [];
let nextId = 1;

const VALID_STATUSES = ["todo", "in-progress", "done"];
const VALID_PRIORITIES = ["low", "medium", "high"];

// 状态机规则：哪些状态转换允许
const ALLOWED_TRANSITIONS = {
  "todo": ["in-progress", "done"],
  "in-progress": ["done"],
  "done": [] // 第一版不支持回退
};

/**
 * 创建一个新任务
 *
 * @param {string} title - 任务标题（必填）
 * @param {string} [description] - 任务描述（可选）
 * @param {string} [priority="medium"] - 优先级（可选，默认 medium）
 * @returns {Object} 创建的任务
 * @throws {Error} 如果标题为空或优先级无效
 */
function createTask(title, description, priority = "medium") {
  if (!title || title.trim() === "") {
    throw new Error("标题不能为空");
  }

  if (!VALID_PRIORITIES.includes(priority)) {
    throw new Error(`无效的优先级：${priority}，有效值：${VALID_PRIORITIES.join(", ")}`);
  }

  const task = {
    id: nextId++,
    title: title.trim(),
    description: description ? description.trim() : "",
    status: "todo",
    priority: priority,
    createdAt: new Date().toISOString()
  };

  tasks.push(task);
  return task;
}

/**
 * 获取任务列表
 *
 * @param {Object} [filter] - 筛选条件（可选）
 * @param {string} [filter.priority] - 按优先级筛选
 * @returns {Array} 任务列表（按创建时间倒序）
 */
function getTasks(filter) {
  let result = [...tasks];

  if (filter && filter.priority) {
    if (!VALID_PRIORITIES.includes(filter.priority)) {
      throw new Error(`无效的优先级：${filter.priority}`);
    }
    result = result.filter(t => t.priority === filter.priority);
  }

  // 按创建时间倒序
  result.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

  return result;
}

/**
 * 更新任务状态
 *
 * @param {number} taskId - 任务 ID
 * @param {string} newStatus - 新状态
 * @returns {Object} 更新后的任务
 * @throws {Error} 如果任务不存在、状态无效或状态转换不允许
 */
function updateStatus(taskId, newStatus) {
  const task = tasks.find(t => t.id === taskId);
  if (!task) {
    throw new Error(`任务不存在：${taskId}`);
  }

  if (!VALID_STATUSES.includes(newStatus)) {
    throw new Error(`无效的状态：${newStatus}，有效值：${VALID_STATUSES.join(", ")}`);
  }

  const allowed = ALLOWED_TRANSITIONS[task.status];
  if (!allowed.includes(newStatus)) {
    throw new Error(`状态转换不允许：${task.status} → ${newStatus}`);
  }

  task.status = newStatus;
  return task;
}

/**
 * 删除任务
 *
 * @param {number} taskId - 任务 ID
 * @returns {boolean} 删除成功返回 true
 * @throws {Error} 如果任务不存在
 */
function deleteTask(taskId) {
  const index = tasks.findIndex(t => t.id === taskId);
  if (index === -1) {
    throw new Error(`任务不存在：${taskId}`);
  }

  tasks.splice(index, 1);
  return true;
}

// 测试辅助：重置数据（只用于测试）
function _resetForTest() {
  tasks = [];
  nextId = 1;
}

module.exports = {
  createTask,
  getTasks,
  updateStatus,
  deleteTask,
  _resetForTest
};
