import streamlit as st
import requests

st.title("Knowledge Documents")
response = requests.get("http://127.0.0.1:8000/documents/")
if response.ok:
    for document in response.json():
        left, right = st.columns([4, 1])
        left.write(f'{document["title"]} · {document["software_version"]} · {document["status"]}')
        if right.button("Delete", key=f'del_{document["id"]}'):
            requests.delete(f'http://127.0.0.1:8000/documents/{document["id"]}')
            st.rerun()
else:
    st.error(response.text)
