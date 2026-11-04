# 客服知识库 RAG 问答

基于 FastAPI、ChromaDB、sentence-transformers 和 DeepSeek 的个人学习项目。
从演示客服文档中分块、向量检索，再把资料和问题交给模型，返回回答与检索片段。

## 运行

建议使用 Python 3.12 或 3.13。

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

在 `.env` 填写自己的 Key，再打开 <http://127.0.0.1:8000/docs>，使用 `/ask` 提问。
首次运行会下载多语言 Embedding 模型，需要联网和额外磁盘空间；检索索引为进程内存存储，每次启动重建。
示例知识库是演示数据，不是实际企业资料。

## 检索评估

```bash
python -m unittest discover -s tests
python -m eval.evaluate --output reports/retrieval.json
```

评估集有 15 题，其中 10 题有对应资料，5 题无答案。默认仅评估 10 题的检索排名，不消耗生成 API 额度；按「主题前缀＋全部关键词」同时命中判定 Top1/Top2。
本仓库提供本地运行生成的 `reports/retrieval.json`，数字只代表这一小规模演示集，不能外推为通用准确率。

无答案题需显式运行 `python -m eval.evaluate --generation` 才会调用真实模型。拒答标记检测是辅助指标，仍需要人工检查，不能视作提示注入防护证明。

## 实现与边界

- `app/loader.py`：按 Markdown 小节和中文句子切片，每片保留主题。
- `app/retriever_chroma.py`：多语言向量化、内存索引、Top-k 检索。
- `app/generator.py`：system/user 角色分离、基于资料回答与缺失时拒答提示。
- `eval/`：可复现的题集与检索评估；`tests/` 检查切片和排名判定。

目前没有文档上传、用户鉴权、持久化索引、重排和系统性提示注入防护。返回的是检索片段，不是逐句经过事实校验的引用。
这是可学习、可复现的 RAG 原型，不应直接暴露成公共问答服务。MIT 许可。
