from gtts import gTTS
from moviepy.editor import *
import os
import random

def CreateVideo(audio_file: AudioFileClip):
    mp4_path = GetRandomMP4()
    background = VideoFileClip(mp4_path)
    start = random.randint(0, int(background.duration) - int(audio_file.duration))
    end = start + audio_file.duration

    new_vid = background.subclip(start, end)

    new_vid = new_vid.set_audio(audio_file)

    new_vid.write_videofile("my_new_video.mp4", codec="libx264")
    background.close()
    new_vid.close()
    audio_file.close()

    
    

def GetRandomMP4():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join('Backgrounds', 'GTAV.mp4')

    return os.path.join(base_dir, relative_path)


def CreateAudioFile(my_text: str, title: str):  
    obj = gTTS(text=my_text, lang='en', tld='com.au')
    obj.save(f"{title}.mp3")

    return AudioFileClip(f"{title}.mp3")


