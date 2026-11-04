import re

def load_sections(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    sections = text.split("\n## ")
    sections = [s.strip() for s in sections if s.strip() and not s.startswith("# ")]
    return sections


def split_sentences(text: str) -> list[str]:
    sentences = re.split(r'(?<=[。！？])', text)
    return [s.strip() for s in sentences if s.strip()]

def build_chunks(sections: list[str], sentences_per_chunk: int = 2) -> list[str]:
    chunks = []
    for section in sections:
        title, body = section.split("\n", 1)
        sentences = split_sentences(body)
        for i in range(0, len(sentences), sentences_per_chunk):
            group = sentences[i:i + sentences_per_chunk]
            chunks.append(f"{title}：" + "".join(group))
    return chunks