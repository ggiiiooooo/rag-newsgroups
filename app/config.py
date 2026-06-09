from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_INDEX = ROOT / "data" / "index"

RAW_DATASETS = DATA_RAW / "datasets.json"
DOCUMENTS_JSONL = DATA_PROCESSED / "documents.jsonl"
CHUNKS_JSONL = DATA_PROCESSED / "chunks.jsonl"

VECTORIZER_PKL = DATA_INDEX / "vectorizer.pkl"
MATRIX_NPZ = DATA_INDEX / "matrix.npz"
INDEX_CHUNKS_JSONL = DATA_INDEX / "chunks.jsonl"

# Сколько фрагментов возвращает retriever
TOP_K = 5
# Нарезка: целевой размер чанка и overlap между соседними чанками (в символах)
CHUNK_MAX_CHARS = 600
CHUNK_OVERLAP = 80
