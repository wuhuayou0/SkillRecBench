# -*- coding: utf-8 -*-
"""SkillRecBench: data loading and evaluation measures.

    import sys; sys.path.insert(0, "scripts")
    from load_benchmark import load, evaluate_metrics
    data = load()                      # or load("path/to/SkillRecBench")

`rankings` may be a list indexed by task_id or a dict keyed by task_id (int or str); each entry is a
list of pool indices, most relevant first. Unlabeled task-skill pairs count as irrelevant (label 0).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(root=None):
    root = Path(root) if root else ROOT
    d = root / "data"
    tasks = [json.loads(l) for l in open(d / "tasks.jsonl", encoding="utf-8")]
    skills = [json.loads(l) for l in open(d / "skills.jsonl", encoding="utf-8")]
    pool_ids = json.load(open(d / "pool_order.json", encoding="utf-8"))["skill_ids"]
    by_id = {s["skill_id"]: s for s in skills}
    return {
        "tasks": tasks,                                    # 2,707 tasks; task_id equals the list index
        "skills": skills,                                  # 26,502 catalog entries
        "pool": [by_id[i] for i in pool_ids],              # 5,000 candidates; list index = pool_index
        "judged": json.load(open(d / "judged_pairs.json", encoding="utf-8"))["pairs"],  # "task_id:pool_index" -> 0/1/2
        "split": json.load(open(d / "split.json", encoding="utf-8")),                   # dev / test / exec task ids
    }


def _ranking(rankings, ti):
    if isinstance(rankings, dict):
        return rankings[ti] if ti in rankings else rankings[str(ti)]
    return rankings[ti]


def rel(ti, si, judged):
    """Relevance label of a task-skill pair; 0 if the pair is unlabeled."""
    return judged.get(f"{ti}:{si}", 0)


def qrs_pair(rel_v, ss_raw):
    """QRS of one pair: harmonic mean of r = Rel/2 and u = (SS-1)/4; 0 if either is 0 (Eq. (12))."""
    rn = rel_v / 2.0
    sn = (float(ss_raw) - 1.0) / 4.0
    if rn <= 0 or sn <= 0:
        return 0.0
    return 2.0 * rn * sn / (rn + sn)


def evaluate_metrics(rankings, tasks, pool, judged, idxs, K=5):
    """Multi-Hit@K, Avg Rel@K, Avg SS@K, QRS@K (macro-averaged over tasks) and judged@K (share of the top-K pairs that have a label)."""
    n = len(idxs)
    multi_hit = qrs_sum = avg_ss = avg_rel = judged_hits = 0.0
    for ti in idxs:
        topk = _ranking(rankings, ti)[:K]
        rels = [rel(ti, int(i), judged) for i in topk]
        ss_raw = [float(pool[int(i)].get("skillability_score") or 0) for i in topk]
        multi_hit += 1 if max(rels) >= 2 else 0
        qrs_sum += sum(qrs_pair(r, s) for r, s in zip(rels, ss_raw)) / K
        avg_ss += sum(ss_raw) / K
        avg_rel += sum(rels) / K
        judged_hits += sum(1 for i in topk if f"{ti}:{int(i)}" in judged)
    return {
        "n_tasks": n,
        f"multi_hit@{K}": multi_hit / n,
        f"avg_rel@{K}": avg_rel / n,
        f"avg_ss@{K}": avg_ss / n,
        f"qrs@{K}": qrs_sum / n,
        f"judged@{K}": judged_hits / (n * K),
    }


def ndcg(rankings, tasks, pool, judged, idxs, K=5):
    """NDCG@K with gain 2^rel - 1; the ideal list is built from the labels of the given ranking.
    Not reported in the paper."""
    import math
    nd = 0.0
    for ti in idxs:
        r = _ranking(rankings, ti)
        rels = [rel(ti, int(i), judged) for i in r[:K]]
        dcg = sum((2 ** x - 1) / math.log2(p + 2) for p, x in enumerate(rels))
        ideal = sorted([rel(ti, int(i), judged) for i in r], reverse=True)[:K]
        idcg = sum((2 ** x - 1) / math.log2(p + 2) for p, x in enumerate(ideal))
        nd += dcg / idcg if idcg > 0 else 0.0
    return nd / len(idxs)


def recall(rankings, pool, judged, idxs, K=5):
    """Share of tasks with at least one label-2 skill in the top-K (identical to Multi-Hit@K)."""
    return sum(1 for ti in idxs if any(rel(ti, int(i), judged) == 2 for i in _ranking(rankings, ti)[:K])) / len(idxs)


if __name__ == "__main__":
    data = load()
    s = data["split"]
    print(f"tasks={len(data['tasks'])} skills={len(data['skills'])} pool={len(data['pool'])} "
          f"labels={len(data['judged'])} dev={s['n_dev']} test={s['n_test']} exec={s['n_exec']}")
