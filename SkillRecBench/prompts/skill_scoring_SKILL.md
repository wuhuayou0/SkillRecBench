---
name: skillability-eval
description: >
  Evaluate an Agent Skill using the ICSE 2026 Skillability Score framework.
  Scores the target skill on six dimensions (TC, IC, C, AV, DF, OR) with 1-5 anchors,
  computes the weighted SS, assigns taxonomy labels, and outputs a structured report.
  Use when the user asks to "evaluate a skill", "assess skillability", "score this skill",
  or "rate this agent skill".
version: 1.0.0
license: MIT
---

# Skillability Eval — Agent Skill 六维评估

基于 ICSE 2026 论文 "From Software Repositories to Agent Skills" 的 Skillability Score 框架，
对任意 Agent Skill 进行六维量化评估。

## 输入

| 输入项 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `target_skill_path` | 路径 (本地目录 / 文件) | 是 | 待评估技能的根目录。至少包含 SKILL.md 或 README.md |
| `language` | string | 否 | 输出语言，默认 `zh`（中文）。可选 `en`（英文） |

Agent 调用方式示例:

```
/skillability-eval D:/rec_skill/skills/data_process
/skillability-eval /path/to/some-skill --lang en
```

## 输出

输出一个结构化的评估报告，包含以下三个部分:

### Part A: 六维评分表

| 维度 | 权重 | 得分 | 证据 |
|------|------|------|------|
| TC 任务清晰度 | 25% | 1-5 | 关键证据 |
| IC 接口清晰度 | 20% | 1-5 | 关键证据 |
| C 可组合性 | 20% | 1-5 | 关键证据 |
| AV 自动化价值 | 25% | 1-5 | 关键证据 |
| DF 部署摩擦 | 5% | 1-5 (原始分) | 关键证据 |
| OR 运行风险 | 5% | 1-5 (原始分) | 关键证据 |
| **加权总分 SS** | 100% | **SS 值** | — |

### Part B: 等级与解读

```
SS = 0.25×TC + 0.20×IC + 0.20×C + 0.25×AV + 0.05×(6−DF) + 0.05×(6−OR)
等级: S(≥4.5) / A(≥4.0) / B(≥3.0) / C(≥2.0) / D(<2.0)
```

### Part C: 分类标签

| 标签 | 取值 |
|------|------|
| 能力类别 (Category) | 11 选 1 |
| 粒度 (Granularity) | 4 选 1 |
| 执行模式 (Execution Mode) | 5 选 1 |

### Part D: 改进建议（可选）

如果 SS < 4.0，针对得分 ≤ 3 的维度提出 2-3 条具体改进建议。

## 工作流程 (Agent 执行步骤)

```
Step 1: 收集目标技能的材料
  ├── 读 SKILL.md (或 README.md) 全文
  ├── 读 .claude/settings.json (如有)
  ├── 读 config.yaml / package.json / requirements.txt (如有)
  └── 读关键代码文件 (接口定义、文件操作、网络调用)
         ↑
         文件优先级见 prompts/collection_priority.md

Step 2: 提取元数据 → 运行 scripts/collect_metadata.py
  ├── cd <当前skill目录> && python scripts/collect_metadata.py <目标技能路径>
  ├── 输出 PART 2 所需的 metadata JSON
  └── 将输出的 JSON 填入 Prompt 模板的 PART 2 占位符

Step 3: 组装 Prompt 并发送给 LLM
  ├── PART 1 (System Instruction)  ← 使用 prompts/rubrics_cn.txt 或 rubrics_en.txt
  ├── PART 2 (Metadata)            ← Step 2 的 JSON 输出
  ├── PART 3 (Content Excerpt)     ← Step 1 收集的文档和代码全文
  ├── PART 4 (JSON Schema)         ← 使用 prompts/ 中的固定模板
  └── 发送给 LLM (temperature=0.1, JSON Mode, retry on error)

Step 4: 解析输出并验证 → 运行 scripts/format_output.py
  ├── python scripts/format_output.py '<LLM返回的JSON>'
  ├── 自动验证: 分数范围、weighted_SS 计算正确性、分类标签有效性
  ├── 发现问题则提示修正，通过则格式化 Markdown 报告
  └── 输出 Part A/B/C/D 完整评估报告

Step 5 (可选): 如果 SS < 4.0, 运行 scripts/format_output.py 自动生成改进建议
```

## Prompt 模板

本 Skill 使用的评估 Prompt 模板严格按照论文附录 A 的四段式结构:

```
(1) System Instruction — 六个维度定义 + 1-5 锚点
(2) Artifact Metadata — JSON 格式元数据
(3) Content Excerpt — SKILL.md 全文 + 关键代码
(4) JSON Schema — 结构化输出约束 + 分类标签
```

完整模板见 `prompts/rubrics_en.txt`（英文）和 `prompts/rubrics_cn.txt`（中文）。


## 参考文献

- Huang, D. et al. "From Software Repositories to Agent Skills." ICSE 2026. CC-BY-4.0.
- 人版 Rubrics: 《通用Rubrics.docx》v1.3
- LLM Prompt 版: 《Skillability_LLM_Prompt.docx》《Skillability_LLM_Prompt_CN.docx》

## 依赖

- 无外部 Python 依赖（metadata 收集使用标准库）
- LLM 调用依赖当前 Agent 的模型能力
- 推荐 LLM 参数: temperature ≤ 0.1, Structured Output / JSON Mode 启用

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-07-18 | 初始版本，支持单技能六维评估 |
