"""Тесты нарезки текста на чанки."""

from app.chunker import chunk_document, chunk_text, run


def test_chunk_text_respects_max_size():
    text = "First paragraph.\n\n" + "word " * 400
    chunks = chunk_text(text, max_chars=400, overlap=50)
    assert chunks
    assert all(len(c) <= 400 for c in chunks)


def test_chunk_text_splits_by_paragraphs():
    text = "First paragraph about encryption.\n\nSecond paragraph about orbit."
    chunks = chunk_text(text, max_chars=400, overlap=50)
    assert len(chunks) == 1
    assert "encryption" in chunks[0]
    assert "orbit" in chunks[0]


def test_chunk_text_overlap_between_chunks():
    para1 = "A" * 300
    para2 = "B" * 300
    text = f"{para1}\n\n{para2}"
    chunks = chunk_text(text, max_chars=400, overlap=50)
    assert len(chunks) >= 2
    assert chunks[1].startswith(chunks[0][-50:])


def test_chunk_text_empty_returns_empty():
    assert chunk_text("   ") == []


def test_chunk_document_has_doc_id():
    doc = {
        "doc_id": "42",
        "name": "sci.space — Shuttle",
        "text": "Variables: year, orbit, altitude.",
    }
    chunks = chunk_document(doc)
    assert len(chunks) == 1
    assert chunks[0]["doc_id"] == "42"
    assert chunks[0]["chunk_id"] == "42_0"
    assert chunks[0]["name"] == "sci.space — Shuttle"


def test_run_creates_chunks_jsonl(tmp_path):
    docs = tmp_path / "documents.jsonl"
    docs.write_text(
        '{"doc_id": "0", "name": "A", "text": "Short text."}\n',
        encoding="utf-8",
    )
    out = tmp_path / "chunks.jsonl"
    count = run(input_path=docs, output_path=out)
    assert count == 1
    assert out.exists()
    line = out.read_text(encoding="utf-8").strip()
    assert '"doc_id": "0"' in line
