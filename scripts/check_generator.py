"""Проверка demo-ответа: 3 рабочих вопроса + 1 negative (отказ)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.generator import ask


def show(label: str, question: str) -> None:
    print(f"\n--- {label}: «{question}» ---")
    result = ask(question)
    print(f"Ответ:\n{result['answer'][:400]}\n")
    print(f"Источников: {len(result['sources'])}")
    for i, src in enumerate(result["sources"], 1):
        print(f"  [{i}] doc_id={src['doc_id']}, score={src['score']:.4f}, name={src['name'][:55]}")


if __name__ == "__main__":
    show("Есть контекст (crypto)", "encryption public key cryptography")
    show("Есть контекст (space)", "NASA space shuttle orbit launch")
    show("Есть контекст (hockey)", "hockey playoff game season")
    show("Negative", "best recipe for borscht soup")
