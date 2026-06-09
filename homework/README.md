# Homework

Материалы домашнего задания.

- [SUBMISSION.md](SUBMISSION.md) — файл сдачи (ссылка на репозиторий, что сделано).
- [IMPROVEMENTS.md](IMPROVEMENTS.md) — направления улучшений + что реализовано.
- [00_planning/](00_planning/) — фаза планирования (5 шагов).
- [01_implementation/](01_implementation/) — фаза реализации (итерации).

## Чек-лист сдачи

- [x] Репозиторий с рабочим pipeline (ingest → chunking → index → retrieval → demo-answer → UI).
- [x] README с инструкцией запуска (`uv sync` → `build_index.py` → `streamlit`).
- [x] Описание данных ([../doc/DATA.md](../doc/DATA.md)).
- [x] 3 demo-вопроса с ответами + 1 negative-вопрос с отказом.
- [x] Тесты зелёные (17 шт.).
- [x] Реализовано ≥ 1 улучшение (Eval, UI, TF-IDF tuning).
- [ ] PR в [MaratNotes/rag-tutorial](https://github.com/MaratNotes/rag-tutorial) с этим `SUBMISSION.md` (выполняется студентом).
