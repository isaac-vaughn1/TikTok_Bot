from gtts import gTTS
from moviepy.editor import *
import os
import random
from TikTokTTS import process_long_text
from dotenv import load_dotenv

load_dotenv()

session_id = os.getenv('SESSION_ID')

def create_video(audio_file: AudioFileClip, title: str):
    """
    Creates the final TikTok video using a background and audio file.

    This function gets a random mp4 from the folder of pre-downloaded mp4 files, trims it to match
    the length of the audio clip, saves the final product

    audio_file: A file containing a reddit story read by an AI voice
    title: A default title for each file; represents each story's index ikn the order it was retrieved
    """
    mp4_path = get_random_mp4()
    background = VideoFileClip(mp4_path)

    if background.duration < audio_file.duration:
        new_vid = background.loop(duration = audio_file.duration)
        new_vid = new_vid.set_audio(audio_file)

    else:
        start = random.randint(0, int(background.duration) - int(audio_file.duration))
        end = start + audio_file.duration
        new_vid = background.subclip(start, end)
        new_vid = new_vid.set_audio(audio_file)

    new_vid.write_videofile(f"{title}.mp4")
    background.close()
    new_vid.close()
    audio_file.close()
    os.remove(f"{title}.mp3")
    os.remove(f"{title}.txt")


def get_random_mp4():
    """
    Retrieves a random mp4 file from the Backgrounds folder

    Returns: a string representing the filepath to the chosen mp4
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join('Backgrounds', 'Minecraft.mp4')

    return os.path.join(base_dir, relative_path)


def create_audio_file(my_text: str, title: str):  
    """
    Using a TikTok TTS API wrapper, return an mp3 file of an AI voice reading Reddit stories

    my_text: The main body of the selected Reddit post
    title: A default title for each file; represents each story's index ikn the order it was retrieved

    Returns: The mp3 version of a Reddit post
    """
    f = open(f"{title}.txt", "w")
    f.write(my_text)
    f.close()

    text_speaker = "en_us_006"  # or any other voice code from constants.voices
    req_text = open(f"{title}.txt", 'r', errors='ignore', encoding='utf-8').read()
    filename = f"{title}.mp3"

    return process_long_text(session_id, text_speaker, req_text, filename)

