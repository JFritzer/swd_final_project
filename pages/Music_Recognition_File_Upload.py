import streamlit as st
from classes import MultimediaDatabase
from classes import SongImporter
from classes import SongDetector

class Main:
    def __init__(self)->None:
        self.db = MultimediaDatabase()
        self.songimport = SongImporter(self.db)
        self.songdetector = SongDetector()

    def run(self)-> None:
        st.set_page_config(page_title="Music Recognition", page_icon="🎵", layout="wide")
        st.markdown("# Music recognition tool, using file upload")
        st.subheader("Here you can upload your file and the program gives you the name of the song back.")
        # Uploading audio file
        audio_file = st.file_uploader("Please upload an audio file.", type=[".mp3", ".wav", ".ogg"])
        # Button to start the recognition
        if st.button("Start recognition"):
            if audio_file is not None:
                st.write("Recognition started...")
                # Calculate hashes of the uploaded audio
                hashes = self.songimport.calculate_hashes(audio_file)
                if hashes:
                    # Call detect_song to find matching hashes in the database
                    matching_hashes_count = self.songdetector.compare_songs(hashes)
                    # You can now use matching_hashes_count for further analysis or display
                    st.write(f"Number of matching hashes found: {matching_hashes_count}")
                    st.write(f"Song is : {self.db.get_title_and_image_by_id(matching_hashes_count[0])[0]}")
                    # Other code for displaying results...
                else:
                    st.write("Error")
            else:
                st.write("Please upload an audio file.")

if __name__=="__main__":
    main = Main()
    main.run()