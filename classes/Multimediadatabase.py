from tinydb import TinyDB, Query
import os
from typing import Optional, Tuple, List
import shutil

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