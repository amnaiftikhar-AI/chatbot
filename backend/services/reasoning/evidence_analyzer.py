def prepare_evidence(results):
    grouped = {}
    for item in results:
        grouped.setdefault(item["document_id"], []).append(item)
    evidence = []
    for document_id, chunks in grouped.items():
        for item in chunks:
            evidence.append({
                "document_id": document_id,
                "document": item["title"],
                "page": item["page"],
                "section": item["section"],
                "text": item["content"],
                "metadata": item["metadata"]
            })
    return evidence

def find_version_warnings(evidence):
    warnings = []
    for item in evidence:
        if item["metadata"].get("status") == "archived" or "archived" in item["document"].lower() or "4.1" in item["metadata"].get("software_version", ""):
            warnings.append(f'{item["document"]} is archived or version-specific; do not apply it automatically to another version.')
    return warnings
