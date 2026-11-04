"""默认只评估检索，不调用生成 API；--generation 显式启用付费生成评估。"""
import argparse
import json
from pathlib import Path
from app.config import ROOT, EMBEDDING_MODEL_NAME
from app.loader import load_sections, build_chunks
from app.retriever_chroma import load_knowledge_base, retrieve
from eval.metrics import find_rank

def evaluate(generation=False):
    load_knowledge_base(build_chunks(load_sections(str(ROOT / "data/knowledge_base.md"))))
    cases = json.loads((ROOT / "eval/test_set.json").read_text())
    rows, top1, top2 = [], 0, 0
    for item in cases:
        if item["expected_topic"] is None:
            continue
        _, sources = retrieve(item["question"], top_k=4)
        rank = find_rank(sources, item["expected_topic"], item["expected_keywords"])
        top1 += rank == 1
        top2 += rank is not None and rank <= 2
        rows.append({"question": item["question"], "rank": rank, "sources": sources})
    report = {"embedding_model": EMBEDDING_MODEL_NAME, "answerable_count": len(rows), "top1_hits": top1, "top2_hits": top2, "unanswerable_count": sum(x["expected_topic"] is None for x in cases), "generation_evaluated": generation, "retrieval": rows}
    if generation:
        from app.generator import generate_answer
        checks = []
        for item in cases:
            if item["expected_topic"] is not None:
                continue
            context, _ = retrieve(item["question"])
            answer = generate_answer(item["question"], context)
            checks.append({"question": item["question"], "answer": answer, "refusal_marker_found": "未找到相关信息" in answer})
        report["unanswerable_generation"] = checks
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generation", action="store_true", help="调用真实模型，消耗 API 额度；拒答标记仍需人工复核")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = evaluate(args.generation)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n")
