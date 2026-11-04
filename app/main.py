from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from app.config import ROOT
from app.retriever_chroma import load_knowledge_base, retrieve
from app.generator import generate_answer
from app.loader import load_sections, build_chunks

@asynccontextmanager
async def lifespan(app):
    load_knowledge_base(build_chunks(load_sections(str(ROOT / "data/knowledge_base.md"))))
    yield

app = FastAPI(title="客服知识库 RAG 演示", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "RAG服务已启动"}

@app.get("/ask")
def ask_question(question: str = Query(..., min_length=1, max_length=500)):
    context, sources = retrieve(question)
    try:
        answer = generate_answer(question, context)
    except Exception:
        raise HTTPException(status_code=502, detail="生成失败，请检查模型配置和上游状态") from None
    return {"question": question, "answer": answer, "sources": sources}
