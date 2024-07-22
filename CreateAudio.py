from gtts import gTTS
import os

def CreateAudioFile(my_text: str, title: str):
    obj = myobj = gTTS(text=my_text, lang='en', tld='com.au')
    myobj.save(f"{title}.mp3")