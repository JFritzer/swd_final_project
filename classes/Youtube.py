from typing import Optional
from pytube import YouTube
from moviepy.editor import AudioFileClip

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
