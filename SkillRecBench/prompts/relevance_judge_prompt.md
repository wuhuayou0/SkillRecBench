# Relevance Judge Prompt(推荐相关性盲评)

来源:`05_skillrec/eval_final_bge.py` 函数 `judge_one`(原 04_recommenders/eval_final_bge.py L100-125)。

参数:model=qwen3.7-plus(default), temperature=0.1, max_tokens=10, retry=3, timeout=20s。

## System

```
只输出数字0/1/2。
```

## User 模板

```
判断以下技能是否能完成给定任务。只输出一个数字(0/1/2)。

任务: {task_prompt[:300]}

技能: {skill_name}
描述: {skill_desc[:300]}

0=不相关 1=部分相关 2=高度相关可完成
只输出数字:
```

> 解析:取回复中第一个数字,截断到 ≤2;三次尝试失败返回 0。
