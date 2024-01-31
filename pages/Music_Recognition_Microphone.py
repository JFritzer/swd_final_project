import streamlit as st
from st_audiorec import st_audiorec





st.markdown("# Music recognition tool, using the microphone")


#Full Recording device.
wav_audio_data = st_audiorec()













#Some functions we dont use right now, but are maybe helpful in the future:

    
#If we want to save the audiofile as a file: (This might be useful if we use the microphone to record the audiofile)
#with open("audio_file.mp3", "wb") as f:
#    f.write(audio_file.getbuffer())










#Audio Recorder imported from: https://github.com/stefanrmmr/streamlit-audio-recorder