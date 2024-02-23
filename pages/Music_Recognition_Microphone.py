import streamlit as st
from st_audiorec import st_audiorec
from classes. Multimediadatabase import MultimediaDatabase
from classes.SongImport_SongDetector import SongDetector, SongImporter
import io

class Main:
    def __init__(self) -> None:
        self.db = MultimediaDatabase()
        self.songimporter = SongImporter(self.db)
        self.songdetector = SongDetector()

    def run(self) -> None:
        st.markdown("# Music recognition tool, using the microphone")
        st.write("Here you can record an recognize an audio file by using your microphone.")
        st.write("After you stop the recording, recognition will start automatically.")
        st.write("Press on reset before you use it.")
        #Full Recording device.
        wav_audio_data = st_audiorec() #This function gives you an audio data type byte back.

        if wav_audio_data is not None:
            st.write("Recognition started...")
            # Calculate hashes of the uploaded audio
            audio_file = io.BytesIO(wav_audio_data)
            hashes = self.songimporter.calculate_hashes(audio_file)
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
            st.write("Please record an audio file.")

if __name__=="__main__":
    main = Main()
    main.run()







#Some functions we dont use right now, but are maybe helpful in the future:

    
#If we want to save the audiofile as a file: (This might be useful if we use the microphone to record the audiofile)
#with open("audio_file.mp3", "wb") as f:
#    f.write(audio_file.getbuffer())





#Änderungen (ToDo):
    # Recognition Teil hier noch hinzufügen
    # Dropdown Menü wieder Datei auswählen und dann recognizen.








#Audio Recorder imported from: https://github.com/stefanrmmr/streamlit-audio-recorder