def find_rank(sources, topic, keywords):
    for i, source in enumerate(sources):
        if source.startswith(topic + "：") and all(keyword in source for keyword in keywords):
            return i + 1
    return None
