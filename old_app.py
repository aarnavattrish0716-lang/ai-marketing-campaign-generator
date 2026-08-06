import streamlit as st
import requests
st.set_page_config(
    page_title="AI Marketing Generator",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Marketing Generator")

product = st.text_input("Product")
audience=st.text_input("Audience")
platform=st.selectbox("Platform",["Instagram","Facebook","LinkedIn"])
if st.button("Generate Campaign"):
    try:
        response = requests.post("http://127.0.0.1:8000/campaigns",
                                json={
                                    "product":product,
                                    "audience":audience,
                                    "platform":platform
                                })
        data = response.json()
        st.subheader("Campaign Title")
        st.write(data["title"])

        st.subheader("Tagline")
        st.write(data["tagline"])

        st.subheader("Call To Action")
        st.write(data["cta"])

        st.subheader("Hashtags")
        st.write(" ".join(data["hashtags"]))
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed:{e}")