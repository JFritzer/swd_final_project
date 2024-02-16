import streamlit as st
from tinydb import TinyDB, Query
from typing import Optional, BinaryIO
import uuid
import os
from music_analyzer import read_in


# Verbindung zur Datenbank herstellen
db = TinyDB('./db/multimedia_database.json')


# Seiteneinstellungen festlegen
st.set_page_config(page_title="Music Recognition", page_icon="🎵", layout="wide")


st.markdown("# Music recognition tool, using file upload")


# Funktion zum Lesen des Audios und Berechnen der Hashes
def calculate_hashes(audio_file: BinaryIO) -> Optional[str]:
    """
    Liest das hochgeladene Audiodatei ein und berechnet die Hashes.

    Args:
        audio_file (BinaryIO): Hochgeladene Audiodatei.

    Returns:
        str: Hashes des Audios.
    """
    if audio_file is not None:
        # Speichern der Audiodatei temporär auf dem Server
        with open("uploaded_audio.wav", "wb") as f:
            f.write(audio_file.read())
        
        # Aufruf der read_in-Funktion mit dem Dateipfad
        hashes = read_in("uploaded_audio.wav")
        
        # Löschen der temporären Audiodatei
        os.remove("uploaded_audio.wav")
        
        return hashes
    else:
        return None
    

# Funktion zum Suchen nach passenden Hashes in der Datenbank
def find_matching_hashes(hashes: str) -> Optional[str]:
    """
    Sucht in der Datenbank nach passenden Hashes und gibt die zugehörige ID zurück.

    Args:
        hashes (str): Hashes des hochgeladenen Audios.

    Returns:
        Optional[str]: Die ID des passenden Eintrags in der Datenbank, oder None, wenn kein passender Eintrag gefunden wurde.
    """
    Entry = Query()
    result = db.get(Entry.hashes == hashes)
    if result:
        return result.get('id')
    else:
        return None


# Uploading audio file
audio_file = st.file_uploader("Please upload an audio file.", type=[".mp3", ".wav", ".ogg"])

# Button to start the recognition
if st.button("Start recognition"):
    if audio_file is not None:
        st.write("Recognition started...")
        # Calculate hashes of the uploaded audio
        hashes = calculate_hashes(audio_file)
        if hashes:
            # Search for matching hashes in the database
            matching_id = find_matching_hashes(hashes)
            if matching_id:
                st.write(f"Matching ID found in the database: {matching_id}")
            else:
                st.write("No matching entry found in the database.")
            st.write("Recognition finished!")
        else:
            st.write("Error")
    else:
        st.write("Please upload an audio file.")