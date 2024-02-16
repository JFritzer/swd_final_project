import numpy as np
from scipy.io.wavfile import read
from scipy.signal import spectrogram
from math import sqrt
from stqdm import stqdm
import settings

def create_spectrum(file_path: str, spectrogram_resolution: float = settings.SPECTOGRAM_RES) -> tuple:
    """
    Create a spectrogram from a given audio file.
    
    Parameters
    ----------
    file_path: The path to the audio file.

    spectrogram_resolution: The resolution of the spectrogram.
    
    Returns
    -------
    frequencies: ndarray
        The frequencies of the spectrogram.

    segtimes: ndarray
        The time segments of the spectrogram.

    Sxx: ndarray
        The spectrogram.
    """
    sample_rate, new_sound = read(file_path)
    nperseg = int(sample_rate * spectrogram_resolution)
    frequencies, segtimes, Sxx = spectrogram(new_sound, sample_rate, nperseg=nperseg)

    return frequencies, segtimes, Sxx

def max_filter(Sxx, radius : int = settings.MAX_FILTER_RADIUS) -> np.ndarray:
    """
    Apply a max filter to the spectrogram.
    
    Parameters
    ----------
    Sxx: ndarray
        The spectrogram.
    
    radius: int
        The radius of the max filter.
    
    Returns
    -------
    Sxx: ndarray
        The filtered spectrogram.
    """
    padded_Sxx = np.pad(Sxx, pad_width=radius, mode = 'edge')

    new_Sxx = np.zeros_like(Sxx)

    for x in stqdm(range(new_Sxx.shape[0]), desc="Running max filter"):
        for y in range(new_Sxx.shape[1]):
            try:
                values = padded_Sxx[x:x+2*radius+1, y:y+2*radius+1]
                new_Sxx[x][y] = values.max()
            except:
                pass
    
    return new_Sxx

def peak_filter(Sxx, new_Sxx) -> np.ndarray:
    """
    Apply a peak filter to the spectrogram.
    
    Parameters
    ----------
    Sxx: ndarray
        The original spectrogram.
    
    new_Sxx: ndarray
        The filtered spectrogram.
    
    Returns
    -------
    peak_Sxx: ndarray
        The filtered spectrogram.
    """
    peak_Sxx = np.zeros_like(new_Sxx)

    for x in stqdm(range(new_Sxx.shape[0]), desc="Running peak filter"):
        for y in range(new_Sxx.shape[1]):
            if new_Sxx[x][y] == Sxx[x][y]:
                peak_Sxx[x][y] = 1

    return peak_Sxx

def create_peak_windows(peak_Sxx : np.ndarray, delta_x : int = settings.DELTA_X, delta_y : int = settings.DELTA_Y) -> dict:
    """
    Create a dictionary of peak windows.
    
    Parameters
    ----------
    peak_Sxx: ndarray
        The filtered spectrogram.
    
    delta_x: int
        The x dimension of the window.
    
    delta_y: int
        The y dimension of the window.
    
    Returns
    -------
    peak_dict: dict
        The dictionary of peak windows.
    """
    peak_dict = {}

    for x in stqdm(range(peak_Sxx.shape[0] - delta_x - 2), desc="Creating peak windows"):
        for y in range(peak_Sxx.shape[1] - delta_y):
            if peak_Sxx[x][y] == 1:
                search_window_x = x + 2
                search_window_y = y - (delta_y // 2)
                sub_points = []

                for i in range(search_window_x, search_window_x + delta_x):
                    for j in range(search_window_y, search_window_y + delta_y):
                        if peak_Sxx[i][j] == 1:
                            sub_points.append((i,j))

                if sub_points != []:
                    peak_dict[x,y] = sub_points

    return peak_dict

def create_hash_dict(peak_dict : dict, frequencies : np.ndarray, segtimes : np.ndarray) -> list:
    """
    Create a dictionary of hashes.
    
    Parameters
    ----------
    peak_dict: dict
        The dictionary of peak windows.
    
    frequencies: ndarray
        The frequencies of the spectrogram.
    
    segtimes: ndarray
        The time segments of the spectrogram.
    
    Returns
    -------
    hashes: list
        The list of hashes.    
    """
    hashes = []
    for key in stqdm(peak_dict, desc="Creating hash dictionary"):
        for value in peak_dict[key]:
            delta_time = sqrt(abs(segtimes[key[1]] - segtimes[value[1]]) + abs(frequencies[key[0]] - frequencies[value[0]]))
            hashes.append([segtimes[key[1]], hash((frequencies[key[0]], frequencies[value[0]], delta_time))])

    return hashes

def read_in(file_path : str) -> list:
    """
    Read in an audio file and create a dictionary of hashes.
    
    Parameters
    ----------
    file_path: str
        The path to the audio file.
    
    Returns
    -------
    hashes: list
        The list of hashes.
    """
    frequencies, segtimes, Sxx = create_spectrum(file_path)
    filtered_Sxx = max_filter(Sxx)
    peak_Sxx = peak_filter(Sxx, filtered_Sxx)
    peak_dict = create_peak_windows(peak_Sxx)
    hashes = create_hash_dict(peak_dict, frequencies, segtimes)
    
    return hashes

def recognise_song(song_recognise, song_compare) -> int:
    """
    Takes hashes of two songs and compares them to find the highest number of time deltas that match.

    Parameters
    ----------
    song_recognise: list
        The list of hashes of the song to be recognised.
    
    song_compare: list
        The list of hashes of the song to be compared.
    
    Returns
    -------
    max_count: int
        The maximum number of time deltas that match.
    """
    pass