"""Свой дополнительный тест: подсветка слов запроса в UI (улучшение из IMPROVEMENTS.md)."""

from app.textutils import highlight


def test_highlight_wraps_query_words():
    out = highlight("NASA space shuttle orbit", "space orbit")
    assert "<mark>space</mark>" in out
    assert "<mark>orbit</mark>" in out


def test_highlight_is_case_insensitive():
    out = highlight("Public Key Encryption", "encryption")
    assert "<mark>Encryption</mark>" in out


def test_highlight_escapes_html_and_keeps_text():
    out = highlight("a <b> tag & more", "tag")
    # исходный угловой скобки экранируется, инъекции нет
    assert "&lt;b&gt;" in out
    assert "<mark>tag</mark>" in out


def test_highlight_skips_short_words():
    # слова короче 3 символов не подсвечиваются (иначе шум)
    out = highlight("an ox is here", "is ox")
    assert "<mark>" not in out
