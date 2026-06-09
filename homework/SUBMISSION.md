# Submission

## Ссылка на репозиторий с заданием

- Repo URL: `<ВСТАВЬТЕ ссылку на ваш GitHub-репозиторий>`

> Этот файл нужно добавить в папку `homework/` через **Pull Request** в репозиторий
> курса [MaratNotes/rag-tutorial](https://github.com/MaratNotes/rag-tutorial).
> Без PR и `homework/SUBMISSION.md` задание считается не сданным.

## Автор

- ФИО / ник: georgiy

## Данные

- **Источник:** [20 Newsgroups](http://qwone.com/~jason/20Newsgroups/) (через scikit-learn).
- **Объём:** 1200 записей в `data/raw/datasets.json`, 3879 чанков после нарезки (оба > 1000).
- **Что индексируется:** поле `text` постов; `name`/`category`/`doc_id` — метаданные.
- Подробно: [doc/DATA.md](../doc/DATA.md).

## Что реализовано

Полный pipeline: `prepare_datasets → ingest → chunking → index → retrieval → demo-answer → UI`.

- **3 demo-вопроса с ответом и источниками:**
  - `encryption keys and public key cryptography` → `sci.crypt` (score ≈ 0.29)
  - `NASA space shuttle orbit launch` → `sci.space` (score ≈ 0.39)
  - `hockey playoff game season` → `rec.sport.hockey` (score ≈ 0.28)
- **1 negative-вопрос с отказом:**
  - `best recipe for borscht soup` → «В базе не найдено релевантных фрагментов» (max score ≈ 0.18 < порога 0.22)
- **Тесты:** 17 шт., все зелёные (`uv run pytest tests/ -q`).
- **Планирование:** `doc/00_project_idea.md`, `vision.md`, `conventions.md`, `tasklist.md`, `workflow.md` + `DATA.md`.

## Реализованные улучшения

1. **Eval:** `scripts/eval_retrieval.py` — `hit@5 = 1.00`, `MRR = 0.95`.
2. **UI:** ползунок порога `min_score`, выбор `top-k`, подсветка слов запроса.
3. **TF-IDF tuning:** english stop-words, биграммы, `sublinear_tf`.

Подробно: [homework/IMPROVEMENTS.md](IMPROVEMENTS.md).

## Запуск

```bash
uv sync
uv run python scripts/build_index.py
uv run streamlit run app/main.py
```
