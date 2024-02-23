import streamlit as st

st.set_page_config(page_title="Music Recognition", page_icon="page_icon.png")
st.title("Music Recognition App by PandasEngineering")

st.subheader("Welcome to the Music Recognition App from PandasEngineering.")
# Bildpfad angeben und korrigieren
image_path = "page_icon.png"
st.image(image_path)

st.write("Please choose an option from the sidebar to get started.")