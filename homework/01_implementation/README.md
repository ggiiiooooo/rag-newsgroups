# Фаза 01 · Реализация

Итерации реализации pipeline. План и карта «файл → итерация» —
в [../../doc/tasklist.md](../../doc/tasklist.md).

| Итерация | Что сделано | Файлы |
|----------|-------------|-------|
| 00 scaffold | структура, `pyproject.toml`, `config.py` | каркас |
| 01 demo-data | 20 Newsgroups → `datasets.json` (1200) | `scripts/prepare_datasets.py` |
| 02 ingestion | `datasets.json` → `documents.jsonl` | `scripts/ingest.py` |
| 03 chunking | абзацы ≤600 / overlap 80 → 3879 чанков | `app/chunker.py` |
| 04 index | TF-IDF fit + save | `scripts/build_index.py` |
| 05 retrieval | cosine top-k | `app/retriever.py` |
| 06 demo-answer | ответ из чанков + отказ по порогу | `app/generator.py`, `app/prompts.py` |
| 07 streamlit UI | фрагменты, ответ, источники | `app/main.py`, `app/textutils.py` |
| 08 tests + readme | 17 тестов, README | `tests/`, `README.md` |
| 09 improvements | eval (hit@k/MRR), UI-порог, подсветка | `scripts/eval_retrieval.py` |

## Результаты прогона

- `build_index.py`: документов 1200, чанков 3879, матрица (3879, ~29000).
- `eval_retrieval.py`: `hit@5 = 1.00`, `MRR = 0.95`.
- `pytest`: 17 passed.
- Полные логи: [../../doc/demo_log.txt](../../doc/demo_log.txt).
