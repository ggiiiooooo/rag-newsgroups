# RAG · 20 Newsgroups

Учебный RAG на текстовых постах **20 Newsgroups**: TF-IDF + demo-ответ с источниками.
Pipeline: данные → документы → чанки → индекс → поиск → ответ.

Повторение пайплайна репозитория-образца [MaratNotes/rag-tutorial](https://github.com/MaratNotes/rag-tutorial) на собственных данных.

**Документы разработки:** [doc/tasklist.md](doc/tasklist.md) · **Данные:** [doc/DATA.md](doc/DATA.md) · **Улучшения:** [homework/IMPROVEMENTS.md](homework/IMPROVEMENTS.md) · **Сдача:** [homework/SUBMISSION.md](homework/SUBMISSION.md)

## Требования

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

## Быстрый старт

```bash
# 1. Окружение и зависимости
uv sync

# 2. Сборка индекса (ingest + chunk + TF-IDF)
uv run python scripts/build_index.py

# 3. Запуск UI
uv run streamlit run app/main.py
```

Откройте в браузере: http://localhost:8501

> `data/raw/datasets.json` (1200 записей) уже закоммичен — шаг 2 работает офлайн.
> Чтобы пересобрать корпус из 20 Newsgroups: `uv run python scripts/prepare_datasets.py`
> (требует интернет при первом запуске, кэшируется в `~/scikit_learn_data`).

## Данные

Корпус — **1200 постов** из датасета [20 Newsgroups](http://qwone.com/~jason/20Newsgroups/)
(60 постов × 20 тематических групп), скачивается через scikit-learn. После нарезки — **3879 чанков**.
Подробности: [doc/DATA.md](doc/DATA.md).

## Demo-вопросы

В sidebar приложения или в поле ввода (вопросы на английском — корпус англоязычный):

| Вопрос | Ожидание |
|--------|----------|
| **encryption keys and public key cryptography** | ответ, тема `sci.crypt`, score ≈ 0.29 |
| **NASA space shuttle orbit launch** | ответ, тема `sci.space`, score ≈ 0.39 |
| **hockey playoff game season** | ответ, тема `rec.sport.hockey`, score ≈ 0.28 |
| **best recipe for borscht soup** | **отказ** — темы еды нет в корпусе (negative-case) |

Другие рабочие запросы: `baseball pitcher batting average`, `car engine dealer prices`,
`gun control second amendment`, `christian faith and god`.

### Логи demo-проверки

Ниже — реальный вывод (полностью в [doc/demo_log.txt](doc/demo_log.txt)):

```
=== Оценка retrieval (k=5, вопросов: 10) ===
[hit@1  ] sci.crypt        | top1=sci.crypt        | «public key encryption and cryptography»
[hit@1  ] sci.space        | top1=sci.space        | «NASA space shuttle launch into orbit»
[hit@1  ] rec.sport.hockey | top1=rec.sport.hockey | «hockey playoff game and the season»
...
hit@5: 10/10 = 1.00
MRR:    0.950
```

```
--- Negative: «best recipe for borscht soup» ---
Ответ:
В базе не найдено релевантных фрагментов. Ответить по данным невозможно.
Источников: 5   (все со score < 0.22 — порог релевантности)
```

## Проверка из консоли

```bash
# Тесты (17 шт.)
uv run pytest tests/ -v

# Поиск
uv run python scripts/check_retrieval.py

# Demo-ответ (3 ответа + 1 отказ)
uv run python scripts/check_generator.py

# Оценка качества retrieval (hit@k, MRR) — реализованное улучшение
uv run python scripts/eval_retrieval.py
```

## Структура проекта

```
rag-tutorial/
├── app/
│   ├── config.py       # пути, top_k, размер чанка
│   ├── chunker.py      # нарезка текста на чанки
│   ├── retriever.py    # TF-IDF + cosine top-k
│   ├── generator.py    # demo-ответ + отказ
│   ├── prompts.py      # правила и порог MIN_SCORE
│   ├── textutils.py    # подсветка слов запроса (UI)
│   └── main.py         # Streamlit UI
├── scripts/
│   ├── prepare_datasets.py  # 20 Newsgroups -> datasets.json
│   ├── ingest.py            # datasets.json -> documents.jsonl
│   ├── build_index.py       # ingest + chunk + TF-IDF
│   ├── check_retrieval.py
│   ├── check_generator.py
│   └── eval_retrieval.py    # hit@k / MRR
├── data/
│   ├── raw/datasets.json    # корпус (коммитится)
│   ├── processed/           # documents.jsonl, chunks.jsonl (генерируются)
│   └── index/               # vectorizer.pkl, matrix.npz (генерируются)
├── tests/                   # 17 тестов
└── doc/                     # планирование + DATA.md + логи
```

## Как работает pipeline (от идеи до ответа)

1. **prepare_datasets.py** — берём 20 Newsgroups, чистим заголовки/цитаты, сохраняем `datasets.json` (`id`, `name`, `text`, `category`).
2. **ingest.py** — нормализуем текст, присваиваем `doc_id` → `documents.jsonl`.
3. **chunker.py** — режем по абзацам (≤ 600 символов, overlap 80) → `chunks.jsonl`.
4. **build_index.py** — TF-IDF (english stop-words, n-граммы 1–2) → `vectorizer.pkl` + `matrix.npz`.
5. **retriever.py** — векторизуем запрос, cosine similarity, top-k чанков.
6. **generator.py** — собираем ответ только из чанков со `score ≥ MIN_SCORE`; иначе **отказ**.
7. **main.py** — Streamlit показывает фрагменты (`doc_id`, `score`, текст), ответ и источники.

## Реализованные улучшения

См. [homework/IMPROVEMENTS.md](homework/IMPROVEMENTS.md). В коде реализованы:

- **Оценка качества (Eval):** `scripts/eval_retrieval.py` — метрики `hit@k` и `MRR` на 10 эталонных вопросах (текущий результат: `hit@5 = 1.00`, `MRR = 0.95`).
- **UI:** ползунок порога `min_score`, выбор `top-k` и подсветка совпавших слов запроса в фрагментах.
- **Качество retrieval:** TF-IDF с english stop-words, биграммами и `sublinear_tf`.

## Ограничения MVP

- Поиск по **словам** (TF-IDF), не по смыслу — синонимы могут не находиться.
- Demo-режим: ответ из найденных чанков, без внешней LLM.
- Порог `MIN_SCORE = 0.22` подобран эмпирически под этот корпус (см. `app/prompts.py`).
