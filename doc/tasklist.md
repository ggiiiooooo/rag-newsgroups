# Tasklist · итерационный план

Статус: ✅ выполнено.

| # | Итерация | Артефакт | Статус |
|---|----------|----------|:------:|
| 0 | Scaffold: структура папок, `pyproject.toml`, `config.py` | каркас | ✅ |
| 1 | Подготовка данных: `prepare_datasets.py` (20 Newsgroups → `datasets.json`, 1200 записей) | `data/raw/datasets.json` | ✅ |
| 2 | Ingestion: `ingest.py` (`datasets.json` → `documents.jsonl`) | `documents.jsonl` | ✅ |
| 3 | Chunking: `chunker.py` (абзацы, ≤600, overlap 80 → 3879 чанков) | `chunks.jsonl` | ✅ |
| 4 | Index: `build_index.py` (TF-IDF fit + save) | `vectorizer.pkl`, `matrix.npz` | ✅ |
| 5 | Retrieval: `retriever.py` (cosine top-k) + `check_retrieval.py` | `Retriever` | ✅ |
| 6 | Demo-ответ: `generator.py` + `prompts.py` (отказ по порогу) + `check_generator.py` | ответ/отказ | ✅ |
| 7 | UI: `app/main.py` (Streamlit: фрагменты, ответ, источники) | приложение | ✅ |
| 8 | Тесты + README | 17 тестов, README | ✅ |
| 9 | Улучшение: `eval_retrieval.py` (hit@k, MRR) + UI-порог + подсветка | метрики, UX | ✅ |

## Карта файлов → итерации

- Итерация 1 → `scripts/prepare_datasets.py`
- Итерация 2 → `scripts/ingest.py`
- Итерация 3 → `app/chunker.py`, `tests/test_chunking.py`
- Итерация 4 → `scripts/build_index.py`
- Итерация 5 → `app/retriever.py`, `scripts/check_retrieval.py`, `tests/test_retrieval.py`
- Итерация 6 → `app/generator.py`, `app/prompts.py`, `scripts/check_generator.py`
- Итерация 7 → `app/main.py`, `app/textutils.py`
- Итерация 9 → `scripts/eval_retrieval.py`, `tests/test_extra.py`

## Definition of Done

- `uv run python scripts/build_index.py` собирает индекс из закоммиченного `datasets.json`.
- `uv run streamlit run app/main.py` показывает фрагменты с `doc_id` и score.
- 3 demo-вопроса дают ответ, negative-вопрос даёт отказ.
- `uv run pytest tests/ -q` — зелёный.
