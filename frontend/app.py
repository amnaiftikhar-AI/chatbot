import requests
import streamlit as st

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="IT Troubleshooting Assistant", page_icon="🛠️")
st.title("IT Troubleshooting Assistant")
st.write("Upload technical documents and investigate IT issues with evidence.")


def fetch_tickets():
    response = requests.get(f"{API}/tickets/", timeout=20)
    response.raise_for_status()
    return response.json()


def load_messages(ticket_id):
    if not ticket_id:
        return []
    response = requests.get(f"{API}/tickets/{ticket_id}/messages", timeout=20)
    response.raise_for_status()
    return response.json()["messages"]


if "ticket_id" not in st.session_state:
    st.session_state.ticket_id = None

with st.sidebar:
    st.subheader("Upload knowledge")
    uploaded = st.file_uploader("Choose PDF or TXT", type=["pdf", "txt"])
    if st.button("Upload document") and uploaded:
        try:
            response = requests.post(
                f"{API}/documents/upload",
                files={"file": (uploaded.name, uploaded.getvalue())},
                timeout=180
            )
            if response.ok:
                st.success("Document uploaded and processed.")
                st.json(response.json())
            else:
                st.error(response.text)
        except requests.RequestException as error:
            st.error(f"Upload failed: {error}")

    st.divider()
    st.subheader("Conversation history")

    try:
        tickets = fetch_tickets()
        ticket_lookup = {
            item["ticket_id"]: item
            for item in tickets
        }
        ticket_options = [""] + list(ticket_lookup.keys())

        selected_ticket = st.selectbox(
            "Open a previous conversation",
            options=ticket_options,
            format_func=lambda key: (
                "Select a conversation"
                if not key
                else f'{ticket_lookup[key]["title"][:45]} ({key[:8]})'
            )
        )

        if selected_ticket and selected_ticket != st.session_state.ticket_id:
            st.session_state.ticket_id = selected_ticket
            st.rerun()

        if st.button("New conversation"):
            st.session_state.ticket_id = None
            st.rerun()

        if st.session_state.ticket_id:
            st.caption(f"Current ticket ID: {st.session_state.ticket_id}")
            if st.button("Delete this conversation", type="secondary"):
                delete_response = requests.delete(
                    f'{API}/tickets/{st.session_state.ticket_id}',
                    timeout=20
                )
                if delete_response.ok:
                    st.session_state.ticket_id = None
                    st.success("Conversation history deleted.")
                    st.rerun()
                else:
                    st.error(delete_response.text)

    except requests.RequestException as error:
        st.warning(f"Could not load conversation history: {error}")

st.subheader("Troubleshooting chat")

if st.session_state.ticket_id:
    st.caption(f"Continuing ticket: {st.session_state.ticket_id}")

try:
    if st.session_state.ticket_id:
        history = load_messages(st.session_state.ticket_id)
    else:
        history = []

    for message in history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

except requests.RequestException as error:
    st.error(f"Could not load conversation messages: {error}")

question = st.chat_input("Describe your IT issue")

if question:
    try:
        response = requests.post(
            f"{API}/chat/",
            json={
                "question": question,
                "ticket_id": st.session_state.ticket_id
            },
            timeout=180
        )

        if response.ok:
            data = response.json()
            st.session_state.ticket_id = data["ticket_id"]
            st.rerun()
        else:
            st.error(response.text)

    except requests.RequestException as error:
        st.error(f"Chat request failed: {error}")

st.subheader("Active documents")

try:
    docs_response = requests.get(f"{API}/documents/", timeout=20)
    docs_response.raise_for_status()
    docs = docs_response.json()
    if docs:
        st.dataframe(docs, use_container_width=True)
    else:
        st.info("No active documents have been uploaded yet.")
except requests.RequestException:
    st.info("Start the FastAPI server to view documents.")
