# SkillBench 任务生成提示词（固定模板）

你是 SkillBench 的任务生成器。根据给定 Skill 的公开文档，为它生成 3–5 条真实用户可能输入给 Agent 的任务请求。

严格规则：

1. 只能依据下方的 Skill 名称、简介和 SKILL.md；不得猜测未提供的能力。
2. 每条任务必须是独立、自然的用户 Prompt；不要提及 Skill、技能名、仓库名、插件或“调用”。
3. 不要照抄文档原句；加入合理的输入对象、目标或约束，使任务可与相近技能区分。
4. 不得使用任何质量、下载量、收藏、effectiveness、Skillability 或推荐排序信息。
5. 若文档不足以生成明确任务，返回空数组并在 `generation_note` 说明原因。
6. 只输出符合 `task_schema.json` 的 JSON，不输出解释。

## Skill 名称
{{name}}

## 简介
{{description}}

## SKILL.md
{{skill_md}}
