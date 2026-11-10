import requests
import streamlit as st

API = "http://127.0.0.1:8000"

st.title("Troubleshoot an issue")

ticket_id = st.text_input("Existing ticket ID (optional)")

if ticket_id and st.button("Load conversation history"):
    try:
        response = requests.get(f"{API}/tickets/{ticket_id}/messages", timeout=20)
        if response.ok:
            result = response.json()
            st.subheader(result.get("title", "Conversation history"))
            for message in result["messages"]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        else:
            st.error(response.text)
    except requests.RequestException as error:
        st.error(f"Could not load history: {error}")

question = st.text_area("Describe the problem")

if st.button("Investigate") and question.strip():
    try:
        response = requests.post(
            f"{API}/chat/",
            json={
                "question": question,
                "ticket_id": ticket_id.strip() or None
            },
            timeout=180
        )

        if response.ok:
            result = response.json()
            st.success(f'Ticket ID: {result["ticket_id"]}')
            st.markdown(result["answer"])
            st.subheader("Sources")
            st.json(result["sources"])
        else:
            st.error(response.text)

    except requests.RequestException as error:
        st.error(f"Investigation failed: {error}")

if ticket_id and st.button("Delete conversation history", type="secondary"):
    try:
        response = requests.delete(f"{API}/tickets/{ticket_id}", timeout=20)
        if response.ok:
            st.success("Conversation history deleted.")
        else:
            st.error(response.text)
    except requests.RequestException as error:
        st.error(f"Delete failed: {error}")
