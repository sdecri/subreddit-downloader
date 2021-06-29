import praw
from logger_manager import *

import PARAMETER

def create_user_agent(reddit_client_id, reddit_username):
    return 'python{}:v1 (by u/{})'.format(reddit_client_id, reddit_username)



def download():
    reddit = praw.Reddit(
        client_id=PARAMETER.REDDIT_CLIENT_ID,
        client_secret=PARAMETER.REDDIT_SECRET,
        user_agent=create_user_agent(PARAMETER.REDDIT_CLIENT_ID, PARAMETER.REDDIT_SECRET),
    )

    # log.info(reddit.read_only)

    subreddit = reddit.subreddit("sanfrancisco")

    log.info('> Subreddit display name: {}'.format(subreddit.display_name))
    log.info('> Subreddit title: {}'.format(subreddit.title))

