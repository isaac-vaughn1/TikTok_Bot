from dotenv import load_dotenv
import praw
import os
from CreateAudio import *



load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
user_agent = os.getenv('USER_AGENT')


reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
)

subreddit = reddit.subreddit('AITAH')

for i, post in enumerate(subreddit.top(limit=1)):
    CreateAudioFile(post.title + post.selftext, f"{i}")
