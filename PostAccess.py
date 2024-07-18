import praw
import os


client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
user_agent = os.getenv('USER_AGENT')


reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
)

subreddit = reddit.subreddit('AITAH')

for post in subreddit.top(limit=1):
    print(f"{post.title}\n{post.selftext}")