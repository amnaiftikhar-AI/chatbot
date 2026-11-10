from backend.services.reasoning.query_decomposer import decompose_query
from backend.services.reasoning.evidence_analyzer import prepare_evidence, find_version_warnings
from backend.services.reasoning.answer_generator import generate_answer
from backend.services.retrieval.hybrid_retriever import retriever
from backend.services.memory.conversation_memory import get_or_create_ticket, load_history, save_message

async def answer_question(db, question, ticket_key=None):
    ticket = get_or_create_ticket(db, ticket_key, question)
    history = load_history(db, ticket.id)
    subqueries = decompose_query(question)
    gathered = {}
    for query in subqueries:
        for item in retriever.search(query, k=8):
            gathered[item["chunk_key"]] = item
    results = list(gathered.values())
    evidence = prepare_evidence(results)
    warnings = find_version_warnings(evidence)
    answer = await generate_answer(question, evidence, warnings, history)
    save_message(db, ticket.id, "user", question)
    save_message(db, ticket.id, "assistant", answer)
    sources = [{
        "document": item["document"],
        "page": item["page"],
        "section": item["section"],
        "document_id": item["document_id"]
    } for item in evidence]
    return {"ticket_id": ticket.ticket_key, "answer": answer, "sources": sources, "subqueries": subqueries}
