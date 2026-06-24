#!/usr/bin/env python3
"""
Loop 输出校验脚本 —— AI 自查骗不过的最后一道关。

用法（reverse-loop —— 2 个文件）:
    python check-output.py reverse-loop <模块文档.md> <Loop 报告.md>

用法（其他 Loop —— 1 个文件）:
    python check-output.py <loop_name> <output_file>

支持:
    reverse-loop, grill-deep-loop, tdd-loop, codex-review-loop, doc-rot-loop

校验项:
    1. 必须有对应 Loop 要求的段落
    2. 自查表行数与该 Loop 的 AC 数量一致，且每行带评分
    3. 主产物中所有 `文件:行号` 引用是否能在 cwd 下找到对应文件
    4. 是否含"禁用模式"中列出的恒真断言、空泛问法等
       —— 段落级扫描：含 [待验证] 的段落（双换行分段）整体跳过
    5. 迭代信息：必须含轮次和是否达到停止条件

不通过 → exit 1，AI 应回到流程的"自查"步重新跑。
"""

import re
import sys
from pathlib import Path

# Loop 配置：每个 Loop 的 AC 数量、禁用模式、所需段落
LOOP_CONFIG = {
    "reverse-loop": {
        "ac_count": 6,
        "ac_prefix": "AC",
        # 2 文件模式：sections_in 指明每个文件应有的段落
        "files": 2,
        "module_doc_sections": [
            "## 理解范围", "## 业务职责", "## 接口与入口",
            "## 核心流程", "## 数据模型", "## 风险与异味",
        ],
        "report_sections": [
            "## 一、自查表", "## 二、需人工确认清单", "## 三、迭代信息",
        ],
        "forbidden_patterns": [
            (r"(?:可能|似乎|大概|应该是|推测)", "未标记的不确定描述（段落需以 [待验证] 开头）"),
        ],
    },
    "grill-deep-loop": {
        "ac_count": 8,
        "ac_prefix": "GQ",
        "files": 1,
        "required_sections": ["## 一、问题清单", "## 二、自查表", "## 三、优先级 5 问", "## 四、业务方专属问题"],
        "forbidden_patterns": [
            (r"如何保证.{0,15}\?", "空泛问法：'如何保证 XX'"),
            (r"是否考虑.{0,10}并发\?", "空泛问法：'是否考虑并发'"),
        ],
    },
    "tdd-loop": {
        "ac_count": 6,
        "ac_prefix": "TC",
        "files": 1,
        "required_sections": ["## 一、测试矩阵", "## 二、测试代码", "## 三、自查表", "## 四、需人工确认清单"],
        "forbidden_patterns": [
            (r"assertNotNull\(\s*result\s*\)", "TC6 违规：assertNotNull(result) 恒真断言"),
            (r"assertTrue\(\s*true\s*\)", "TC6 违规：assertTrue(true) 恒真断言"),
            (r"@Test\s+(?:public\s+)?void\s+test\d*\s*\(", "命名违规：test1() 类无意义命名"),
        ],
    },
    "codex-review-loop": {
        "ac_count": 6,
        "ac_prefix": "AC",
        "files": 1,
        "required_sections": ["## 一、总览", "## 二、问题列表", "## 三、自查表", "## 四、需人工确认清单"],
        "forbidden_patterns": [
            (r"建议优化此处\s*$", "空建议：'建议优化此处'，未说明如何优化"),
        ],
    },
    "doc-rot-loop": {
        "ac_count": 6,
        "ac_prefix": "AC",
        "files": 1,
        "required_sections": ["## 一、总览健康度", "## 二、腐化清单", "## 三、自查表", "## 四、行动清单"],
        "forbidden_patterns": [],
    },
}


def check_sections(content, required, file_label=""):
    errors = []
    for section in required:
        if section not in content:
            errors.append(f"[{file_label}] 缺少段落: {section}" if file_label else f"缺少段落: {section}")
    return errors


def check_self_review_table(content, ac_prefix, ac_count, file_label=""):
    """自查表中应有 ac_count 行 ACx/TCx/GQx/RCx 标签 + 全部带评分"""
    errors = []
    pattern = rf"\|\s*{ac_prefix}\d+"
    matches = re.findall(pattern, content)
    label = f"[{file_label}] " if file_label else ""
    if len(matches) < ac_count:
        errors.append(f"{label}自查表 {ac_prefix} 行数不足: 期望 {ac_count}, 实际 {len(matches)}")

    # 找自查表段并检查评分
    # 兼容 "## 一、自查表" 和 "## 二、自查表" 等
    table_re = re.search(r"##\s*[一二三四五六七八九十]、自查表\s*\n([\s\S]+?)(?=\n## |\Z)", content)
    if table_re:
        block = table_re.group(1)
        rows_with_score = len(re.findall(r"[✅⚠️❌]", block))
        if rows_with_score < ac_count:
            errors.append(f"{label}自查表带评分的行不足: 期望 {ac_count}, 实际 {rows_with_score}")
    return errors


def check_file_references(content, cwd, file_label=""):
    """提取 `文件名.ext:行号` 形式的引用，验证文件存在；找不到 >5 处发警告"""
    errors = []
    pattern = r"([A-Za-z][A-Za-z0-9_/.]+\.(?:java|kt|py|ts|js|yml|yaml))(?::(\d+))?"
    refs = set(re.findall(pattern, content))

    not_found = []
    for ref, _ in refs:
        # 跳过明显是文档自引用
        if ref.startswith(("docs/", "AI版/", "AI_工作流", "CLAUDE.md", "README.md")):
            continue
        if "Loop" in ref or "loop.md" in ref:
            continue
        if ref.endswith(".md"):
            continue

        found = False
        for _ in cwd.rglob(Path(ref).name):
            found = True
            break
        if not found:
            not_found.append(ref)

    label = f"[{file_label}] " if file_label else ""
    if not_found and len(not_found) > 5:
        errors.append(
            f"{label}⚠️ 警告: {len(not_found)} 处文件引用在当前目录下未找到（可能 AI 编造）: "
            f"{not_found[:3]}..."
        )
    return errors


def check_forbidden_patterns(content, patterns, file_label=""):
    """段落级扫描：以双换行分段，含 [待验证] 的段落整体跳过"""
    errors = []
    label = f"[{file_label}] " if file_label else ""
    paragraphs = content.split("\n\n")
    for pattern, desc in patterns:
        hits = 0
        for para in paragraphs:
            # 段落级豁免：含 [待验证] 整段不扫描
            if "[待验证]" in para:
                continue
            hits += len(re.findall(pattern, para))
        if hits:
            errors.append(f"{label}违规: {desc} (命中 {hits} 处)")
    return errors


def check_iteration_info(content):
    errors = []
    if not re.search(r"轮次[:：]\s*[12]", content):
        errors.append("缺少 '轮次: 1' 或 '轮次: 2'")
    if not re.search(r"是否达到停止条件[:：]\s*[是否]", content):
        errors.append("缺少 '是否达到停止条件: 是/否'")
    return errors


def validate_single_file(loop_name, path, config):
    """单文件模式校验：grill-deep-loop / tdd-loop / codex-review-loop / doc-rot-loop"""
    content = path.read_text(encoding="utf-8")
    cwd = Path.cwd()

    errors = []
    errors += check_sections(content, config["required_sections"])
    errors += check_self_review_table(content, config["ac_prefix"], config["ac_count"])
    errors += check_forbidden_patterns(content, config["forbidden_patterns"])
    errors += check_iteration_info(content)
    errors += check_file_references(content, cwd)
    return errors


def validate_reverse_loop(module_doc_path, report_path, config):
    """reverse-loop 2 文件模式：模块文档 + Loop 报告分别校验"""
    cwd = Path.cwd()
    errors = []

    # 文件 1：模块文档 —— 检查段落 + 禁用词 + 行号引用
    module_content = module_doc_path.read_text(encoding="utf-8")
    errors += check_sections(module_content, config["module_doc_sections"], "模块文档")
    errors += check_forbidden_patterns(module_content, config["forbidden_patterns"], "模块文档")
    errors += check_file_references(module_content, cwd, "模块文档")

    # 文件 2：Loop 报告 —— 检查段落 + 自查表 + 迭代信息
    report_content = report_path.read_text(encoding="utf-8")
    errors += check_sections(report_content, config["report_sections"], "Loop 报告")
    errors += check_self_review_table(report_content, config["ac_prefix"], config["ac_count"], "Loop 报告")
    errors += check_iteration_info(report_content)

    return errors


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)

    loop_name = sys.argv[1]
    if loop_name not in LOOP_CONFIG:
        print(f"❌ 未知 Loop: {loop_name}")
        print(f"   支持: {', '.join(LOOP_CONFIG.keys())}")
        sys.exit(2)

    config = LOOP_CONFIG[loop_name]
    expected_files = config["files"]

    paths = []
    for arg in sys.argv[2:]:
        p = Path(arg)
        if not p.exists():
            print(f"❌ 文件不存在: {p}")
            sys.exit(2)
        paths.append(p)

    if len(paths) != expected_files:
        print(f"❌ {loop_name} 需要 {expected_files} 个文件参数，实际给了 {len(paths)} 个")
        print(f"   用法见脚本顶部 docstring")
        sys.exit(2)

    print(f"🔍 校验 {loop_name}: {', '.join(str(p) for p in paths)}\n")

    if loop_name == "reverse-loop":
        errors = validate_reverse_loop(paths[0], paths[1], config)
    else:
        errors = validate_single_file(loop_name, paths[0], config)

    if not errors:
        print("✅ 全部校验通过")
        sys.exit(0)

    print(f"❌ 发现 {len(errors)} 个问题:")
    for i, err in enumerate(errors, 1):
        print(f"  {i}. {err}")
    print("\n→ AI 应回到流程的'自查'步重新跑，针对以上问题修正。")
    sys.exit(1)


if __name__ == "__main__":
    main()
