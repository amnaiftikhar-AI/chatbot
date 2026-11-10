from backend.services.retrieval.rrf import reciprocal_rank_fusion, deduplicate

def test_rrf_combines_results():
    a = [{"chunk_key": "a", "content": "one"}]
    b = [{"chunk_key": "a", "content": "one"}, {"chunk_key": "b", "content": "two"}]
    result = reciprocal_rank_fusion([a, b])
    assert result[0]["chunk_key"] == "a"
    assert len(deduplicate(result)) == 2
