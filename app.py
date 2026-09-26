import streamlit as st
from pdf_utils import extract_text, chunk_text
from rag_engine import build_index, analyze_paper, rag_answer, ask_llm

st.set_page_config(page_title="Research Paper Assistant", layout="wide", page_icon="📄")

st.markdown("""
<style>

/* ==============================
   GLOBAL
   ============================== */

.stApp {
    background: #0B0D11;
}

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 4rem;
    max-width: 1450px;
}

h1, h2, h3, h4 {
    letter-spacing: -0.02em;
}

/* ==============================
   SIDEBAR
   ============================== */

section[data-testid="stSidebar"] {
    background: #101217;
    border-right: 1px solid #252933;
}

section[data-testid="stSidebar"] > div {
    padding: 2rem 1.25rem;
}

.sidebar-brand {
    font-size: 1.15rem;
    font-weight: 700;
    color: #F4F4F5;
    margin-bottom: 0.2rem;
}

.sidebar-description {
    color: #858B98;
    font-size: 0.82rem;
    line-height: 1.5;
}

/* ==============================
   PAGE HEADER
   ============================== */

.page-header {
    margin-bottom: 1.8rem;
}

.page-title {
    font-size: 2.15rem;
    font-weight: 750;
    color: #F5F5F6;
    margin-bottom: 0.35rem;
    letter-spacing: -0.04em;
}

.page-subtitle {
    color: #858B98;
    font-size: 0.95rem;
}

/* ==============================
   CARDS
   ============================== */

.card {
    background: #14171D;
    border: 1px solid #252933;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 18px;
    transition: border-color 0.2s ease, transform 0.2s ease;
}

.card:hover {
    border-color: #343946;
    transform: translateY(-1px);
}

.card h4 {
    margin-top: 0;
    margin-bottom: 12px;
    color: #CFC8FF;
    font-size: 1rem;
    font-weight: 650;
}

.card-content {
    color: #D5D7DC;
    line-height: 1.7;
    font-size: 0.94rem;
}

/* ==============================
   ANALYSIS CARDS
   ============================== */

.analysis-card {
    background: #12151A;
    border: 1px solid #272B34;
    border-radius: 16px;
    padding: 24px;
    min-height: 180px;
    margin-bottom: 18px;
}

.analysis-label {
    color: #AAA2FF;
    font-size: 0.86rem;
    font-weight: 650;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 12px;
}

.analysis-content {
    color: #D8D9DE;
    line-height: 1.7;
    font-size: 0.93rem;
}

/* ==============================
   STATUS
   ============================== */

.status {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: #171A21;
    border: 1px solid #292D36;
    border-radius: 999px;
    padding: 6px 11px;
    color: #AEB3BE;
    font-size: 0.78rem;
    margin-bottom: 18px;
}

.status-dot {
    width: 7px;
    height: 7px;
    background: #8B7CF6;
    border-radius: 50%;
}

/* ==============================
   INPUTS
   ============================== */

.stTextInput input {
    background: #111419 !important;
    border: 1px solid #292D36 !important;
    border-radius: 10px !important;
    color: #F4F4F5 !important;
    padding: 0.75rem 0.9rem !important;
}

.stTextInput input:focus {
    border-color: #7064D9 !important;
    box-shadow: 0 0 0 1px #7064D9 !important;
}

/* ==============================
   BUTTONS
   ============================== */

.stButton > button {
    border-radius: 9px;
    border: 1px solid #303440;
    background: #181B22;
    color: #E9E9EC;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #7770C9;
    color: #FFFFFF;
}

/* Primary buttons */

.stButton > button[kind="primary"] {
    background: #7669E8;
    border: 1px solid #7669E8;
    color: white;
}

.stButton > button[kind="primary"]:hover {
    background: #8478F0;
    border-color: #8478F0;
}

/* ==============================
   TABS
   ============================== */

.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: #101217;
    padding: 5px;
    border-radius: 11px;
    border: 1px solid #252933;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 9px 18px;
    color: #858B98;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background: #1B1E26;
    color: #F1F1F3 !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background: #8B7CF6;
}

/* ==============================
   FILE UPLOADER
   ============================== */

[data-testid="stFileUploader"] {
    background: #14171D;
    border: 1px dashed #343946;
    border-radius: 12px;
    padding: 8px;
}

[data-testid="stFileUploader"]:hover {
    border-color: #7064D9;
}

/* ==============================
   SELECT BOX
   ============================== */

div[data-baseweb="select"] > div {
    background: #14171D;
    border-color: #292D36;
    border-radius: 9px;
}

/* ==============================
   DIVIDERS
   ============================== */

hr {
    border-color: #252933;
}

/* ==============================
   HELPER TEXT
   ============================== */

.subtle {
    color: #858B98;
    font-size: 0.88rem;
    line-height: 1.6;
}

/* ==============================
   EMPTY STATE
   ============================== */

.empty-state {
    background: #111419;
    border: 1px solid #252933;
    border-radius: 16px;
    padding: 55px 30px;
    text-align: center;
    margin-top: 25px;
}

.empty-icon {
    font-size: 2.4rem;
    margin-bottom: 12px;
}

.empty-title {
    color: #E7E7EA;
    font-size: 1.2rem;
    font-weight: 650;
    margin-bottom: 6px;
}

.empty-description {
    color: #858B98;
    font-size: 0.9rem;
}

/* ==============================
   CHAT / ANSWER
   ============================== */

.answer-card {
    background: #14171D;
    border: 1px solid #292D36;
    border-radius: 14px;
    padding: 24px;
    margin-top: 18px;
    color: #D9DADE;
    line-height: 1.75;
}

/* ==============================
   SCROLLBAR
   ============================== */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #0B0D11;
}

::-webkit-scrollbar-thumb {
    background: #2B2F38;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #3A3F4B;
}

</style>
""", unsafe_allow_html=True)

if "papers" not in st.session_state:
    st.session_state.papers = {}

ICONS = {"Summary": "📝", "Key Contributions": "✅", "Limitations": "⚠️", "Future Work": "🔭"}

with st.sidebar:
    st.markdown("### 📄 Research Paper Assistant")
    st.markdown("<span class='subtle'>Upload, summarize, and query papers.</span>", unsafe_allow_html=True)
    st.divider()
    uploaded = st.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)

    if uploaded:
        for f in uploaded:
            if f.name not in st.session_state.papers:
                with st.spinner(f"Indexing {f.name}..."):
                    text = extract_text(f)
                    chunks = chunk_text(text)
                    index = build_index(chunks)
                    st.session_state.papers[f.name] = {"index": index, "analysis": None}
                st.success(f"{f.name} ready")

    if st.session_state.papers:
        st.divider()
        paper_name = st.selectbox("Active paper", list(st.session_state.papers.keys()))
    else:
        paper_name = None

if not paper_name:
    st.title("📄 Your Research Workspace")

    st.write(
        "Upload a research paper to extract insights, "
        "ask questions, and compare findings with other papers."
    )

    st.info("👈 Upload a PDF from the sidebar to get started.")

    st.stop()     
paper = st.session_state.papers[paper_name]
st.markdown(f"""
<div class="page-header">
    <div class="page-title">{paper_name}</div>
    <div class="page-subtitle">
        Research workspace · Analyze, question, and compare
    </div>
</div>

<div class="status">
    <span class="status-dot"></span>
    Paper indexed and ready
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Analysis", "💬 Ask a Question", "🔍 Compare Papers"])

with tab1:
    if st.button("Analyze Paper", type="primary"):
        with st.spinner("Generating analysis..."):
            paper["analysis"] = analyze_paper(None, paper["index"])

    if paper["analysis"]:
        cols = st.columns(2)
        for i, (label, content) in enumerate(paper["analysis"].items()):
            with cols[i % 2]:
                st.markdown(f"""<div class="analysis-card">
                    <div class="analysis-label">
                        {ICONS.get(label, "📌")} {label}
                    </div>
                    <div class="analysis-content">
                        {content}
                    </div>
                </div>""", unsafe_allow_html=True)    
        st.markdown("<span class='subtle'>Click Analyze Paper to generate a summary, contributions, limitations, and future work.</span>", unsafe_allow_html=True)

with tab2:
    q = st.text_input("Ask something about this paper", placeholder="e.g. What was the sample size?")
    if q:
        with st.spinner("Thinking..."):
            answer = rag_answer(q, paper["index"])
        st.markdown(f"""<div class="answer-card">
            {answer}
        </div>""", unsafe_allow_html=True)

with tab3:
    others = [n for n in st.session_state.papers if n != paper_name]
    if not others:
        st.markdown("<span class='subtle'>Upload a second paper to compare.</span>", unsafe_allow_html=True)
    else:
        compare_with = st.selectbox("Compare with", others)
        if st.button("Compare", type="primary"):
            idx_a = paper["index"]
            idx_b = st.session_state.papers[compare_with]["index"]
            ctx_a = "\n".join(idx_a["chunks"][:4])
            ctx_b = "\n".join(idx_b["chunks"][:4])
            prompt = f"Compare these two papers' approaches and findings:\n\nPaper A:\n{ctx_a}\n\nPaper B:\n{ctx_b}"
            with st.spinner("Comparing..."):
                result = ask_llm(prompt)
            st.markdown(f"""<div class="answer-card">
                {result}
            </div>""", unsafe_allow_html=True)