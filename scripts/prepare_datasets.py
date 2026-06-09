"""Подготовка корпуса: 20 Newsgroups (sklearn) → data/raw/datasets.json.

Скачивает датасет 20 Newsgroups (~18k постов, 20 тематических групп) через
scikit-learn, очищает технические заголовки/цитаты и сохраняет
сбалансированную выборку в формате {id, name, text, category}.

Запуск:
    uv run python scripts/prepare_datasets.py
    uv run python scripts/prepare_datasets.py --per-category 50

Требует интернет при первом запуске (sklearn кэширует данные в ~/scikit_learn_data).
Готовый datasets.json уже закоммичен — пересборка нужна только если хотите
изменить состав/объём корпуса.
"""

import argparse
import json
import re
from pathlib import Path

from sklearn.datasets import fetch_20newsgroups

ROOT = Path(__file__).resolve().parent.parent
OUT_JSON = ROOT / "data" / "raw" / "datasets.json"

# Минимальная длина «полезного» текста поста (после очистки)
MIN_TEXT_LEN = 200
# Сколько постов на каждую из 20 групп берём по умолчанию (20 * 60 = 1200 записей)
DEFAULT_PER_CATEGORY = 60


def extract_subject(raw: str) -> str:
    """Достаёт тему письма (Subject:) из заголовка поста, если она есть."""
    m = re.search(r"^Subject:\s*(.+)$", raw, flags=re.MULTILINE)
    if not m:
        return ""
    subject = m.group(1).strip()
    subject = re.sub(r"^(Re:\s*)+", "", subject, flags=re.IGNORECASE).strip()
    return subject[:120]


def clean_body(raw: str) -> str:
    """Текст поста без служебного заголовка и строк-цитат (`> ...`)."""
    # Тело письма идёт после первой пустой строки (конец заголовка)
    parts = raw.split("\n\n", 1)
    body = parts[1] if len(parts) == 2 else raw
    lines = [ln for ln in body.splitlines() if not ln.lstrip().startswith(">")]
    body = "\n".join(lines)
    body = re.sub(r"[ \t]+", " ", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def build_records(per_category: int) -> list[dict]:
    # remove=('footers', 'quotes') убирает подписи и блоки цитирования,
    # заголовки оставляем, чтобы достать Subject для человекочитаемого name.
    bunch = fetch_20newsgroups(
        subset="train",
        remove=("footers", "quotes"),
        shuffle=True,
        random_state=42,
    )
    categories = bunch.target_names
    per_cat_count = {c: 0 for c in categories}
    records: list[dict] = []

    for raw, target in zip(bunch.data, bunch.target):
        category = categories[target]
        if per_cat_count[category] >= per_category:
            continue
        body = clean_body(raw)
        if len(body) < MIN_TEXT_LEN:
            continue
        subject = extract_subject(raw)
        name = f"{category} — {subject}" if subject else f"{category} — пост #{len(records)}"
        records.append({"name": name, "text": body, "category": category})
        per_cat_count[category] += 1
        if all(v >= per_category for v in per_cat_count.values()):
            break

    for i, item in enumerate(records):
        item["id"] = i
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Подготовка корпуса 20 Newsgroups")
    parser.add_argument(
        "--per-category",
        type=int,
        default=DEFAULT_PER_CATEGORY,
        help=f"Сколько постов на группу (по умолчанию {DEFAULT_PER_CATEGORY})",
    )
    args = parser.parse_args()

    records = build_records(args.per_category)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps({"datasets": records}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {len(records)} records to {OUT_JSON}")


if __name__ == "__main__":
    main()
