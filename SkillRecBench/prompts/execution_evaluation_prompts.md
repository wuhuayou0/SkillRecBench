# RQ4 执行评测 Prompt(Executor + Execution Judge)

来源:`05_skillrec/rq4_execution_bge2.py`(Top-1)与 `05_skillrec/rq4_top5_execution.py`(Top-5)。

通用参数:model=qwen3.7-plus;Executor temperature=0.3, max_tokens=600;Judge temperature=0.1;均无 system 消息;retry=3, timeout=90s。

## 1. Top-1 Executor(rq4_execution_bge2.py L121-132)

```
你是一个 AI Agent。使用以下技能来完成任务。

任务: {task_prompt[:400]}

可用技能: {skill_name}
技能描述: {skill_desc[:500]}

请描述你如何完成这个任务，以及最终的输出结果。分两段:
[执行过程]: (简要描述步骤)
[输出结果]: (产出的具体内容)
```

## 2. Top-1 Execution Judge(rq4_execution_bge2.py L134-149)

```
你是一个 Agent 任务质量评判器。评估以下执行结果。

任务: {task_prompt[:400]}

推荐技能 [{label}]: {skill_name}

执行输出: {result[:500] if result else '(无输出)'}

请给三个 0-1 分数（保留一位小数）:
1. 任务完成度 (能否完成任务? 0=不能, 1=完美完成)
2. 技能有用度 (推荐技能对完成任务有多大帮助? 0=无用, 1=关键)
3. 输出质量 (最终产出质量如何? 0=差, 1=优秀)

只输出一行: completion=X.X usefulness=X.X quality=X.X
```

> 解析(parse_judge, L63-77):对三个维度分别按中英文键名正则提取数值,全 None 记为解析失败。

## 3. Top-5 Executor(rq4_top5_execution.py L128-140)

```
你是一个 AI Agent。以下是 5 个可用技能（名称与描述）。请先选择最适合完成任务的技能，再描述执行过程与最终输出结果。

任务: {task_prompt[:400]}

可用技能列表:
{skill_list_text[:900]}

输出分三段:
[选择技能]: 只写技能名称
[执行过程]: (简要描述步骤)
[输出结果]: (产出的具体内容)
```

> skill_list_text = 每行 `{i}. {name} — {desc[:120]}`(L121-126)。

## 4. Top-5 Execution Judge(rq4_top5_execution.py L142-158)

```
你是一个 Agent 任务质量评判器。评估以下执行结果。执行 Agent 是从一个技能列表中自选技能完成任务的。

任务: {task_prompt[:400]}

推荐列表 [{label}] 内容:
{skill_list_text[:900]}

执行输出: {result[:500] if result else '(无输出)'}

请给三个 0-1 分数（保留一位小数）:
1. 任务完成度 (能否完成任务? 0=不能, 1=完美完成)
2. 技能有用度 (推荐列表对完成任务有多大帮助? 0=无用, 1=关键)
3. 输出质量 (最终产出质量如何? 0=差, 1=优秀)

只输出一行: completion=X.X usefulness=X.X quality=X.X
```
