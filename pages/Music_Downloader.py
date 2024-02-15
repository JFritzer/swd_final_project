#Code muss noch in Seite implementiert werden.
#Grundsätzlich funktioniert der Download und die Umwandlung aber.
#Rein geht ein Link zu einem YouTube-Video und raus kommt eine MP3-Datei.
#Das Ganze funktioniert über die Bibliotheken pytube und moviepy.
#Diese müssen noch in die requierements.txt eingetragen werden.

import streamlit as st
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
from typing import Optional  # Typ-Hinweis hinzugefügt


#Page header configuration:
st.set_page_config(page_title="Music Import", page_icon="🎵", layout="wide")

def download_video(url: str) -> Optional[str]:
    """
    Diese Funktion lädt ein YouTube-Video herunter und gibt den Dateinamen zurück.

    Args:
        url (str): Die URL des YouTube-Videos.

    Returns:
        Optional[str]: Der Dateiname des heruntergeladenen Videos, oder None, wenn ein Fehler auftritt.
    """
    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        video_file = video.download()
        return video_file
    except Exception as e:
        print("Error:", str(e))
        return None

def convert_to_mp3(video_file: str) -> Optional[str]:
    """
    Diese Funktion konvertiert ein Video in das MP3-Format und gibt den Dateinamen zurück.

    Args:
        video_file (str): Der Dateiname des heruntergeladenen Videos.

    Returns:
        Optional[str]: Der Dateiname der MP3-Datei, oder None, wenn ein Fehler auftritt.
    """
    try:
        video = VideoFileClip(video_file)
        mp3_file = video_file.replace('.mp4', '.mp3')
        video.audio.write_audiofile(mp3_file)
        video.close()
        return mp3_file
    except Exception as e:
        print("Error:", str(e))
        return None
        

def main():
    st.title("YouTube Video zu MP3 konvertieren")

    # URL-Eingabefeld
    url = st.text_input("Gib die URL des YouTube-Videos ein:")

    if st.button("Konvertieren"):
        st.write("Konvertierung wird durchgeführt...")
        video_file = download_video(url)
        if video_file:
            mp3_file = convert_to_mp3(video_file)
            if mp3_file:
                st.success(f"Das MP3 wurde erfolgreich heruntergeladen: {mp3_file}")
            else:
                st.error("Fehler beim Konvertieren in MP3.")
        else:
            st.error("Fehler beim Herunterladen des Videos.")

if __name__ == "__main__":
    main()