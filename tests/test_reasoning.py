from backend.services.reasoning.query_decomposer import decompose_query

def test_query_decomposition():
    queries = decompose_query("Windows 11 VPN error SC-809")
    assert len(queries) >= 2
