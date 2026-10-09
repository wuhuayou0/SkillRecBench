# -*- coding: utf-8 -*-
"""Offline example: a TF-IDF retrieval baseline evaluated on the test set (requires scikit-learn).

This is a minimal usage example; its configuration differs from the Semantic (TF-IDF) baseline of the
paper. Recommended pairs without a label count as irrelevant; label them with
prompts/relevance_judge_prompt.md before comparing its measures with those of the paper."""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from load_benchmark import load, evaluate_metrics

K = 5


def main():
    data = load()
    tasks, pool, judged, split = data["tasks"], data["pool"], data["judged"], data["split"]
    docs = [" ".join([s["name"] or "", s["description"] or ""]) for s in pool]   # skill text = name + description
    vec = TfidfVectorizer(max_features=20000, sublinear_tf=True).fit(docs)
    sim = (vec.transform([t["prompt"] for t in tasks]) @ vec.transform(docs).T).toarray()
    rankings = [[int(i) for i in np.argsort(-sim[ti], kind="stable")] for ti in range(len(tasks))]
    m = evaluate_metrics(rankings, tasks, pool, judged, split["test_task_ids"], K=K)
    print(f"TF-IDF example on the test set ({m['n_tasks']} tasks), K={K}:")
    for k, v in m.items():
        if k != "n_tasks":
            print(f"  {k:12s} {v:.4f}")


if __name__ == "__main__":
    main()
