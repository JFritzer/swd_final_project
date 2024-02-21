import streamlit as st
from classes import Youtube, MultimediaDatabase, SongDetector, SongImporter


class Main:
    def __init__(self) -> None:
        self.youtube = Youtube()
        self.db = MultimediaDatabase()
        self.songdetector = SongDetector()
        self.songimporter = SongImporter(self.db)

    def run(self) -> None:
        # Seiteneinstellungen festlegen
        st.set_page_config(page_title="Music Youtube download", page_icon="🎵", layout="wide")
        # Seitentitel
        st.title("YouTube Video zu WAV konvertieren")
        st.subheader("Here you can download a youtube video and convert it to a wav file.")
        # Eingabefeld für die YouTube-URL
        url = st.text_input("Gib die URL des YouTube-Videos ein:")
        # Start- und Endzeit für den Ausschnitt abfragen
        start_time = st.number_input("Startzeit des Ausschnitts (in Sekunden):", min_value=0, value=0, step=1)
        end_time = st.number_input("Endzeit des Ausschnitts (in Sekunden):", min_value=0, value=0, step=1)
        # Button zum Starten der Konvertierung
        if st.button("Konvertieren"):
            st.write("Konvertierung wird durchgeführt...")
            # Video herunterladen
            print(url)
            video_file = self.youtube.download_video(url)
            if video_file:
                # Video in WAV konvertieren und zuschneiden
                wav_file = self.youtube.convert_mp4_to_wav(video_file, start_time, end_time)
                if wav_file:
                    st.success(f"Die WAV-Datei wurde erfolgreich erstellt: {wav_file}")
                    st.write("Recognition started...")
                    # Calculate hashes of the uploaded audio
                    hashes = self.songimporter.calculate_hashes(wav_file)
                    if hashes:
                        # Call detect_song to find matching hashes in the database
                        matching_hashes_count = self.songdetector.compare_songs(hashes)
                        # You can now use matching_hashes_count for further analysis or display
                        st.write(f"Number of matching hashes found: {matching_hashes_count}")
                        st.write(f"Song is : {self.db.get_title_and_image_by_id(matching_hashes_count[0])[0]}")
                        # Other code for displaying results...
                    else:
                        st.error("Fehler")
                else:
                    st.error("Fehler beim Konvertieren in WAV.")
            else:
                st.error("Fehler beim Herunterladen des Videos.")

        st.write("Later on, you can choose a snippet from a youtube video and regocnise the music from it.")

if __name__ == "__main__":
    main = Main()
    main.run()


