import re

def extract_sections(pages):
    output = []
    for page in pages:
        current_heading = "General"
        buffer = []
        for line in page["text"].splitlines():
            line = line.strip()
            if not line:
                continue
            if re.match(r"^(SECTION\s+\d+|CHAPTER\s+\d+|\d+(\.\d+)*\s+)", line, re.I):
                if buffer:
                    output.append({"page": page["page"], "section": current_heading, "text": "\n".join(buffer)})
                    buffer = []
                current_heading = line
            else:
                buffer.append(line)
        if buffer:
            output.append({"page": page["page"], "section": current_heading, "text": "\n".join(buffer)})
    return output
