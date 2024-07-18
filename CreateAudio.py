from gtts import gTTS
import os

def CreateAudioFile(my_text, title):
    # type text: string
    # type title: string
    #rtype: no return type
    obj = myobj = gTTS(text=my_text, lang='en', slow=False)
    myobj.save(f"{title}.mp3")