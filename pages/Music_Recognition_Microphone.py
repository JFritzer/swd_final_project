import streamlit as st
from st_audiorec import st_audiorec
from classes import MultimediaDatabase, SongDetector,SongImporter

class Main:
    def __init__(self) -> None:
        self.db = MultimediaDatabase()
        self.songimporter = SongImporter(self.db)
        self.songdetector = SongDetector()

    def run(self) -> None:
        st.markdown("# Music recognition tool, using the microphone")
        st.subheader("Here you can record an audiotrack and the program gives you the name of the song back.")
        #Full Recording device.
        wav_audio_data = st_audiorec()
        st.write("Right now, you only can record an audiofile. The recognition of the song is not implemented yet.")
        if wav_audio_data is not None:
            st.write("Recognition started...")
            # Calculate hashes of the uploaded audio
            hashes = self.songimporter.calculate_hashes(wav_audio_data)
            if hashes:
                #Call detect_song to find matching hashes in the database
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







#Some functions we dont use right now, but are maybe helpful in the future:

    
#If we want to save the audiofile as a file: (This might be useful if we use the microphone to record the audiofile)
#with open("audio_file.mp3", "wb") as f:
#    f.write(audio_file.getbuffer())





#Änderungen (ToDo):
    # Recognition Teil hier noch hinzufügen
    # Dropdown Menü wieder Datei auswählen und dann recognizen.








#Audio Recorder imported from: https://github.com/stefanrmmr/streamlit-audio-recorder