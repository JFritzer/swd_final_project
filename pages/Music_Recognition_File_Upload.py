import streamlit as st

#Page header configuration:
st.set_page_config(page_title="Music Recognition", page_icon="🎵", layout="wide")


st.markdown("# Music recognition tool, using file upload")



#Uploading audio file:
audio_file = st.file_uploader("Please upload an audio file.", type=[".mp3", ".wav", ".ogg"])

#Playback of uploaded audiofile:
if audio_file is not None:
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')

#Button to start the recognition:
if st.button("Start recognition"):
    st.write("Recognition started...")
    #Searching for audio snippet in the database. (Here we need to add the function to search for the audio snippet in the database)
    st.write("Recognition finished!")
    