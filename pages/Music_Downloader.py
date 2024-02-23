import streamlit as st
from classes.Multimediadatabase import MultimediaDatabase
from classes.SongImport_SongDetector import SongDetector,SongImporter
from classes.Youtube import Youtube

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
        if st.button("Download and recognize the audio"):
            st.write("Converting the video...")
            # Video herunterladen
            print(url)
            video_file = self.youtube.download_video(url)
            if video_file:
                # Video in WAV konvertieren und zuschneiden
                wav_file = self.youtube.convert_mp4_to_wav(video_file, start_time, end_time)
                if wav_file:
                    st.success(f"Converting the downloaded video was sucessful: {wav_file}")
                    st.write("Recognition started...")
                    # Calculate hashes of the uploaded audio
                    hashes = self.songimport.calculate_hashes(wav_file)
                    if hashes:
                    # Call detect_song to find matching hashes in the database
                        matching_hashes_count = self.songdetector.compare_songs(hashes)
                    # You can now use matching_hashes_count for further analysis or display
                        st.write(f"Number of matching hashes found: {matching_hashes_count}")
                    # Other code for displaying results...
                        entry = self.db.get_entry_by_id(matching_hashes_count[0])
                        if entry:
                            st.write(f"Title: {entry['title']}")
                            st.image(entry['image_file_path'], caption='Album Cover',width=500)
                        else:
                            st.write("Entry not found!")
                    else:
                        st.write("Entry not found")
                else:
                    st.error("Error converting mp4 to wav.")
            else:
                st.error("Error during download the video.")




    

if __name__ == "__main__":
    main = Main()
    main.run()



#Änderungen (ToDo):
    #Die MP4 Datei und die wav datei soll nach dem download gelöscht werden.
    #Sie sollen in einem temporären Ordner gespeichert werden.
    

