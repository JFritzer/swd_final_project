from distutils.command import upload
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

    def get_hahes_out_database(self):
        entry_ids = []
        hashes = []
        for entry in self.db.all():
            entry_ids.append(entry.get('id'))
            hashes.append(entry.get('hashes'))

        return entry_ids, hashes
        

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
            upload_hashes = read_in("uploaded_audio.wav")
        
            # Löschen der temporären Audiodatei
            os.remove("uploaded_audio.wav")
        
            return upload_hashes
        else:
            return None
        
class SongDetector:
    def __init__(self):
        self.db = TinyDB('./db/multimedia_database.json')

    def compare_songs(self, upload_hashes):
        max_matches = 0
        matching_song = None

        for entry in self.db.all():
            entry_id = entry.get('id')
            hashes = entry.get('hashes')

            num_matches = recognise_song(upload_hashes, hashes)
                        
            if num_matches > max_matches:
                max_matches = num_matches
                matching_song = entry_id

        return matching_song, max_matches

    
    

# Uploading audio file
audio_file = st.file_uploader("Please upload an audio file.", type=[".mp3", ".wav", ".ogg"])


# Instanz der Multimedia-Datenbank erstellen
db = MultimediaDatabase()

# Button to start the recognition
if st.button("Start recognition"):
    # for entry_id, hashes in db.get_hahes_out_database():
    #     print("Song ID:", entry_id)
    #     print("-" * 50)  # Trennlinie für bessere Lesbarkeit
    if audio_file is not None:
        st.write("Recognition started...")
        # Calculate hashes of the uploaded audio
        song_import = SongImport()
        hashes = song_import.calculate_hashes(audio_file)
        if hashes:
            # Call detect_song to find matching hashes in the database
            song_detector = SongDetector()
            matching_hashes_count = song_detector.compare_songs(hashes)
            
            # You can now use matching_hashes_count for further analysis or display
            st.write(f"Number of matching hashes found: {matching_hashes_count}")
            st.write(f"Song is : {db.get_title_and_image_by_id(matching_hashes_count[0])[0]}")
            # Other code for displaying results...
        else:
            st.write("Error")
    else:
        st.write("Please upload an audio file.")