def decompose_query(question):
    text = question.strip()
    lower = text.lower()
    queries = [text]
    if any(term in lower for term in ["vpn", "sc-", "error"]):
        queries.append("Find the meaning and troubleshooting steps for the exact VPN error code")
    if any(term in lower for term in ["wifi", "wi-fi", "network", "connect"]):
        queries.append("Check device network connection and DNS configuration requirements")
    if "version" in lower or "windows" in lower or "vpn" in lower:
        queries.append("Find software and operating system version compatibility instructions")
    return list(dict.fromkeys(queries))
