from gtts import gTTS
from moviepy.editor import *
import os
import random

def create_video(audio_file: AudioFileClip, title: str):
    """
    Creates the final TikTok video using a background and audio file.

    The function gets a random mp4 from the folder of pre-downloaded mp4 files, trims it to match
    the length of the audio clip, saves the final product

    audio_file: A file containing a reddit story read by an AI voice
    title: A default title for each file; represents each story's index ikn the order it was retrieved
    """
    mp4_path = get_random_mp4()
    background = VideoFileClip(mp4_path)

    start = random.randint(0, int(background.duration) - int(audio_file.duration))
    end = start + audio_file.duration

    new_vid = background.subclip(start, end)
    new_vid = new_vid.set_audio(audio_file)

    new_vid.write_videofile(f"{title}.mp4")
    background.close()
    new_vid.close()
    audio_file.close()
    os.remove(f"{title}.mp3")

    

def get_random_mp4():
    """
    Retrieves a random mp4 file from the Backgrounds folder

    Returns: a string representing the filepath to the chosen mp4
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join('Backgrounds', 'GTAV.mp4')

    return os.path.join(base_dir, relative_path)


def create_audio_file(my_text: str, title: str):  
    """
    Using gTTS, creates an mp3 of an AI voice reading a selected Reddit story

    my_text: The main body of the selected Reddit post
    title: A default title for each file; represents each story's index ikn the order it was retrieved

    Returns: The mp3 version of a Reddit post
    """
    obj = gTTS(text=my_text, lang='en', tld='com.au')
    obj.save(f"{title}.mp3")
    
    return AudioFileClip(f"{title}.mp3")


