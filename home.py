import streamlit as st
import tinydb as db

db_test = db.TinyDB('./db/db_test.json')



st.set_page_config(page_title="Music Recognition", page_icon=":smiley:")
st.title("Music Recognition App by PandasEngineering")


st.write("Welcome to the Music Recognition App from PandasEngineering.")

st.write(" ")
st.write(" ")
st.write(" ")



st.write("Off Topic -> This is a gay test. Click the button and the program will tell you if you are gay or not.")

st.button("Reset", type="primary")
if st.button('GayCheck'):
    st.write('HAH. GAAAAAYYYY!!!!!')
else:
    st.write('Press the button.')