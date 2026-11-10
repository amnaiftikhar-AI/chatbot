import re

def extract_metadata(text, filename):
    def value(pattern, default):
        match = re.search(pattern, text, re.I | re.M)
        return match.group(1).strip() if match else default
    return {
        "document_key": value(r"DOCUMENT_ID:\s*(.+)", filename),
        "title": value(r"TITLE:\s*(.+)", filename),
        "document_type": value(r"DOCUMENT_TYPE:\s*(.+)", "uploaded_document"),
        "device_model": value(r"DEVICE_MODEL:\s*(.+)", "unknown"),
        "software_version": value(r"SOFTWARE_VERSION:\s*(.+)", "unknown"),
        "category": value(r"CATEGORY:\s*(.+)", "general"),
        "status": value(r"STATUS:\s*(.+)", "active").lower()
    }
