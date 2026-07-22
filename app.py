import streamlit as st

st.set_page_config(
    page_title="AI Marketing Generator",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Marketing Generator")

name = st.text_input("Enter your name")

if st.button("Submit"):
    st.success(f"Welcome {name}!")