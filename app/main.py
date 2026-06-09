"""Streamlit UI: вопрос -> фрагменты -> ответ -> источники.

Улучшения относительно базового MVP (см. homework/IMPROVEMENTS.md):
- ползунок порога score (min_score) прямо в интерфейсе;
- подсветка совпавших слов запроса в найденных фрагментах.
"""

import streamlit as st

from app.config import INDEX_CHUNKS_JSONL, MATRIX_NPZ, TOP_K, VECTORIZER_PKL
from app.generator import ask
from app.prompts import MIN_SCORE
from app.retriever import Retriever
from app.textutils import highlight

DEMO_QUESTIONS = [
    "encryption keys and public key cryptography",   # sci.crypt
    "NASA space shuttle orbit launch",               # sci.space
    "hockey playoff game season",                    # rec.sport.hockey
    "best recipe for borscht soup",                  # negative -> отказ
]


def index_exists() -> bool:
    return all(p.exists() for p in (VECTORIZER_PKL, MATRIX_NPZ, INDEX_CHUNKS_JSONL))


@st.cache_resource
def load_retriever() -> Retriever:
    return Retriever()


def render_chunk(i: int, src: dict, query: str, min_score: float, expanded: bool) -> None:
    label = f"[{i}] doc_id={src['doc_id']} · score={src['score']:.4f}"
    with st.expander(label, expanded=expanded):
        st.markdown(f"**{src['name']}**")
        if src["score"] < min_score:
            st.caption("⚠️ ниже порога релевантности — в ответ не попадает")
        st.markdown(highlight(src["text"], query), unsafe_allow_html=True)


def render_fragments(sources: list[dict], query: str, min_score: float) -> None:
    st.subheader("Найденные фрагменты (top-k)")
    if not sources:
        st.info("Фрагменты не найдены.")
        return
    for i, src in enumerate(sources, 1):
        render_chunk(i, src, query, min_score, expanded=src["score"] >= min_score)


def render_sources(sources: list[dict], query: str, min_score: float) -> None:
    st.subheader("Источники")
    relevant = [s for s in sources if s["score"] >= min_score]
    if not relevant:
        st.info("Источники отсутствуют (нет фрагментов выше порога).")
        return
    for i, src in enumerate(relevant, 1):
        render_chunk(i, src, query, min_score, expanded=False)


def main() -> None:
    st.set_page_config(page_title="RAG · 20 Newsgroups", layout="wide")
    st.title("RAG · 20 Newsgroups")
    st.caption("Учебный RAG: TF-IDF + demo-ответ с источниками")

    if not index_exists():
        st.error(
            "Индекс не собран. Сначала выполните:\n\n"
            "`uv run python scripts/build_index.py`"
        )
        st.stop()

    st.sidebar.header("Demo-вопросы")
    for q in DEMO_QUESTIONS:
        if st.sidebar.button(q, use_container_width=True):
            st.session_state["question"] = q

    st.sidebar.header("Параметры")
    min_score = st.sidebar.slider(
        "Порог релевантности (min_score)",
        min_value=0.0,
        max_value=0.5,
        value=float(MIN_SCORE),
        step=0.01,
        help="Фрагменты со score ниже порога считаются нерелевантными и дают отказ.",
    )
    top_k = st.sidebar.slider("Сколько фрагментов (top-k)", 1, 10, TOP_K)

    question = st.text_input("Ваш вопрос", key="question")

    if st.button("Спросить", type="primary"):
        if not question.strip():
            st.warning("Введите вопрос.")
            st.stop()

        with st.spinner("Поиск..."):
            result = ask(
                question.strip(),
                k=top_k,
                retriever=load_retriever(),
                min_score=min_score,
            )

        render_fragments(result["sources"], question, min_score)

        st.subheader("Ответ")
        st.text(result["answer"])

        render_sources(result["sources"], question, min_score)


if __name__ == "__main__":
    main()
