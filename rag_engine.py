from dotenv import load_dotenv
load_dotenv()

from groq import Groq
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

client = Groq()  # reads GROQ_API_KEY from .env

CHAT_MODEL = "openai/gpt-oss-120b"

def build_index(chunks: list[str]):
    """Returns a TF-IDF vector store for the chunks."""
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(chunks)
    return {"chunks": chunks, "vectorizer": vectorizer, "matrix": matrix}

def retrieve(query: str, index, top_k=4):
    q_vec = index["vectorizer"].transform([query])
    sims = cosine_similarity(q_vec, index["matrix"])[0]
    top_idx = sims.argsort()[::-1][:top_k]
    return [index["chunks"][i] for i in top_idx]

def ask_llm(prompt: str, temperature: float = 0.3) -> str:
    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return resp.choices[0].message.content

def rag_answer(query: str, index) -> str:
    context = "\n\n---\n\n".join(retrieve(query, index))
    prompt = f"""Answer the question using ONLY the context below. If the context doesn't contain the answer, say so.

Context:
{context}

Question: {query}
Answer:"""
    return ask_llm(prompt)

def analyze_paper(full_text: str, index) -> dict:
    """Generates Summary, Key Contributions, Limitations, Future Work."""
    context = "\n\n---\n\n".join(retrieve("main findings methodology results conclusion", index, top_k=6))

    prompts = {
        "Summary": f"Summarize this research paper in 4-6 sentences:\n\n{context}",
        "Key Contributions": f"List the key contributions of this paper as bullet points:\n\n{context}",
        "Limitations": f"What limitations does this paper have or acknowledge? List as bullet points:\n\n{context}",
        "Future Work": f"What future work does this paper suggest? List as bullet points:\n\n{context}",
    }
    return {label: ask_llm(p) for label, p in prompts.items()}