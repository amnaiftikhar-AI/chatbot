def filter_items(items, device_model=None, software_version=None, document_type=None, category=None):
    output = []
    for item in items:
        metadata = item.get("metadata", {})
        if device_model and device_model.lower() not in metadata.get("device_model", "").lower():
            continue
        if software_version and software_version.lower() not in metadata.get("software_version", "").lower():
            continue
        if document_type and document_type.lower() != metadata.get("document_type", "").lower():
            continue
        if category and category.lower() != metadata.get("category", "").lower():
            continue
        output.append(item)
    return output
