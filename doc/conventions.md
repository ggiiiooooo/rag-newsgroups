# Соглашения

## Структура кода

- `app/` — библиотека (импортируемые модули, без сайд-эффектов на импорте).
- `scripts/` — точки входа (CLI), каждый запускается через `uv run python scripts/<name>.py`.
- `tests/` — pytest, изолированные фикстуры (свой mini-index во временной папке).
- `doc/` — планирование и описание данных.
- `data/` — `raw/` (вход, коммитится), `processed/` и `index/` (генерируются, в `.gitignore`).

## Формат данных

| Артефакт | Формат | Ключи |
|----------|--------|-------|
| `datasets.json` | JSON `{"datasets": [...]}` | `id`, `name`, `text`, `category` |
| `documents.jsonl` | JSONL | `doc_id`, `name`, `text`, `category`, `source_file` |
| `chunks.jsonl` | JSONL | `chunk_id`, `doc_id`, `name`, `text` |

- `doc_id` — строка (`str(id)`).
- `chunk_id` — `"{doc_id}_{i}"`.
- Все файлы в UTF-8, `ensure_ascii=False`.

## Параметры (единый источник — `app/config.py`)

- `TOP_K = 5`, `CHUNK_MAX_CHARS = 600`, `CHUNK_OVERLAP = 80`.
- Порог отказа — `MIN_SCORE` в `app/prompts.py`.
- Менять параметры **только** в этих файлах, не хардкодить в логике.

## Код

- Python 3.10+, type hints в сигнатурах публичных функций.
- Докстринги — на русском, кратко (что делает функция).
- Чистые функции отделены от I/O (например, `chunk_text` не читает файлы).
- Без внешних сетевых вызовов в `app/` и в тестах (сеть — только в `prepare_datasets.py`).

## Тесты

- Не зависят от собранного индекса: строят свой mini-index в `tmp_path`.
- Каждый тест проверяет одно поведение; имена `test_<что>_<ожидание>`.
- Перед коммитом: `uv run pytest tests/ -q` должен быть зелёным.

## Git

- `datasets.json` коммитится (pipeline воспроизводим офлайн).
- Индекс и `*.jsonl` в `data/processed` — не коммитятся (генерируются).
