# Vision · стек и архитектура

## Цель

Воспроизводимый offline-RAG: вопрос → top-k фрагментов → ответ с источниками либо отказ.

## Архитектура (поток данных)

```
20 Newsgroups (sklearn)
        │  prepare_datasets.py
        ▼
data/raw/datasets.json        {id, name, text, category}
        │  ingest.py            (нормализация, doc_id)
        ▼
data/processed/documents.jsonl
        │  chunker.py           (абзацы, ≤600 симв., overlap 80)
        ▼
data/processed/chunks.jsonl
        │  build_index.py       (TF-IDF fit)
        ▼
data/index/{vectorizer.pkl, matrix.npz, chunks.jsonl}
        │  retriever.py         (cosine top-k)
        ▼
generator.py  →  ответ + источники  /  отказ (score < MIN_SCORE)
        │
        ▼
app/main.py (Streamlit UI)
```

## Стек

| Слой | Технология | Почему |
|------|-----------|--------|
| Подготовка данных | scikit-learn (`fetch_20newsgroups`) | открытый датасет без ключей |
| Хранение | JSON / JSONL + файлы индекса | просто, прозрачно, версионируется |
| Векторизация | `TfidfVectorizer` (1–2-граммы, english stop-words) | без обучения эмбеддингов |
| Поиск | cosine similarity (sklearn) | стандарт для TF-IDF |
| Ответ | сборка из чанков (demo-режим) | без внешней LLM |
| UI | Streamlit | быстрый интерактив, показ источников |
| Тесты | pytest | изолированные mini-index фикстуры |
| Менеджер | uv | воспроизводимое окружение |

## Ключевые решения

- **Чанк = абзацы до 600 символов с overlap 80.** Посты короткие; такой размер
  обычно даёт 1–4 чанка на пост и сохраняет контекст между ними.
- **Порог релевантности `MIN_SCORE = 0.22`.** Подобран эмпирически: релевантные
  запросы дают top-score ~0.28–0.39, нерелевантные (еда) — не выше ~0.19.
- **`category` хранится, но не индексируется** — используется только для оценки качества.

## Границы MVP

В MVP нет: embeddings, LLM, векторной БД, reranking, hybrid search. Все они описаны
как направления развития в [../homework/IMPROVEMENTS.md](../homework/IMPROVEMENTS.md).
