from importlib import import_module

from backend.core.config import settings
from backend.services.reasoning.prompts import SYSTEM_PROMPT


async def generate_answer(question, evidence, warnings, history):

    if not settings.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is missing from environment configuration")

    ChatGroq = import_module("langchain_groq").ChatGroq

    llm = ChatGroq(
        model=settings.LLM_MODEL,
        temperature=0.2,
        api_key=settings.GROQ_API_KEY,
        timeout=60,
        max_retries=2
    )

    context = "\n\n".join(
        f"""
Document: {item["document"]}
Page: {item["page"]}
Section: {item["section"]}
Content: {item["text"]}
"""
        for item in evidence
    )

    messages = [
        ("system", SYSTEM_PROMPT)
    ]

    for item in history[-8:]:
        messages.append((item["role"], item["content"]))

    messages.append((
        "human",
        f"""
Question: {question}

Evidence:
{context}

Warnings:
{warnings}
"""
    ))

    response = await llm.ainvoke(messages)

    return response.content