import streamlit as st
from classes.Multimediadatabase import MultimediaDatabase
import os
from typing import List


# Vordefiniertes Passwort
PASSWORD: str = "1"

# Klasse für die Hauptanwendung
class Main:
    def __init__(self) -> None:
        self.db: MultimediaDatabase = MultimediaDatabase()
        
    def run(self) -> None:
        """Starte die Anwendung."""
        # Konfiguration der Streamlit-Seite
        st.set_page_config(page_title="Music and Image Import", page_icon="🎵", layout="wide")
        st.title("Tool for editing the database")

        # Passwort-Eingabefeld
        password: str = st.text_input("Enter password:", type="password")

        # Überprüfen, ob das eingegebene Passwort korrekt ist
        if password == PASSWORD:
            # Abschnitt für die Anzeige der vorhandenen Audiodateien im Dropdown-Menü
            st.subheader("Select an existing audio file:")
            audio_files: List[str] = os.listdir("Audio")
            audio_files: List[str] = [file for file in audio_files if file.endswith(".wav")]

            if not audio_files:
                st.write("No audio files found.")
            else:
                selected_audio_file: str = st.selectbox("Select audio file:", audio_files)
                audio_id: str = selected_audio_file.split("_")[1].split(".")[0]  # Extrahieren der ID aus dem Dateinamen
                title, image_path = self.db.get_title_and_image_by_id(audio_id)
                if title and image_path:
                    st.image(image_path)  # Anzeige des Albumcovers
                    audio_directory: str = "Audio"
                    selected_audio_path: str = os.path.join(audio_directory, selected_audio_file)
                    st.audio(selected_audio_path, format="audio/wav")  # Anzeige der Audiodatei
                    # Checkbox zum Bestätigen des Löschens
                    confirmation: bool = st.checkbox("Confirm Deletion")
                    # Button zum Löschen der Audio-Datei
                    if confirmation and st.button("Delete Audio File"):
                        self.db.delete_audio_file(audio_id)
                        st.success("Audio file and associated image deleted successfully.")
                        st.experimental_rerun()
            confirmation_all: bool = st.checkbox("Confirm Delete Everything")
            # Button zum Löschen der gesamten Datenbank
            if confirmation_all and st.button("Delete Everything"):
                self.db.delete_everything()
                st.success("Entire database, audio, and image files deleted successfully.")
                st.experimental_rerun()
        elif password != "":
            st.warning("Incorrect password. Please try again.")

# Hauptprogramm
if __name__ == "__main__":
    main: Main = Main()
    main.run()