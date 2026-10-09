# SkillRecBench Statistics

All numbers are computed from the files in `data/`. Section numbers, table numbers, and equation numbers
refer to the SkillRec paper.

## 1. Skill catalog and Skillability Scores

| Statistic | Value |
|---|---|
| Skills in the catalog (ClawHub snapshot, March 2026) | 26,502 |
| Skills with a Skillability Score (SS) | 17,446 (65.8%) |
| Skills with downloads > 0 | 26,359 |
| Downloads per skill | median 222, mean 786 |
| SS range | [1.00, 5.00] |
| SS mean / median / standard deviation | 4.031 / 4.350 / 0.871 |

SS by integer bucket (bucket k contains k <= SS < k+1; bucket 5 contains SS = 5):

| Bucket | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Skills | 861 | 1,569 | 2,619 | 12,335 | 62 |

Six rubric dimensions (17,446 scoring records). Higher is better for TC, IC, C, and AV; lower is
better for DF and OR, which enter SS reverse-coded.

| Dimension | Mean | SD | Score 1 | Score 5 |
|---|---|---|---|---|
| TC, task clarity | 4.44 | 0.90 | 110 | 11,624 |
| IC, interface clarity | 3.66 | 1.23 | 1,118 | 5,487 |
| C, composability | 3.23 | 1.27 | 2,512 | 2,386 |
| AV, automation value | 4.33 | 1.25 | 1,507 | 12,333 |
| DF, deployment friction | 2.70 | 1.13 | 3,417 | 302 |
| OR, operational risk | 2.87 | 1.11 | 3,284 | 260 |

SS = 0.25 TC + 0.20 IC + 0.20 C + 0.25 AV + 0.05 (6 - DF) + 0.05 (6 - OR). The released SS is the
`weighted_SS` value returned by the scorer (Section 3.4 of the paper); it is not recomputed from the
dimension scores.

### Functional category (taxonomy of Huang et al., ICSE 2026)

| Category | Skills |
|---|---|
| Knowledge_Workflow | 3,256 |
| External_Service_Connectors | 3,062 |
| Data_Retrieval_Search | 1,985 |
| System_Infrastructure | 1,951 |
| Business_Productivity | 1,420 |
| Web_Automation | 1,365 |
| Communication_Collaboration | 910 |
| Code_DevOps | 858 |
| Multimedia_Content | 820 |
| Document_Processing | 511 |
| Other | 532 |
| Labels outside the taxonomy (e.g. Security: 39) | 776 |

The paper counts the 776 labels outside the taxonomy as Other.

### Granularity

| Granularity | Skills |
|---|---|
| workflow_skill | 8,087 |
| service_wrapper | 7,210 |
| primitive_tool | 2,078 |
| platform_adapter | 62 |
| browser_mediated | 5 |
| protocol_specification | 1 |
| Other | 1 |
| plugin | 1 |
| core-patch | 1 |

## 2. Task generation

| Statistic | Value |
|---|---|
| Seed skills (stratified by SS, seed 42) | 600 |
| Seed skills with at least one task | 577 |
| Tasks | 2,707 |
| Tasks per seed skill | 400 seeds with 5, 176 seeds with 4, 1 seed with 3, 23 seeds with 0 |
| Task length (characters) | 7 to 730, mean 121.6, median 112 |
| Tasks containing Chinese characters | 701 (25.9%) |

Task length in 50-character bins: 0-49: 344, 50-99: 802, 100-149: 751, 150-199: 492, 200-249: 206, 250-299: 71, 300-349: 25, 350+: 16.

SS groups at each construction step (a task belongs to the group of its seed skill, Eq. (11)):

| SS group | Scored skills | Candidate pool | Seed skills | Seeds with tasks | Tasks |
|---|---|---|---|---|---|
| Low (SS < 3) | 2,430 | 694 | 80 | 73 | 337 |
| Medium (3 <= SS < 4) | 2,619 | 785 | 120 | 115 | 532 |
| High (SS >= 4) | 12,397 | 3,521 | 400 | 389 | 1,838 |
| Total | 17,446 | 5,000 | 600 | 577 | 2,707 |

## 3. Candidate pool

5,000 skills: the 600 seed skills (pool indices 0-599) and 4,400 other scored skills
(shuffled with seed 42). The generating seed of every task is in the pool.

## 4. Relevance labels

| Label | Pairs | Share |
|---|---|---|
| 2 (highly relevant) | 1,815 | 9.3% |
| 1 (partially relevant) | 1,192 | 6.1% |
| 0 (irrelevant) | 16,477 | 84.6% |
| Total | 19,484 | 100% |

All labels were assigned by the same judge (Qwen3.7-Plus, temperature 0.1) with the same prompt
(`prompts/relevance_judge_prompt.md`).

| | Development | Test |
|---|---|---|
| Labeled pairs | 5,002 (12.5 per task) | 14,482 (36.2 per task) |
| Shares of labels 0 / 1 / 2 | 73.8% / 10.5% / 15.7% | 88.3% / 4.6% / 7.1% |
| Tasks with a label 2 | 340 (85.0%) | 353 (88.2%) |

## 5. Task sets

| | Development | Test | Execution |
|---|---|---|---|
| Tasks | 400 | 400 | 500 |
| Seed skills | 228 | 232 | 360 |
| Mean SS over seed skills | 4.066 | 4.091 | 4.053 |
| Mean task length (characters) | 119.3 | 125.0 | 119.9 |

The development and test sets share no seed skill. The execution set shares 66 tasks with the development
set and 96 with the test set; 338 of its tasks are in neither.
