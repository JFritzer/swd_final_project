#Code muss noch in Seite implementiert werden.
#Grundsätzlich funktioniert der Download und die Umwandlung aber.
#Rein geht ein Link zu einem YouTube-Video und raus kommt eine MP3-Datei.
#Das Ganze funktioniert über die Bibliotheken pytube und moviepy.
#Diese müssen noch in die requierements.txt eingetragen werden.

from pytube import YouTube
from moviepy.editor import *

def download_video(url):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        video_file = video.download()
        return video_file
    except Exception as e:
        print("Error:", str(e))
        return None

def convert_to_mp3(video_file):
    try:
        video = AudioFileClip(video_file)
        mp3_file = video_file.replace('.mp4', '.mp3')
        video.write_audiofile(mp3_file)
        video.close()
        return mp3_file
    except Exception as e:
        print("Error:", str(e))
        return None

def main():
    url = input("Gib die URL des YouTube-Videos ein: ")
    video_file = download_video(url)
    if video_file:
        mp3_file = convert_to_mp3(video_file)
        if mp3_file:
            print("Das MP3 wurde erfolgreich heruntergeladen:", mp3_file)
        else:
            print("Fehler beim Konvertieren in MP3.")
    else:
        print("Fehler beim Herunterladen des Videos.")

if __name__ == "__main__":
    main()