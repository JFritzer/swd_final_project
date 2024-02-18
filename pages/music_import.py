import streamlit as st
from tinydb import TinyDB, Query
import os
import uuid
from music_analyzer import read_in  
import wave
import settings  

# Klasse für die Multimedia-Datenbank
class MultimediaDatabase:
    def __init__(self, db_path: str = './db/multimedia_database.json') -> None:
        # Stellen Sie sicher, dass das Verzeichnis vorhanden ist
        db_dir = os.path.dirname(db_path)
        os.makedirs(db_dir, exist_ok=True)

        # Erstellen Sie die TinyDB-Instanz
        self.db = TinyDB(db_path)

    def insert_entry(self, entry_data: dict) -> None:
        """Füge einen Eintrag in die Datenbank ein."""
        self.db.insert(entry_data)

    def get_entry_by_id(self, entry_id: str) -> dict:
        """Hole einen Eintrag aus der Datenbank anhand der ID."""
        Entry = Query()
        return self.db.get(Entry.id == entry_id)

# Klasse für den Song-Import
class SongImporter:
    def __init__(self, database: MultimediaDatabase) -> None:
        self.database = database

    def upload_files(self, audio_file, image_file, title: str, interpret: str, album: str) -> None:
        """Lade Audio-, Bilddateien und hash hoch und füge sie in die Datenbank ein."""
        if audio_file is not None and image_file is not None:
            audio = audio_file.read()
            image = image_file.read()
            entry_id = str(uuid.uuid4())
            directory_audio = "Audio"
            os.makedirs(directory_audio, exist_ok=True)
            directory_image = "Image"
            os.makedirs(directory_image, exist_ok=True)
            audio_filename = os.path.join(directory_audio, f"{title}_{entry_id}.wav")
            with wave.open(audio_filename, 'w') as audio_f:
                audio_f.setnchannels(settings.NUM_CHANNELS)
                audio_f.setsampwidth(settings.BIT_DEPTH // 8)
                audio_f.setframerate(settings.SAMPLE_RATE)
                audio_f.setcomptype(settings.COMPRESSION_TYPE, 'NONE')
                audio_f.writeframes(audio)
            image_filename = os.path.join(directory_image, f"{title}_{entry_id}.png")
            with open(image_filename, 'wb') as image_f:
                image_f.write(image)
            hashes = read_in(audio_filename)
            self.database.insert_entry({'id': entry_id, 'type': 'multimedia', 'title': title, 'artist': interpret, 'album': album, 'audio_file_path': audio_filename, 'image_file_path': image_filename, 'hashes' : hashes})

# Klasse für die Main
class Main:
    def __init__(self) -> None:
        self.db = MultimediaDatabase()
        self.song_importer = SongImporter(self.db)

    def run(self) -> None:
        """Starte die Anwendung."""
        st.set_page_config(page_title="Music and Image Import", page_icon="🎵", layout="wide")
        st.title("Music import tool for adding new songs to the database")

        # Abschnitt zum Hochladen von Dateien und Metadaten
        st.subheader("Import a new song by uploading an audio and an image file. Choose a title, artist, and album for the song.")
        audio_file = st.file_uploader("Please upload an audio file.", type=[".wav"])
        image_file = st.file_uploader("Please upload an image file.", type=[".png"])
        title = st.text_input("Enter the title of the song:")
        interpret = st.text_input("Enter the artist of the song:")
        album = st.text_input("Enter the albumname of the song:")
        if st.button("Start import"):
            st.write("Import started...")
            self.song_importer.upload_files(audio_file, image_file, title, interpret, album)
            st.write("Import finished!")

        # Abschnitt zum Abrufen von Informationen über einen Song
        st.subheader("Fetch information about a song by entering the ID of the entry.")
        entry_id = st.text_input("Enter the ID of the entry:")
        if st.button("Fetch Information"):
            entry = self.db.get_entry_by_id(entry_id)
            if entry:
                st.write(f"Title: {entry['title']}")
                st.image(entry['image_file_path'], caption='Album Cover', use_column_width=True)
            else:
                st.write("Entry not found!")

# Main
if __name__ == "__main__":
    main = Main()
    main.run()