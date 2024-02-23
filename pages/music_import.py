import streamlit as st
from classes.Multimediadatabase import MultimediaDatabase
from classes.SongImport_SongDetector import SongImporter

# Klasse für die Main
class Main:
    def __init__(self) -> None:
        self.db = MultimediaDatabase()
        self.songimporter = SongImporter(self.db)

    def run(self) -> None:
        """Starte die Anwendung."""
        st.set_page_config(page_title="Music and Image Import", page_icon="🎵", layout="wide")
        st.title("Music import tool for adding new songs to the database")

        # Abschnitt zum Hochladen von Dateien und Metadaten
        st.subheader("Import a new song by uploading an audio and an image file. Choose a title, artist, and album for the song.")
        audio_file = st.file_uploader("Please upload an audio file.", type=[".wav"])
        image_file = st.file_uploader("Please upload an image file.", type=[".png", ".jpg", ".jpeg"])
        title = st.text_input("Enter the title of the song:")
        interpret = st.text_input("Enter the artist of the song:")
        album = st.text_input("Enter the albumname of the song:")
        if st.button("Start import"):
            st.write("Import started...")
            self.songimporter.upload_files(audio_file, image_file, title, interpret, album)
            st.write("Import finished!")

    
# Main
if __name__ == "__main__":
    main = Main()
    main.run()