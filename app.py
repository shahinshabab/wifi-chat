# app.py
import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Sticky Text Input", page_icon="📝", layout="centered")

DATA_FILE = Path("saved_text.json")

def load_text() -> str:
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8")).get("text", "")
        except Exception:
            return ""
    return ""

def save_text(text: str) -> None:
    DATA_FILE.write_text(json.dumps({"text": text}, ensure_ascii=False, indent=2), encoding="utf-8")

# Initialize session state from disk (runs once)
if "saved_text" not in st.session_state:
    st.session_state.saved_text = load_text()

st.title("📝 Persistent Text Box")
st.caption("Type something, hit **Submit**, and it’ll still be here after refresh.")

# Big text area, pre-filled with the saved text
text = st.text_area(
    "Your text",
    value=st.session_state.saved_text,
    height=300,
    placeholder="Start typing here…",
)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Submit", type="primary"):
        st.session_state.saved_text = text
        save_text(text)
        st.success("Saved! Your text will persist across refreshes.")
with col2:
    if st.button("Clear"):
        st.session_state.saved_text = ""
        save_text("")
        st.info("Cleared.")

# Show current stored value
with st.expander("Show stored value"):
    st.code(st.session_state.saved_text or "«empty»")

st.caption("Data is stored in ./saved_text.json")
