import streamlit as st
from tinydb import TinyDB, Query
from typing import Optional, BinaryIO, Tuple
import os
from music_analyzer import read_in
from music_analyzer import recognise_song #(song_recognise, song_compare) -> int:
import wave
import settings




# Seiteneinstellungen festlegen
st.set_page_config(page_title="Music Recognition", page_icon="🎵", layout="wide")


st.markdown("# Music recognition tool, using file upload")
st.subheader("Here you can upload your file and the program gives you the name of the song back.")


# Klasse für die Multimedia-Datenbank
class MultimediaDatabase:
    def __init__(self, db_path: str = './db/multimedia_database.json') -> None:
        self.db = TinyDB(db_path)

    def get_entry_id_by_hashes(self, recognise_hashes: str) -> str:
        """Hole die ID eines Eintrags aus der Datenbank anhand der Hashes."""
        Entry = Query()
        entry = self.db.get(Entry.hashes == recognise_hashes)
        if entry:
            return entry.get('id')
        else:
            return None
    
    def find_matching_hashes(self, hashes: str) -> Optional[str]:
        """
        Sucht in der Datenbank nach übereinstimmenden Hashes.

        Args:
            hashes (str): Die Hashes des hochgeladenen Audios.

        Returns:
            Optional[str]: Die ID des gefundenen Eintrags oder None, wenn kein übereinstimmender Eintrag gefunden wurde.
        """
        matching_id = self.get_entry_id_by_hashes(hashes)
        return matching_id
    
    def get_title_and_image_by_id(self, entry_id: str) -> Optional[Tuple[str, str]]:
        """Holt den Titel und den Bildpfad eines Eintrags aus der Datenbank anhand der ID."""
        Entry = Query()
        entry = self.db.get(Entry.id == entry_id)
        if entry:
            title = entry.get('title')
            image_path = entry.get('image_file_path')
            return title, image_path
        else:
                return None, None

    
class SongImport:
    def __init__(self):
        pass

    # Funktion zum Lesen des Audios und Berechnen der Hashes
    def calculate_hashes(self, audio_file: BinaryIO) -> Optional[str]:
        """
        Liest das hochgeladene Audiodatei ein und berechnet die Hashes.

        Args:
            audio_file (BinaryIO): Hochgeladene Audiodatei.

        Returns:
            str: Hashes des Audios.
        """

        audio = audio_file.read()
        if audio_file is not None:
            # Speichern der Audiodatei temporär auf dem Server
            with wave.open("uploaded_audio.wav", "wb") as audio_f:
                audio_f.setnchannels(settings.NUM_CHANNELS)
                audio_f.setsampwidth(settings.BIT_DEPTH // 8)
                audio_f.setframerate(settings.SAMPLE_RATE)
                audio_f.setcomptype(settings.COMPRESSION_TYPE, 'NONE')
                audio_f.writeframes(audio)
            # Aufruf der read_in-Funktion mit dem Dateipfad
            hashes = read_in("uploaded_audio.wav")
        
            # Löschen der temporären Audiodatei
            os.remove("uploaded_audio.wav")
        
            return hashes
        else:
            return None
        
class SongDetector:
    def __init__(self):
        self.db = MultimediaDatabase

    def song_detecton():
        pass
    

# Uploading audio file
audio_file = st.file_uploader("Please upload an audio file.", type=[".mp3", ".wav", ".ogg"])


# Instanz der Multimedia-Datenbank erstellen
db = MultimediaDatabase()

# Button to start the recognition
if st.button("Start recognition"):
    if audio_file is not None:
        st.write("Recognition started...")
        # Calculate hashes of the uploaded audio
        song_import = SongImport()
        hashes = song_import.calculate_hashes(audio_file)
        if hashes:
            # Search for matching hashes in the database
            matching_id = db.find_matching_hashes(hashes)
            if matching_id:
                # Fetch title and image path from the database using the matching ID
                title, image_path = db.get_title_and_image_by_id(matching_id)
                if title and image_path:
                    st.write(f"Matching ID found in the database: {matching_id}")
                    st.write(f"Title: {title}")
                    st.image(image_path, caption='Album Cover', use_column_width=True)
                else:
                    st.write("Error retrieving title and image path from the database.")
            else:
                st.write("No matching entry found in the database.")
            st.write("Recognition finished!")
        else:
            st.write("Error")
    else:
        st.write("Please upload an audio file.")