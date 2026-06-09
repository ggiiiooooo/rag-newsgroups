"""Проверка retrieval — понятный консольный вывод."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.retriever import Retriever


def print_hit(i: int, hit: dict) -> None:
    preview = hit["text"][:120].replace("\n", " ")
    print(f"  [{i}] doc_id={hit['doc_id']}, score={hit['score']:.4f}")
    print(f"      {hit['name'][:70]}")
    print(f"      {preview}...")


def main() -> None:
    print("=== Проверка Retriever ===\n")

    r = Retriever()
    print("OK: индекс загружен (vectorizer.pkl + matrix.npz + chunks.jsonl)\n")

    queries = [
        ("encryption public key cryptography", "тема sci.crypt -> score > 0"),
        ("NASA space shuttle orbit", "тема sci.space -> score > 0"),
        ("best recipe for borscht soup", "темы нет в корпусе -> низкий score"),
    ]

    for query, hint in queries:
        print(f"Запрос: «{query}»")
        print(f"Ожидание: {hint}")
        results = r.search(query, k=3)
        print(f"Получено результатов: {len(results)}")
        for i, hit in enumerate(results, 1):
            print_hit(i, hit)
        print()

    print("=== Итог ===")
    print("Если видите результаты с полями doc_id / score / text — retrieval работает.")


if __name__ == "__main__":
    main()
