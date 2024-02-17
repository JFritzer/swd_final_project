import streamlit as st
import tinydb as db
from random import randint

db_test = db.TinyDB('./db/db_test.json')



st.set_page_config(page_title="Music Recognition", page_icon=":smiley:")
st.title("Music Recognition App by PandasEngineering")


st.subheader("Welcome to the Music Recognition App from PandasEngineering.")

st.write(" ")
st.write(" ")
st.write(" ")



st.write("Please choose a option from the sidebar to get started.")



