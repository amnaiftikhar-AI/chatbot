from backend.services.ingestion.structure_extractor import extract_sections

def test_sections_keep_page_and_heading():
    result = extract_sections([{"page": 2, "text": "SECTION 1: Network\nCheck DNS"}])
    assert result[0]["page"] == 2
    assert "SECTION 1" in result[0]["section"]
