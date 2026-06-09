# Workflow · как прогонять pipeline

## Полный прогон с нуля

```bash
uv sync                                    # окружение
uv run python scripts/prepare_datasets.py  # (опц.) пересобрать datasets.json из 20 Newsgroups
uv run python scripts/build_index.py       # ingest + chunk + TF-IDF
uv run streamlit run app/main.py           # UI на http://localhost:8501
```

`datasets.json` уже в репозитории, поэтому шаг `prepare_datasets.py` можно пропустить —
`build_index.py` работает офлайн.

## Отдельные шаги (для отладки)

```bash
uv run python scripts/ingest.py            # datasets.json -> documents.jsonl
uv run python -m app.chunker               # documents.jsonl -> chunks.jsonl
uv run python scripts/check_retrieval.py   # ручная проверка поиска
uv run python scripts/check_generator.py   # 3 ответа + 1 отказ
uv run python scripts/eval_retrieval.py    # метрики hit@k, MRR
```

## Тесты

```bash
uv run pytest tests/ -q     # быстрый прогон
uv run pytest tests/ -v     # подробный
```

## Цикл изменения данных

1. Поправить объём/состав в `scripts/prepare_datasets.py` (или флаг `--per-category`).
2. `uv run python scripts/prepare_datasets.py`
3. `uv run python scripts/build_index.py` — **обязательно** пересобрать индекс.
4. Перезапустить Streamlit (он кэширует `Retriever` через `@st.cache_resource`).

## Цикл изменения параметров

- Размер чанка / overlap / top_k → `app/config.py` → пересобрать индекс.
- Порог отказа `MIN_SCORE` → `app/prompts.py` → индекс пересобирать **не нужно**
  (порог применяется на этапе ответа), достаточно перезапустить UI.

## Типичные проблемы

| Симптом | Причина | Решение |
|---------|---------|---------|
| `Индекс не найден` | не собран индекс | `uv run python scripts/build_index.py` |
| Negative-вопрос даёт ответ | низкий `MIN_SCORE` | поднять порог в `app/prompts.py` |
| Изменения данных не видны в UI | кэш `Retriever` | перезапустить Streamlit |
