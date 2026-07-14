#!/usr/bin/env python3
"""
申论题型快速分类器 - 基于关键词/正则匹配
用法: python3 classify.py "题目文本"
输出: JSON {"type": "题型名", "confidence": "high|medium|low"}
"""

import sys
import json
import re


def classify(question: str) -> dict:
    """根据题目文本判断申论题型"""

    # === 大作文（优先级最高：有明确的大作文标志） ===
    dawen_patterns = [
        r"写一篇文章",
        r"自拟题目",
        r"自选角度",
        r"自拟标题",
        r"议论文",
        r"申发论述",
        r"文章写作",
        r"写一篇.*文章",
        r"围绕.*写一篇文章",
        r"结合.*写一篇文章",
    ]
    for p in dawen_patterns:
        if re.search(p, question):
            return {"type": "大作文", "confidence": "high"}

    # === 应用文写作 ===
    yingyong_patterns = [
        (r"倡议书", "high"),
        (r"工作汇报|汇报材料|汇报", "high"),
        (r"考察报告", "high"),
        (r"经验交流|交流稿", "high"),
        (r"通知$|通知》|写.*通知", "high"),
        (r"讲话稿|发言稿|致辞", "high"),
        (r"调研报告", "high"),
        (r"宣传稿", "high"),
        (r"导言", "high"),
        (r"公开信", "high"),
        (r"编者按", "high"),
        (r"简报", "high"),
        (r"工作方案", "medium"),
        (r"建议书", "medium"),  # 可能是应用文也可能是对策题，需根据上下文判断
    ]
    for pat, conf in yingyong_patterns:
        if re.search(pat, question):
            return {"type": "应用文写作", "confidence": conf}

    # === 综合分析题 ===
    zonghe_patterns = [
        (r"分析.*(原因|问题|现象|意义|影响)", "high"),
        (r"评述|评析", "high"),
        (r"阐释|阐述", "high"),
        (r"谈谈.*(理解|看法|认识|启示)", "high"),
        (r"如何理解", "high"),
        (r"怎么看", "medium"),
        (r"理解.*含义|理解.*内涵", "high"),
    ]
    for pat, conf in zonghe_patterns:
        if re.search(pat, question):
            return {"type": "综合分析题", "confidence": conf}

    # === 对策建议题 ===
    duice_patterns = [
        (r"提出.*建议", "high"),
        (r"拟定.*措施", "high"),
        (r"说明.*对策", "high"),
        (r"提出.*对策", "high"),
        (r"怎么办|如何解决|怎样解决", "medium"),
        (r"提出.*解决办法", "high"),
        (r"针对性.*建议", "high"),
        (r"可行.*建议", "medium"),
    ]
    for pat, conf in duice_patterns:
        if re.search(pat, question):
            return {"type": "对策建议题", "confidence": conf}

    # === 概括论述题（兜底：动词标志最明确） ===
    gaikuo_patterns = [
        (r"概括", "high"),
        (r"归纳", "high"),
        (r"总结", "high"),
        (r"概述", "high"),
        (r"梳理", "medium"),
        (r"列出", "medium"),
        (r"指出.*(问题|原因|变化|意义|做法)", "medium"),
        (r"摘要|案例摘要|写.*摘要", "high"),  # 案例摘要属于概括论述类
    ]
    for pat, conf in gaikuo_patterns:
        if re.search(pat, question):
            return {"type": "概括论述题", "confidence": conf}

    # === 无法确定 ===
    return {"type": "unknown", "confidence": "low",
            "hint": "无法从关键词确定题型，请根据题目完整语境判断"}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # 从 stdin 读取
        question = sys.stdin.read().strip()
    else:
        question = " ".join(sys.argv[1:])

    result = classify(question)
    print(json.dumps(result, ensure_ascii=False))
