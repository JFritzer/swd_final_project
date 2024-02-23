import streamlit as st

st.set_page_config(page_title="Music Recognition", page_icon="page_icon.png", layout="wide")
col1, mid, col2 = st.columns([20,1,20])
with col1:
    st.title("Music Recognition App by PandasEngineering")

    st.subheader("Welcome to the Music Recognition App from PandasEngineering.")
    st.write("Please choose an option from the sidebar to get started.")
with col2:
    st.image("page_icon.png")