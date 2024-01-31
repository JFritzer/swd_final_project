import streamlit as st
import numpy as np


#Page header configuration:
st.set_page_config(page_title="Music Import", page_icon="🎵", layout="wide")



st.markdown("# Music import tool for database filling")


#Uploading audio file:
audio_file = st.file_uploader("Please upload an audio file.", type=[".mp3", ".wav", ".ogg"])

#Playback of uploaded audiofile:
if audio_file is not None:
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')

#Button to start the import:
if st.button("Start import"):
    st.write("Import started...")
    #Importing the audiofile into the database: (Here we need to add the function to import the audiofile into the database)
    st.write("Import finished!")






    











