"""Небольшие текстовые утилиты для UI (вынесены отдельно ради тестируемости)."""

import html
import re


def highlight(text: str, query: str) -> str:
    """Оборачивает слова запроса (длиной 3+) в <mark> внутри HTML-экранированного текста."""
    words = sorted(
        {w for w in re.findall(r"\w+", query.lower()) if len(w) >= 3},
        key=len,
        reverse=True,
    )
    escaped = html.escape(text)
    for w in words:
        escaped = re.sub(f"(?i)({re.escape(w)})", r"<mark>\1</mark>", escaped)
    return escaped.replace("\n", "<br>")
