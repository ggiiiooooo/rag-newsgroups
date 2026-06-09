"""Оценка качества retrieval: hit@k и MRR на наборе эталонных вопросов.

Реализованное улучшение из homework/IMPROVEMENTS.md (п. «Оценка качества / Eval»).

Для каждого вопроса известна ожидаемая тематическая группа (category 20 Newsgroups).
Считаем:
- hit@k  — доля вопросов, где хотя бы один из top-k чанков принадлежит нужной группе;
- MRR    — средний обратный ранг первого правильного попадания.

Запуск:
    uv run python scripts/eval_retrieval.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import RAW_DATASETS, TOP_K
from app.retriever import Retriever

# Эталонный набор: вопрос -> ожидаемая группа 20 Newsgroups
GOLD = [
    ("public key encryption and cryptography", "sci.crypt"),
    ("NASA space shuttle launch into orbit", "sci.space"),
    ("hockey playoff game and the season", "rec.sport.hockey"),
    ("baseball pitcher batting average", "rec.sport.baseball"),
    ("car engine and dealer prices", "rec.autos"),
    ("motorcycle riding and helmet safety", "rec.motorcycles"),
    ("graphics image file formats and rendering", "comp.graphics"),
    ("symptoms treatment and medical doctor", "sci.med"),
    ("gun control and second amendment rights", "talk.politics.guns"),
    ("belief in god and christian faith", "soc.religion.christian"),
]


def load_doc_category() -> dict[str, str]:
    """doc_id -> category, из data/raw/datasets.json."""
    data = json.loads(RAW_DATASETS.read_text(encoding="utf-8"))
    return {str(item["id"]): item.get("category", "") for item in data["datasets"]}


def main() -> None:
    doc_cat = load_doc_category()
    r = Retriever()
    k = TOP_K

    hits = 0
    reciprocal_ranks = 0.0
    print(f"=== Оценка retrieval (k={k}, вопросов: {len(GOLD)}) ===\n")

    for question, expected in GOLD:
        results = r.search(question, k=k)
        rank = None
        for idx, hit in enumerate(results, 1):
            if doc_cat.get(hit["doc_id"]) == expected:
                rank = idx
                break
        if rank:
            hits += 1
            reciprocal_ranks += 1.0 / rank
        mark = f"hit@{rank}" if rank else "MISS"
        top_cat = doc_cat.get(results[0]["doc_id"], "?") if results else "?"
        print(f"[{mark:7}] {expected:24} | top1={top_cat:24} | «{question}»")

    n = len(GOLD)
    print("\n=== Итог ===")
    print(f"hit@{k}: {hits}/{n} = {hits / n:.2f}")
    print(f"MRR:    {reciprocal_ranks / n:.3f}")


if __name__ == "__main__":
    main()
