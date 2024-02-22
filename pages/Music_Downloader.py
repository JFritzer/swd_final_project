import streamlit as st
from classes import Youtube, MultimediaDatabase, SongDetector, SongImporter


class Main:
    def __init__(self) -> None:
        self.youtube = Youtube()
        self.db = MultimediaDatabase()
        self.songdetector = SongDetector()
        self.songimport = SongImporter(self.db)

    def run(self) -> None:
        # Seiteneinstellungen festlegen
        st.set_page_config(page_title="Music Youtube download", page_icon="🎵", layout="wide")
        # Seitentitel
        st.title("YouTube Video convert to .wav file")
        st.subheader("Here you can download a youtube video and convert it to a wav file.")
        # Eingabefeld für die YouTube-URL
        url = st.text_input("URL from the youtube video:")
        # Start- und Endzeit für den Ausschnitt abfragen
        start_time = st.number_input("Starttime (in seconds):", min_value=0, value=0, step=1)
        end_time = st.number_input("Endtime (in secoonds):", min_value=0, value=0, step=1)
        # Button zum Starten der Konvertierung
        if st.button("Download and convert to .wav file"):
            st.write("Konvertierung wird durchgeführt...")
            # Video herunterladen
            print(url)
            video_file = self.youtube.download_video(url)
            if video_file:
                # Video in WAV konvertieren und zuschneiden
                wav_file = self.youtube.convert_mp4_to_wav(video_file, start_time, end_time)
                if wav_file:
                    st.success(f"Die WAV-Datei wurde erfolgreich erstellt: {wav_file}")
                else:
                    st.error("Fehler beim Konvertieren in WAV.")
            else:
                st.error("Fehler beim Herunterladen des Videos.")

        st.subheader("Afterwards you can analyze the song here:")

        # Uploading audio file
        audio_file_2 = st.file_uploader("Please upload an audio file.", type=[".mp3", ".wav", ".ogg"])
        # Button to start the recognition
        if st.button("Start recognition"):
            if audio_file_2 is not None:
                st.write("Recognition started...")
                # Calculate hashes of the uploaded audio
                hashes = self.songimport.calculate_hashes(audio_file_2)
                if hashes:
                    # Call detect_song to find matching hashes in the database
                    matching_hashes_count = self.songdetector.compare_songs(hashes)
                    # You can now use matching_hashes_count for further analysis or display
                    st.write(f"Number of matching hashes found: {matching_hashes_count}")
                    # Other code for displaying results...
                    entry = self.db.get_entry_by_id(matching_hashes_count[0])
                    if entry:
                        st.write(f"Title: {entry['title']}")
                        st.image(entry['image_file_path'], caption='Album Cover', use_column_width=True)
                    else:
                        st.write("Entry not found!")

                else:
                    st.write("Error")
            else:
                st.write("Please upload an audio file.")
    

if __name__ == "__main__":
    main = Main()
    main.run()



#To Do:
    #Between Youtube Download and Recognition there should be a dropdown menu where you can choose the downloaded song you want to recognize.
    

