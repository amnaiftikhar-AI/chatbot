def reciprocal_rank_fusion(result_lists, k=60):
    scores = {}
    records = {}

    for results in result_lists:
        for rank, item in enumerate(results, 1):
            key = item["chunk_key"]
            scores[key] = scores.get(key, 0) + 1 / (k + rank)
            records[key] = item

    ranked = sorted(scores, key=scores.get, reverse=True)
    return [dict(records[key], rrf_score=scores[key]) for key in ranked]


def deduplicate(results):
    seen = set()
    output = []

    for item in results:
        content = item.get("content", "").strip().lower()
        key = (
            item.get("document_id"),
            item.get("section"),
            content or item.get("chunk_key")
        )

        if key not in seen:
            seen.add(key)
            output.append(item)

    return output
