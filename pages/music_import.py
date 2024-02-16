import streamlit as st
from tinydb import TinyDB, Query
from typing import Optional, BinaryIO
import uuid
import os
from music_analyzer import read_in
import wave
import settings

# Page header configuration:
st.set_page_config(page_title="Music and Image Import", page_icon="🎵", layout="wide")

# Markdown title for the app
st.markdown("# Music and Image import tool for database filling")

# Connect to the database
db = TinyDB('./db/multimedia_database.json')

def upload_files(audio_file: Optional[BinaryIO], image_file: Optional[BinaryIO], title: str, interpret: str, album: str) -> None:
    if audio_file is not None and image_file is not None:
        audio = audio_file.read()
        image = image_file.read()
        # Generating a unique ID for the entry
        entry_id = str(uuid.uuid4())
        # Create a directory with title and ID
        directory_audio = "Audio"
        os.makedirs(directory_audio, exist_ok=True)
        # Create a directory with Cover and ID
        directory_image = "Image"
        os.makedirs(directory_image, exist_ok=True)
        # Save audio file
        audio_filename = os.path.join(directory_audio, f"{title}_{entry_id}.wav")
        with wave.open(audio_filename, 'w') as audio_f:
            audio_f.setnchannels(settings.NUM_CHANNELS)
            audio_f.setsampwidth(settings.BIT_DEPTH // 8)
            audio_f.setframerate(settings.SAMPLE_RATE)
            audio_f.setcomptype(settings.COMPRESSION_TYPE, 'NONE')
            audio_f.writeframes(audio)
            
    
            # audio_f.write(audio)
        # Save image file
        image_filename = os.path.join(directory_image, f"{title}_{entry_id}.png")
        with open(image_filename, 'wb') as image_f:
            image_f.write(image)
        
        hashes = read_in(audio_filename)

        # Inserting audio file and image file data into the database
        db.insert({'id': entry_id, 'type': 'multimedia', 'title': title, 'artist': interpret, 'album': album, 'audio_file_path': audio_filename, 'image_file_path': image_filename, 'hashes' : hashes})
        
def get_info_by_id(entry_id: str) -> Optional[str]:
    """
    Function to retrieve the image file path by entry ID from the database.

    Parameters:
        entry_id (str): ID of the entry to retrieve.

    Returns:
        str or None: File path of the image, or None if entry not found.
    """
    Entry = Query()
    result = db.get(Entry.id == entry_id)
    if result:
        image_file_path = result.get('image_file_path')
        return image_file_path
    else:
        return None
    
def get_title_by_id(entry_id: str) -> Optional[str]:
    
    Entry = Query()
    result = db.get(Entry.id == entry_id)
    if result:
        title = result.get('title')
        return title
    else:
        return None

def main() -> None:
    # Uploading audio file
    audio_file = st.file_uploader("Please upload an audio file.", type=[".wav"])

    # Uploading image file
    image_file = st.file_uploader("Please upload an image file.", type=[".png"])

    # Text inputs for title, artist, and album
    title = st.text_input("Enter the title:")
    interpret = st.text_input("Enter the artist:")
    album = st.text_input("Enter the album:")

    # Start import button
    if st.button("Start import"):
        st.write("Import started...")
        # Importing the audio and image files into the database
        upload_files(audio_file, image_file, title, interpret, album)

        st.write("Import finished!")

    # Text input for entry ID
    entry_id = st.text_input("Enter the ID of the entry:")

    if st.button("Fetch Information"):
        # Get image file path from the database
        image_file_path = get_info_by_id(entry_id)
        if image_file_path:
            # Get the title from the database
            title = get_title_by_id(entry_id)
            st.write(f"Title: {title}")
            st.image(image_file_path, caption='Album Cover', use_column_width=True)
        else:
            st.write("Entry not found!")

if __name__ == "__main__":
    main()











