from gtts import gTTS
from moviepy.editor import *
import os
import random
from TikTokTTS import process_long_text
from pytubefix import YouTube
from pytubefix.cli import on_progress
import whisper
import datetime
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

    # Load the Whisper model for subtitle generation
    model = whisper.load_model("base")
    result = model.transcribe(f"{title}.mp3")
    srt_content = create_srt(result)

    with open(f'{title}.srt', 'w') as srt_file:
        srt_file.write(srt_content)

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
    os.remove(mp4_path)


def get_random_mp4(title: str="BackgroundMP4.mp4"):
    """
    Retrieves a random YouTube link from Backgrounds.txt and downloads the video at the end of said link

    Returns: a string representing the filepath to the chosen mp4
    """
    with open("Backgrounds.txt", "r") as f:
        links = [line.strip() for line in f.readlines()]

    yt = YouTube(random.choice(links), on_progress_callback = on_progress)
    yt = yt.streams.get_highest_resolution()
    yt.download(filename=title)

    file_path = os.path.abspath(title)

    return file_path


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

def create_srt(transcription: dict):
    """
    Uses the transcribed audio from Whisper API to create an srt file for later subtitle creation

    transcription: a dictionary with transcription info on our audio file returned by the Whisper API

    Returns: the srt content in the form of a string
    """
    srt = []
    for i, segment in enumerate(transcription['segments']):
        start_time = str(datetime.timedelta(seconds=segment['start']))
        end_time = str(datetime.timedelta(seconds=segment['end']))
        text = segment['text'].strip()
        
        start_parts = start_time.split('.')
        end_parts = end_time.split('.')
        
        start_time = start_parts[0] + (',' + start_parts[1][:3] if len(start_parts) > 1 else ',000')
        end_time = end_parts[0] + (',' + end_parts[1][:3] if len(end_parts) > 1 else ',000')
        
        srt.append(f"{i+1}\n{start_time} --> {end_time}\n{text}\n")
    return ''.join(srt)