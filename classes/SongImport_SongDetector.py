from classes.Multimediadatabase import MultimediaDatabase
from typing import BinaryIO, Union, Optional, Tuple
import os
import uuid
from pydub import AudioSegment
import settings
from music_analyzer import read_in, recognise_song
from tinydb import TinyDB
import concurrent.futures




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
            image = image_file.read()
            entry_id = str(uuid.uuid4())
            directory_audio = "Audio"
            os.makedirs(directory_audio, exist_ok=True)
            directory_image = "Image"
            os.makedirs(directory_image, exist_ok=True)
            
            audio_filename = os.path.join(directory_audio, f"{title}_{entry_id}.wav")
            with open(audio_filename, "wb") as f:
                f.write(audio_file.getbuffer())
            
            audio = AudioSegment.from_wav(audio_filename)
            audio = audio.set_channels(settings.NUM_CHANNELS)
            audio = audio.set_frame_rate(settings.SAMPLE_RATE)
            audio = audio.set_sample_width(settings.BIT_DEPTH // 8)
            audio.export(audio_filename, format="wav")

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
            # Es handelt sich um einen Dateipfad
            audio_filename = "uploaded_audio.wav"
            audio = AudioSegment.from_wav(audio_file)
            audio = audio.set_channels(settings.NUM_CHANNELS)
            audio = audio.set_frame_rate(settings.SAMPLE_RATE)
            audio = audio.set_sample_width(settings.BIT_DEPTH // 8)
            audio.export(audio_filename, format="wav")
        else:
            # Es handelt sich um ein Dateiobjekt
            audio_filename = "uploaded_audio.wav"
            with open(audio_filename, "wb") as f:
                f.write(audio_file.getbuffer())
            
            audio = AudioSegment.from_wav(audio_filename)
            audio = audio.set_channels(settings.NUM_CHANNELS)
            audio = audio.set_frame_rate(settings.SAMPLE_RATE)
            audio = audio.set_sample_width(settings.BIT_DEPTH // 8)
            audio.export(audio_filename, format="wav")
        
        # Aufruf der read_in-Funktion mit dem Dateipfad
        upload_hashes = read_in("uploaded_audio.wav")

        # Löschen der temporären Audiodatei
        os.remove("uploaded_audio.wav")

        return upload_hashes

        
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