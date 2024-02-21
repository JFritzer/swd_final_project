from tinydb import TinyDB, Query
import os
from typing import Optional, BinaryIO, Tuple
import uuid
from music_analyzer import read_in  
from music_analyzer import recognise_song 
import wave
import settings  
from pytube import YouTube
from moviepy.editor import AudioFileClip

# Klasse für die Multimedia-Datenbank
class MultimediaDatabase:
    def __init__(self, db_path: str = './db/multimedia_database.json') -> None:
        # Stellen Sie sicher, dass das Verzeichnis vorhanden ist
        db_dir = os.path.dirname(db_path)
        os.makedirs(db_dir, exist_ok=True)

        # Erstellen Sie die TinyDB-Instanz
        self.db = TinyDB(db_path)

    def insert_entry(self, entry_data: dict) -> None:
        """Füge einen Eintrag in die Datenbank ein."""
        self.db.insert(entry_data)

    def get_entry_by_id(self, entry_id: str) -> dict:
        """Hole einen Eintrag aus der Datenbank anhand der ID."""
        Entry = Query()
        return self.db.get(Entry.id == entry_id)
    
    def get_hahes_out_database(self):
        entry_ids = []
        hashes = []
        for entry in self.db.all():
            entry_ids.append(entry.get('id'))
            hashes.append(entry.get('hashes'))

        return entry_ids, hashes
        
    def get_title_and_image_by_id(self, entry_id: str) -> Optional[Tuple[str, str]]:
        """Holt den Titel und den Bildpfad eines Eintrags aus der Datenbank anhand der ID."""
        Entry = Query()
        entry = self.db.get(Entry.id == entry_id)
        if entry:
            title = entry.get('title')
            image_path = entry.get('image_file_path')
            return title, image_path
        else:
                return None, None

# Klasse für den Song-Import
class SongImporter:
    def __init__(self, database: MultimediaDatabase) -> None:
        self.database = database

    def upload_files(self, audio_file, image_file, title: str, interpret: str, album: str) -> None:
        """Lade Audio-, Bilddateien und hash hoch und füge sie in die Datenbank ein."""
        if audio_file is not None and image_file is not None:
            audio = audio_file.read()
            image = image_file.read()
            entry_id = str(uuid.uuid4())
            directory_audio = "Audio"
            os.makedirs(directory_audio, exist_ok=True)
            directory_image = "Image"
            os.makedirs(directory_image, exist_ok=True)
            audio_filename = os.path.join(directory_audio, f"{title}_{entry_id}.wav")
            with wave.open(audio_filename, 'w') as audio_f:
                audio_f.setnchannels(settings.NUM_CHANNELS)
                audio_f.setsampwidth(settings.BIT_DEPTH // 8)
                audio_f.setframerate(settings.SAMPLE_RATE)
                audio_f.setcomptype(settings.COMPRESSION_TYPE, 'NONE')
                audio_f.writeframes(audio)
            image_filename = os.path.join(directory_image, f"{title}_{entry_id}.png")
            with open(image_filename, 'wb') as image_f:
                image_f.write(image)
            hashes = read_in(audio_filename)
            self.database.insert_entry({'id': entry_id, 'type': 'multimedia', 'title': title, 'artist': interpret, 'album': album, 'audio_file_path': audio_filename, 'image_file_path': image_filename, 'hashes' : hashes})

    # Funktion zum Lesen des Audios und Berechnen der Hashes
    def calculate_hashes(self, audio_file: BinaryIO) -> Optional[str]:
        """
        Liest das hochgeladene Audiodatei ein und berechnet die Hashes.

        Args:
            audio_file (BinaryIO): Hochgeladene Audiodatei.

        Returns:
            str: Hashes des Audios.
        """
        # Überprüfen, ob audio_file ein Dateipfad oder ein Dateiobjekt ist
        if isinstance(audio_file, str):
            # Es handelt sich um einen Dateipfad
            audio_path = audio_file
            with open(audio_path, 'rb') as f:
                audio_data = f.read()
        else:
            # Es handelt sich um ein Dateiobjekt
            audio_data = audio_file.read()

        # Jetzt können Sie wie gewohnt mit den Audiodaten arbeiten
        if audio_data is not None:
            # Speichern der Audiodatei temporär auf dem Server
            with wave.open("uploaded_audio.wav", "wb") as audio_f:
                audio_f.setnchannels(settings.NUM_CHANNELS)
                audio_f.setsampwidth(settings.BIT_DEPTH // 8)
                audio_f.setframerate(settings.SAMPLE_RATE)
                audio_f.setcomptype(settings.COMPRESSION_TYPE, 'NONE')
                audio_f.writeframes(audio_data)

            # Aufruf der read_in-Funktion mit dem Dateipfad
            upload_hashes = read_in("uploaded_audio.wav")

            # Löschen der temporären Audiodatei
            os.remove("uploaded_audio.wav")

            return upload_hashes
        else:
            return None
        
class SongDetector:
    def __init__(self):
        self.db = TinyDB('./db/multimedia_database.json')

    def compare_songs(self, upload_hashes):
        max_matches = 0
        matching_song = None

        for entry in self.db.all():
            entry_id = entry.get('id')
            hashes = entry.get('hashes')

            num_matches = recognise_song(upload_hashes, hashes)
                        
            if num_matches > max_matches:
                max_matches = num_matches
                matching_song = entry_id

        return matching_song, max_matches
    
class Youtube:
    def __init__(self):
        pass

    def download_video(self, url: str) -> Optional[str]:
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


    def convert_mp4_to_wav(self, mp4_file: str, start_time: float, end_time: float) -> Optional[str]:
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