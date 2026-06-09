# Данные и назначение репозитория

Документ описывает, **какие данные** использует учебный RAG, **откуда** они взяты
и **что именно** попадает в индекс.

---

## Назначение репозитория

**Для кого:** студенты, которые повторяют RAG-pipeline на собственных данных.

**Что демонстрирует:**

- полный offline-pipeline: сырые данные → документы → чанки → TF-IDF индекс → поиск → demo-ответ;
- ответ **только по найденным фрагментам** с указанием источника (`doc_id`, score);
- явный **отказ**, если релевантного контекста нет (negative-case);
- Streamlit UI для интерактивной проверки;
- автоматическую оценку retrieval (`hit@k`, `MRR`).

**Границы MVP:**

- поиск по **словам** (TF-IDF), не embeddings и не LLM;
- demo-режим без внешних API;
- локальный корпус 1200 документов / 3879 чанков;
- не production-система, а **учебный шаблон**.

---

## Источник данных

| Источник | Файл в проекте | Комментарий |
|----------|----------------|-------------|
| [20 Newsgroups](http://qwone.com/~jason/20Newsgroups/) (через [scikit-learn](https://scikit-learn.org/stable/datasets/real_world.html#newsgroups-dataset)) | `~/scikit_learn_data/` | ~18000 постов, 20 групп. Скачивается scikit-learn при первом запуске `prepare_datasets.py`, кэшируется локально. **Не коммитится.** |
| Подготовленный корпус | `data/raw/datasets.json` | 1200 записей: `id`, `name`, `text`, `category`. **Коммитится** — готовый набор, pipeline работает офлайн. |
| Скрипт подготовки | `scripts/prepare_datasets.py` | Выборка 60 постов × 20 групп, очистка заголовков и цитат. |

**О датасете:** 20 Newsgroups — классический бенчмарк для классификации текстов:
~18k сообщений из 20 тематических групп Usenet (наука, спорт, политика, техника, религия).

**Лицензия:** датасет распространяется свободно для исследовательских/учебных целей
(см. страницу [20 Newsgroups](http://qwone.com/~jason/20Newsgroups/) и документацию scikit-learn).

**Дата подготовки:** июнь 2026 (`random_state=42`, выборка детерминирована и воспроизводима).

---

## Что индексируем

| Поле / артефакт | Индексируется? | Где используется |
|-----------------|:--------------:|------------------|
| `text` из `datasets.json` | **Да** | TF-IDF матрица, поиск, demo-ответ |
| `name` (группа + Subject) | Нет (метаданные) | UI, источники — подпись документа |
| `category` (группа) | Нет (метаданные) | оценка качества `eval_retrieval.py` |
| `doc_id` | Нет (метаданные) | UI, источники — идентификатор записи |
| `source_file` | Нет | `documents.jsonl`, трассировка происхождения |

**Pipeline:**

```
datasets.json → documents.jsonl → chunks.jsonl → vectorizer.pkl + matrix.npz
```

- **Чанки:** нарезка по абзацам, max 600 символов, overlap 80 (`app/chunker.py`).
- **Поиск:** cosine similarity по TF-IDF (english stop-words, n-граммы 1–2) (`app/retriever.py`).

---

## Что НЕ индексируем

| Не индексируется | Причина |
|------------------|---------|
| Сырой кэш scikit-learn | Только для подготовки `datasets.json` |
| Технические заголовки писем, блоки цитат (`>`) | Удаляются в `prepare_datasets.py` как шум |
| `category` / `name` / `doc_id` | Метаданные, не часть поискового текста |
| `data/processed/*.jsonl`, `data/index/*` | Промежуточные артефакты, пересобираются скриптами |
| Секреты, API-ключи | Demo-режим без внешних LLM |

---

## Состав корпуса

1200 документов (`doc_id` 0…1199), по 60 на каждую из 20 групп:

| Раздел | Группы |
|--------|--------|
| comp.* | graphics, os.ms-windows.misc, sys.ibm.pc.hardware, sys.mac.hardware, windows.x |
| rec.* | autos, motorcycles, sport.baseball, sport.hockey |
| sci.* | crypt, electronics, med, space |
| talk.* | politics.guns, politics.mideast, politics.misc, religion.misc |
| прочее | alt.atheism, misc.forsale, soc.religion.christian |

**Рабочие demo-запросы** (даёт ответ с источниками):
`encryption keys cryptography` → `sci.crypt`,
`NASA space shuttle orbit` → `sci.space`,
`hockey playoff game` → `rec.sport.hockey`.

**Negative-запрос** `best recipe for borscht soup` → **отказ**: кулинарной темы
в корпусе нет, максимальный score (~0.18) ниже порога `MIN_SCORE = 0.22`.

---

## Объём (для критерия оценки)

| Метрика | Значение |
|---------|---------:|
| Записей в источнике (`datasets.json`) | **1200** |
| Чанков после нарезки | **3879** |
| Размер TF-IDF словаря | ~29000 |

Оба показателя превышают 1000 → соответствует уровню **«отлично»**.

---

## Как обновить / изменить данные

```bash
# изменить объём (по умолчанию 60 на группу = 1200 записей)
uv run python scripts/prepare_datasets.py --per-category 100

# пересобрать индекс
uv run python scripts/build_index.py
```

---

## Связанные документы

- [00_project_idea.md](00_project_idea.md) — идея и целевые данные
- [vision.md](vision.md) — стек и границы MVP
- [conventions.md](conventions.md) — соглашения по коду и данным
- [tasklist.md](tasklist.md) — итерационный план
- [workflow.md](workflow.md) — как прогонять pipeline
