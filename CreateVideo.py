from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.config import change_settings
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
magick_path = os.getenv('MAGICK_PATH')

change_settings({"IMAGEMAGICK_BINARY": magick_path})

def create_video(audio_file: AudioFileClip, title: str):
    """
    Creates the final TikTok video using a background and audio file.

    This function gets a random YouTube video from the Backgrounds.txt, trims it to match
    the length of the audio clip, creates an srt file, overlays the subtitles, and saves the final product

    audio_file: A file containing a reddit story read by an AI voice
    title: A default title for each file; represents each story's index ikn the order it was retrieved
    """

    # Load the Whisper model for subtitle generation
    model = whisper.load_model("base")
    result = model.transcribe(f"{title}.mp3")
    srt_content = create_srt(result)

    try:
        with open(f'{title}.srt', 'w') as srt_file:
            srt_file.write(srt_content)
    except FileNotFoundError:
        print(f"File {title}.srt not found")
    except Exception as e:
        print(f"Looks like we have an error: {e}")

    mp4_path = get_random_mp4()
    background = VideoFileClip(mp4_path)

    # Ensure the background runs for the length of the audio
    if background.duration < audio_file.duration:
        new_vid = background.loop(duration = audio_file.duration)
        new_vid = new_vid.set_audio(audio_file)

    else:
        start = random.randint(0, int(background.duration) - int(audio_file.duration))
        end = start + audio_file.duration
        new_vid = background.subclip(start, end)
        new_vid = new_vid.set_audio(audio_file)
    
    # SUBTITLES!!
    generator = lambda txt: TextClip(txt, font='Arial-Bold', fontsize=50, color='white', stroke_color='black', stroke_width=2)
    sub = SubtitlesClip(f"{title}.srt", generator)
    final_vid = CompositeVideoClip([new_vid, sub.set_position('center')])

    final_vid.write_videofile(f"{title}.mp4")
    background.close()
    new_vid.close()
    audio_file.close()
    os.remove(f"{title}.mp3")
    os.remove(f"{title}.txt")
    os.remove(f"{title}.srt")
    os.remove(mp4_path)
    print('DING! Fries are done!')


def get_random_mp4(title: str="BackgroundMP4.mp4"):
    """
    Retrieves a random YouTube link from Backgrounds.txt and downloads the video at the end of said link

    Returns: a string representing the filepath to the chosen mp4
    """
    try:
        with open("Backgrounds.txt", "r") as f:
            links = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print("File Backgrounds.txt not found")
    except Exception as e:
        print(f"Looks like we have an error: {e}")

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
    try:
        f = open(f"{title}.txt", "w")
        f.write(my_text)
        f.close()
    except FileNotFoundError:
        print(f"File {title}.txt not found")
    except Exception as e:
        print(f"Error using {title}.txt: {e}")

    text_speaker = "en_us_006"  # or any other voice code from constants.voices
    req_text = open(f"{title}.txt", 'r', errors='ignore', encoding='utf-8').read()
    filename = f"{title}.mp3"

    return process_long_text(session_id, text_speaker, req_text, filename)

def create_srt(transcription: dict):
    """
    Uses the transcribed audio from Whisper API to create an SRT file which will display one word at a time 
    to keep the attention of TikTok users
    
    Transcription: a dictionary with transcription info on our audio file returned by the Whisper API.
    
    Returns: the srt content in the form of a string.
    """
    srt = []
    index = 1

    for segment in transcription['segments']:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text'].strip()
        words = text.split()
        word_duration = (end_time - start_time) / len(words)

        for i in range(0, len(words), 2):
            word_start_time = start_time + i * word_duration
            word_end_time = word_start_time + 2 * word_duration

            start_time_str = str(datetime.timedelta(seconds=word_start_time))
            end_time_str = str(datetime.timedelta(seconds=word_end_time))

            start_parts = start_time_str.split('.')
            end_parts = end_time_str.split('.')

            start_time_str = start_parts[0] + (',' + start_parts[1][:3] if len(start_parts) > 1 else ',000')
            end_time_str = end_parts[0] + (',' + end_parts[1][:3] if len(end_parts) > 1 else ',000')

            # Combine the current word and the next word (if exists)
            combined_words = ' '.join(words[i:i+2])
            
            srt.append(f"{index}\n{start_time_str} --> {end_time_str}\n{combined_words}\n\n")
            index += 1

    return ''.join(srt)