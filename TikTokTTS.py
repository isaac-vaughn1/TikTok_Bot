import requests, base64, random, argparse, os, playsound, time, re, textwrap
from constants import voices
from moviepy.editor import *

API_BASE_URL = f"https://api16-normal-useast5.us.tiktokv.com/media/api/text/speech/invoke/"
USER_AGENT = f"com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)"


def tts(session_id: str, text_speaker: str = "en_us_002", req_text: str = "TikTok Text To Speech",
        filename: str = 'voice.mp3', play: bool = False):
    req_text = req_text.replace("+", "plus")
    req_text = req_text.replace(" ", "+")
    req_text = req_text.replace("&", "and")
    req_text = req_text.replace("ä", "ae")
    req_text = req_text.replace("ö", "oe")
    req_text = req_text.replace("ü", "ue")
    req_text = req_text.replace("ß", "ss")

    r = requests.post(
        f"{API_BASE_URL}?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0&aid=1233",
        headers={
            'User-Agent': USER_AGENT,
            'Cookie': f'sessionid={session_id}'
        }
    )

    if r.json()["message"] == "Couldn’t load speech. Try again.":
        output_data = {"status": "Session ID is invalid", "status_code": 5}
        print(output_data)
        return output_data

    vstr = [r.json()["data"]["v_str"]][0]
    msg = [r.json()["message"]][0]
    scode = [r.json()["status_code"]][0]
    log = [r.json()["extra"]["log_id"]][0]

    dur = [r.json()["data"]["duration"]][0]
    spkr = [r.json()["data"]["speaker"]][0]

    b64d = base64.b64decode(vstr)

    with open(filename, "wb") as out:
        out.write(b64d)

    output_data = {
        "status": msg.capitalize(),
        "status_code": scode,
        "duration": dur,
        "speaker": spkr,
        "log": log
    }

    print(output_data)

    if play is True:
        playsound.playsound(filename)
        os.remove(filename)

    return output_data


def batch_create(filename: str = 'voice.mp3'):
    out = open(filename, 'wb')

    def sorted_alphanumeric(data):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(data, key=alphanum_key)

    for item in sorted_alphanumeric(os.listdir('./batch/')):
        filestuff = open('./batch/' + item, 'rb').read()
        out.write(filestuff)

    out.close()


def randomvoice():
    count = random.randint(0, len(voices))
    text_speaker = voices[count]

    return text_speaker


def sampler():
    for item in voices:
        text_speaker = item
        filename = item
        print(item)
        req_text = 'TikTok Text To Speech Sample'
        tts(text_speaker, req_text, filename)


def process_long_text(session_id: str, text_speaker: str="en_us_006", req_text: str="Next time, provide some text", filename: str="voice.mp3"):
    """
    Splits long text by line, creating temporary audio files for each line

    session_id: a user's TikTok session ID cookie
    text_speaker: the desired AI voice for a recording
    req_text: text for the AI to read
    filename: the final mp3's filename

    Returns: A fully combined AudioFileClip()
    """
    words_per_chunk = 45
    words = req_text.split()
    temp_files = []

    for i in range(0, len(words), words_per_chunk):
        chunk = words[i:i + words_per_chunk]
        temp_filename = f"temp_audio_{i}.mp3"
        tts(session_id, text_speaker, " ".join(chunk), temp_filename)
        temp_files.append(temp_filename)

    return combine_audio(temp_files, filename)
    


def combine_audio(files: list, output_file: str="final.mp3"):
    """
    Combines all temporary audio files

    files: a list of the temporary files
    output_file: the name of our final mp3 file

    Returns: the combined AudioFileClip()
    """
    audio = [AudioFileClip(filename) for filename in files]

    combined_audio = concatenate_audioclips(audio)

    combined_audio.write_audiofile(output_file)

    for file in files:  # Clean up! Clean up! Everybody, everywhere!
        os.remove(file)

    return AudioFileClip(output_file)

# NOTE: tts() seems like it can only handle up to 49 words. Process the txt so it splits into groups of ~45 words for safe use