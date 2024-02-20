import streamlit as st
from pytube import YouTube
from moviepy.editor import AudioFileClip
from typing import Optional

# Seiteneinstellungen festlegen
st.set_page_config(page_title="Music Youtube download", page_icon="🎵", layout="wide")

def download_video(url: str) -> Optional[str]:
    """
    Lädt ein YouTube-Video herunter und gibt den Dateinamen zurück.

    Args:
        url (str): Die URL des YouTube-Videos.

    Returns:
        Optional[str]: Der Dateiname des heruntergeladenen Videos, oder None, wenn ein Fehler auftritt.
    """
    try:
        # YouTube-Videoobjekt erstellen
        yt = YouTube(url)
        # Nur den Audiostream auswählen
        video = yt.streams.filter(only_audio=True).first()
        # Video herunterladen und Dateinamen zurückgeben
        video_file = video.download()
        return video_file
    except Exception as e:
        print("Error:", str(e))
        return None

def convert_mp4_to_wav(mp4_file: str, start_time: float, end_time: float) -> Optional[str]:
    """
    Konvertiert eine MP4-Datei in das WAV-Format und schneidet sie entsprechend der angegebenen Start- und Endzeit zu.

    Args:
        mp4_file (str): Der Dateiname der MP4-Datei.
        start_time (float): Die Startzeit des Ausschnitts in Sekunden.
        end_time (float): Die Endzeit des Ausschnitts in Sekunden.

    Returns:
        Optional[str]: Der Dateiname der WAV-Datei, oder None, wenn ein Fehler auftritt.
    """
    try:
        # AudioFileClip-Objekt aus der MP4-Datei erstellen
        audio = AudioFileClip(mp4_file)
        
        # Wenn start_time und end_time 0 sind, die gesamte Datei kopieren
        if start_time == 0 and end_time == 0:
            wav_file = mp4_file.replace('.mp4', '.wav')
            audio.write_audiofile(wav_file)
            return wav_file
        
        # Ausschnitt zuschneiden
        audio = audio.subclip(start_time, end_time)
        
        # Dateinamen für die WAV-Datei erstellen
        wav_file = mp4_file.replace('.mp4', '.wav')
        
        # Audio in das WAV-Format konvertieren und WAV-Datei speichern
        audio.write_audiofile(wav_file)
        return wav_file
    except Exception as e:
        print("Error:", str(e))
        return None


def main():
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
        video_file = download_video(url)
        if video_file:
            # Video in WAV konvertieren und zuschneiden
            wav_file = convert_mp4_to_wav(video_file, start_time, end_time)
            if wav_file:
                st.success(f"Die WAV-Datei wurde erfolgreich erstellt: {wav_file}")
            else:
                st.error("Fehler beim Konvertieren in WAV.")
        else:
            st.error("Fehler beim Herunterladen des Videos.")

    st.write("Later on, you can choose a snippet from a youtube video and regocnise the music from it.")

if __name__ == "__main__":
    main()


#Was hier noch fehlt:
    
#Die Recognition fehlt noch.
    