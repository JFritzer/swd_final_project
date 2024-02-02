import streamlit as st
import tinydb as db
from random import randint

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
    if randint(1,2) == 1:
        st.write('HAH. GAAAAAYYYY!!!!!')
    else:
        st.write("AHA. NOT GAAAYYYY!!!!")
else:
    st.write('Press the button.')



#Debug:
    
#Page Music_Recognition_File_Upload: Doesnt show up in Streamlit as page. I dont know why.