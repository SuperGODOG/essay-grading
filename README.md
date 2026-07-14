# essay-grading

申论作文批改 Hermes Skill —— 基于题型自动识别的智能批改系统。

## 支持的题型

| 题型 | 识别标志 | 评分侧重 |
|------|---------|---------|
| 概括论述题 | 概括、归纳、总结、概述 | 要点完整性、原关键词保留 |
| 对策建议题 | 提出建议、拟定措施、说明对策 | 对策针对性、可行性、操作性 |
| 综合分析题 | 分析、评述、阐释、理解 | What-Why-How 结构、辩证深度 |
| 应用文写作 | 倡议书/汇报/通知/讲话稿等 | 材料对策权重(70-80%)、格式规范 |
| 大作文 | 写一篇文章、自拟题目、议论文 | 论点明确性、论证充分性、结构完整性 |

## 架构

```
essay-grading/
├── SKILL.md                       # 主工作流：题型路由 → 加载标准 → 批改 → 输出
├── references/
│   ├── gaikuolunshu.md            # 概括论述题专版
│   ├── duicejianyi.md             # 对策建议题专版
│   ├── zonghefenxi.md             # 综合分析题专版
│   ├── yingyongwen.md             # 应用文写作专版
│   └── dazuowen.md                # 大作文专版（写作指导 + 评分标准）
├── scripts/
│   └── classify.py                # 关键词/正则题型快速分类器
└── assets/
    └── rubric.json                # 通用评分维度与等级标准
```

**条件判断机制**：Skill 层通过 SKILL.md 定义分支逻辑 + `classify.py` 做关键词匹配 + Progressive Disclosure（只加载匹配的 reference 文件），LLM 作为执行引擎自然走 Plan-Execute 流程。

## 安装

```bash
git clone https://github.com/SuperGODOG/essay-grading.git
ln -s "$(pwd)/essay-grading" ~/.hermes/skills/essay-grading
```

Hermes 会自动加载。之后在对话中提交申论题目即可触发。

## Roadmap

### v1.1 — 大作文批改增强
- [ ] 参照其他 4 个题型的精细度，补全大作文评分细则（要点/表述/格式三维打分）
- [ ] 新增大作文专属打分示例模板
- [ ] 关联 rubric.json 中大作文子维度

### v1.2 — 多 Agent 讨论模式
- [ ] 大作文启用并行多 Agent 评分（delegate_task）
  - Agent A：内容与结构
  - Agent B：语言与规范
  - Orchestrator：综合讨论、消解分歧、输出最终分数
- [ ] 可选扩展到其他主观题型（综合分析）

### v1.3 — 体验优化
- [ ] classify.py 增加更多边界关键词（近义词、歧义处理）
- [ ] 批改输出支持分项分数可视化
- [ ] 标准答案生成支持多方案对比

### v2.0 — 智能增强
- [ ] 接入材料全文理解（长文本 context 管理）
- [ ] 历史批改记录追踪（考生进步曲线）
- [ ] 错题/薄弱点自动归纳

## 使用方式

在 Hermes 对话中直接提交题目和答案：

```
【题目】概括材料中反映的主要问题。（10分，不超过200字）
【材料】近年来，随着城市化进程加快...
【我的答案】1. 环境污染严重 2. 交通拥堵 3. ...
```

Skill 自动识别为「概括论述题」→ 加载对应标准 → 输出标准答案 + 逐项打分 + 改进建议。

如果只提交题目不提交答案，则仅输出标准答案。

## License

MIT
