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
import concurrent.futures
import shutil
from typing import List, Union

class MultimediaDatabase:
    def __init__(self, db_path: str = './db/multimedia_database.json') -> None:
        """
        Initialize the MultimediaDatabase class.

        Args:
            db_path (str, optional): Path to the database file. Defaults to './db/multimedia_database.json'.
        """
        # Ensure the directory exists
        db_dir = os.path.dirname(db_path)
        os.makedirs(db_dir, exist_ok=True)
        self.db_path = db_path
        # Create the TinyDB instance
        self.db = TinyDB(db_path)

    def insert_entry(self, entry_data: dict) -> None:
        """
        Insert an entry into the database.

        Args:
            entry_data (dict): Data of the entry to be inserted.
        """
        self.db.insert(entry_data)

    def get_entry_by_id(self, entry_id: str) -> dict:
        """
        Get an entry from the database by its ID.

        Args:
            entry_id (str): ID of the entry to retrieve.

        Returns:
            dict: Data of the retrieved entry.
        """
        Entry = Query()
        return self.db.get(Entry.id == entry_id)
    
    def get_hashes_from_database(self) -> Tuple[List[str], List[str]]:
        """
        Get all entry IDs and their corresponding hashes from the database.

        Returns:
            Tuple[List[str], List[str]]: Tuple containing lists of entry IDs and hashes.
        """
        entry_ids = []
        hashes = []
        for entry in self.db.all():
            entry_ids.append(entry.get('id'))
            hashes.append(entry.get('hashes'))

        return entry_ids, hashes
        
    def get_title_and_image_by_id(self, entry_id: str) -> Optional[Tuple[str, str]]:
        """
        Get the title and image path of an entry from the database by its ID.

        Args:
            entry_id (str): ID of the entry to retrieve.

        Returns:
            Optional[Tuple[str, str]]: Tuple containing title and image path, or None if entry not found.
        """
        Entry = Query()
        entry = self.db.get(Entry.id == entry_id)
        if entry:
            title = entry.get('title')
            image_path = entry.get('image_file_path')
            return title, image_path
        else:
            return None, None
        
    def delete_audio_file(self, audio_id: str) -> None:
        """
        Delete an audio file, its associated image, and the entry from the database.

        Args:
            audio_id (str): ID of the audio file.
        """
        # Get title and image path
        title, image_path = self.get_title_and_image_by_id(audio_id)
        # Remove entry from the database
        self.db.remove(Query().id == audio_id)
    
        # Delete image and audio file
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
    
        audio_directory = "Audio"
        audio_file = f"{title}_{audio_id}.wav"
        audio_path = os.path.join(audio_directory, audio_file)
        if os.path.exists(audio_path):
            os.remove(audio_path)

        # Also remove the image file if exists
        image_directory = "Image"
        image_file = f"{title}_{audio_id}.png"
        image_path = os.path.join(image_directory, image_file)
        if os.path.exists(image_path):
            os.remove(image_path)
            
    def delete_everything(self) -> None:
        """
        Delete all entries from the database and all audio and image files.
        """
        # Remove all entries from the database
        self.db.truncate()
        # Delete the Audio and Image directories
        audio_dir = "Audio"
        image_dir = "Image"
        shutil.rmtree(audio_dir, ignore_errors=True)
        shutil.rmtree(image_dir, ignore_errors=True)

class SongImporter:
    def __init__(self, database: MultimediaDatabase) -> None:
        """
        Initialize the SongImporter class.

        Args:
            database (MultimediaDatabase): The database instance to interact with.
        """
        self.database = database

    def upload_files(self, audio_file: BinaryIO, image_file: BinaryIO, title: str, interpret: str, album: str) -> None:
        """
        Upload audio and image files, calculate hashes, and insert them into the database.

        Args:
            audio_file (BinaryIO): Binary file object of the audio.
            image_file (BinaryIO): Binary file object of the image.
            title (str): Title of the multimedia file.
            interpret (str): Artist name.
            album (str): Album name.
        """
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

    def calculate_hashes(self, audio_file: Union[str, BinaryIO]) -> Optional[str]:
        """
        Calculate hashes of the uploaded audio file.

        Args:
            audio_file (Union[str, BinaryIO]): File path or binary file object of the audio.

        Returns:
            Optional[str]: Calculated hashes of the audio.
        """
        if isinstance(audio_file, str):
            audio_path = audio_file
            with open(audio_path, 'rb') as f:
                audio_data = f.read()
        else:
            audio_data = audio_file.read()

        if audio_data is not None:
            with wave.open("uploaded_audio.wav", "wb") as audio_f:
                audio_f.setnchannels(settings.NUM_CHANNELS)
                audio_f.setsampwidth(settings.BIT_DEPTH // 8)
                audio_f.setframerate(settings.SAMPLE_RATE)
                audio_f.setcomptype(settings.COMPRESSION_TYPE, 'NONE')
                audio_f.writeframes(audio_data)

            upload_hashes = read_in("uploaded_audio.wav")

            os.remove("uploaded_audio.wav")

            return upload_hashes
        else:
            return None
      
class SongDetector:
    def __init__(self, database_path: str = './db/multimedia_database.json') -> None:
        """
        Initialize the SongDetector class.

        Args:
            database_path (str): Path to the multimedia database.
        """
        self.db = TinyDB(database_path)

    def compare_songs(self, upload_hashes: str, max_workers: int = settings.MAX_WORKERS) -> Tuple[Optional[str], int]:
        """
        Compare uploaded hashes with hashes in the database to find the matching song.

        Args:
            upload_hashes (str): Hashes of the uploaded audio.
            max_workers (int, optional): Maximum number of concurrent workers. Defaults to settings.MAX_WORKERS.

        Returns:
            Tuple[Optional[str], int]: ID of the matching song and number of matches.
        """
        max_matches = 0
        matching_song = None

        def recognise_song_wrapper(upload_hashes: str, hashes: str) -> int:
            """
            Wrapper function to call the recognise_song function with the specified hashes.

            Args:
                upload_hashes (str): Hashes of the uploaded audio.
                hashes (str): Hashes of a song in the database.

            Returns:
                int: Number of matches.
            """
            return recognise_song(upload_hashes, hashes)

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submitting tasks for each entry in the database
            future_to_entry = {executor.submit(recognise_song_wrapper, upload_hashes, entry.get('hashes')): entry for entry in self.db.all()}

            # Iterating through completed futures
            for future in concurrent.futures.as_completed(future_to_entry):
                entry = future_to_entry[future]
                entry_id = entry.get('id')
                num_matches = future.result()

                if num_matches > max_matches:
                    max_matches = num_matches
                    matching_song = entry_id

        return matching_song, max_matches
    
class Youtube:
    def __init__(self) -> None:
        """Initialize the Youtube class."""
        pass

    def download_video(self, url: str) -> Optional[str]:
        """
        Download a YouTube video and return the filename.

        Args:
            url (str): The URL of the YouTube video.

        Returns:
            Optional[str]: The filename of the downloaded video, or None if an error occurs.
        """
        try:
            # Create YouTube video object
            yt = YouTube(url)
            # Select only the audio stream
            video = yt.streams.filter(only_audio=True).first()
            # Download video and return filename
            video_file = video.download()
            return video_file
        except Exception as e:
            print("Error:", str(e))
            return None


    def convert_mp4_to_wav(self, mp4_file: str, start_time: float, end_time: float) -> Optional[str]:
        """
        Convert an MP4 file to WAV format and trim it according to the specified start and end times.

        Args:
            mp4_file (str): The filename of the MP4 file.
            start_time (float): The start time of the clip in seconds.
            end_time (float): The end time of the clip in seconds.

        Returns:
            Optional[str]: The filename of the WAV file, or None if an error occurs.
        """
        try:
            # Create AudioFileClip object from the MP4 file
            audio = AudioFileClip(mp4_file)
        
            # If start_time and end_time are 0, copy the entire file
            if start_time == 0 and end_time == 0:
                wav_file = mp4_file.replace('.mp4', '.wav')
                audio.write_audiofile(wav_file)
                return wav_file
        
            # Trim the clip
            audio = audio.subclip(start_time, end_time)
        
            # Create filename for the WAV file
            wav_file = mp4_file.replace('.mp4', '.wav')
        
            # Convert audio to WAV format and save WAV file
            audio.write_audiofile(wav_file)
            return wav_file
        except Exception as e:
            print("Error:", str(e))
            return None
