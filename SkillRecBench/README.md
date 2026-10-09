# SkillRecBench

SkillRecBench is a benchmark for skill recommendation in agent-skill marketplaces. Given a natural-language
task and a pool of candidate skills, a method returns a ranked list of skills; the benchmark evaluates the
relevance of the recommended skills, their static quality, and the trade-off between the two.

It is built from a March 2026 snapshot of 26,502 skills from the ClawHub marketplace and accompanies the paper

> **SkillRec: Quality-Aware Skill Recommendation for Agent Skill Marketplaces.** [TODO: authors, venue, link]

| Component | Size |
|---|---|
| Skill catalog | 26,502 skills (name, description, downloads, platform effectiveness value) |
| Skillability Scores (SS) | 17,446 skills, six rubric dimensions with evidence |
| Tasks | 2,707, generated from 577 of 600 seed skills stratified by SS |
| Candidate pool | 5,000 skills (the 600 seed skills and 4,400 other scored skills) |
| Relevance labels | 19,484 task-skill pairs, labels 0 / 1 / 2, for 800 tasks |
| Task sets | development 400, test 400 (no shared seed skill), execution 500 |

## Contents

```
SkillRecBench/
├── data/
│   ├── tasks.jsonl          # 2,707 tasks: task_id, seed_skill_id, seed_ss, prompt
│   ├── skills.jsonl         # 26,502 catalog entries: skill_id, name, description, downloads,
│   │                        #   effectiveness_score, skillability_score (SS, null if not scored)
│   ├── scores_llm.jsonl     # 17,446 scoring records: six dimension scores with evidence,
│   │                        #   weighted_SS, category, granularity, execution_mode
│   ├── pool_order.json      # the 5,000-skill candidate pool; list index = pool_index
│   ├── judged_pairs.json    # 19,484 relevance labels, "task_id:pool_index" -> 0/1/2
│   └── split.json           # development, test, and execution task ids
├── prompts/                 # prompts for scoring, task generation, relevance judging, execution assessment
├── scripts/
│   ├── load_benchmark.py            # data loader and evaluation measures
│   ├── semantic_baseline.py         # minimal TF-IDF example (requires scikit-learn)
│   └── LICENSE                      # MIT
├── STATS.md                 # statistics of all components
└── LICENSE                  # CC BY 4.0 (data)
```

## Quick start

```python
import sys; sys.path.insert(0, "scripts")
from load_benchmark import load, evaluate_metrics

data = load()
tasks, pool, judged, split = data["tasks"], data["pool"], data["judged"], data["split"]

# rankings[task_id] = pool indices, most relevant first (a list or a dict keyed by task_id)
rankings = your_recommender(tasks, pool)
print(evaluate_metrics(rankings, tasks, pool, judged, split["test_task_ids"], K=5))
```

## Evaluation protocol

All methods rank the same 5,000-skill pool for each task and are evaluated at K = 5 on the 400 test tasks.
A method may use the task text and the name, description, SS, download count, and effectiveness value of
each candidate. It must not use the generating seed of a task or any relevance label. Weights and other
hyper-parameters are selected on the development set only.

For a task q and a skill s with label Rel(q, s) in {0, 1, 2} and SS(s) in [1, 5]:

| Measure | Definition (per task, then averaged over tasks) |
|---|---|
| Multi-Hit@K | 1 if at least one of the top-K skills has label 2 |
| Avg Rel@K | mean label of the top-K skills |
| Avg SS@K | mean SS of the top-K skills |
| QRS@K | mean over the top-K skills of 2 r u / (r + u), with r = Rel/2 and u = (SS - 1)/4 (0 if r or u is 0) |
| judged@K | share of the top-K pairs that have a label |

`load_benchmark.py` also provides `ndcg` and `recall`, which the paper does not report; `recall` is
identical to Multi-Hit@K.

**Unlabeled pairs.** A recommended pair without a label counts as irrelevant. A new method may recommend
unlabeled pairs; label them with `prompts/relevance_judge_prompt.md` before computing the measures
(Qwen3.7-Plus, temperature 0.1, max_tokens 10; the first digit of the reply is the label, capped at 2).

**Labels.** The labels are LLM judgments of whether the name and description of a skill satisfy a task,
not independently established ground truth. All labels were assigned by the same judge model with the
same temperature and prompt.

## Construction

1. **Catalog.** Metadata and source files of 26,502 ClawHub skills; 17,455 have a `SKILL.md` document.
2. **Skillability scoring.** An LLM (Qwen3.7-Plus, temperature 0.1, JSON mode) scores 17,446 documented skills
   on the six dimensions of the Skillability rubric of Huang et al. (ICSE 2026): task clarity, interface
   clarity, composability, automation value, deployment friction, and operational risk. SS is the returned
   `weighted_SS`, which the prompt asks to compute as 0.25 TC + 0.20 IC + 0.20 C + 0.25 AV + 0.05 (6 - DF)
   + 0.05 (6 - OR); it is not recomputed.
3. **Task generation.** 600 seed skills are sampled from three SS groups (SS < 3: 80; 3 <= SS < 4: 120;
   SS >= 4: 400). For each seed, an LLM (temperature 0.7) receives its name, description, and `SKILL.md` and
   writes three to five user tasks without naming the skill and without any quality or popularity
   information. 23 seeds yield no task, so the 2,707 tasks come from 577 seeds.
4. **Candidate pool.** The 600 seed skills and 4,400 other scored skills (seed 42).
5. **Relevance labels.** For 800 tasks sampled uniformly from the 2,707, an LLM judge, blind to the method
   and rank, labels the top-5 pairs of the reported methods.
6. **Task sets.** The 800 labeled tasks are split into development and test sets of 400 tasks by seed skill
   (dynamic-programming subset-sum), so the two sets share no seed skill. The execution set contains 500
   tasks drawn from all 2,707 tasks (`random.Random(123)`), independently of this split.

The prompts in `prompts/` are the verbatim prompts used (most of them in Chinese); their headers refer to the
authors' internal code files. The execution assessment of the paper is described by its prompts; its outputs
are not part of this release. See `STATS.md` for distributions.

## Citation

```bibtex
[TODO: BibTeX entry of the SkillRec paper]
```

## License

The data are released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) and the code in
`scripts/` under the MIT License. Skill names and descriptions are taken from public ClawHub listings.
[TODO: confirm the redistribution terms for third-party skill metadata.]
