import sys

import praw
from psaw import PushshiftAPI
from logger_manager import *
import json

import PARAMETER


def create_user_agent(reddit_client_id, reddit_username):
    return 'python{}:v1 (by u/{})'.format(reddit_client_id, reddit_username)


def init_reddit_client():

    reddit = praw.Reddit(
        client_id=PARAMETER.REDDIT_CLIENT_ID,
        client_secret=PARAMETER.REDDIT_SECRET,
        user_agent=create_user_agent(PARAMETER.REDDIT_CLIENT_ID, PARAMETER.REDDIT_SECRET),
    )

    return reddit


def init_pushshift_client(reddit_client):
    return PushshiftAPI(reddit_client)


def download_submissions(pushshift_client, reddit_client, start_epoch, end_epoch):

    sub_generator = pushshift_client.search_submissions(
        subreddit=PARAMETER.SUBREDDIT,
        sort='asc',
        sort_type='created_utc',
        after=start_epoch,
        before=end_epoch,
        limit=PARAMETER.SUBMISSIONS_BATCH_SIZE,
        num_comments=">0"
    )

    last_submission = None
    num_downloaded_submissions = 0
    num_downloaded_comments = 0
    for sub in sub_generator:
        submission_info = {
            "id": sub.id,
            "created_utc": sub.created_utc,
            "num_comments": sub.num_comments,
            "title": sub.title.replace('\n', '\\n'),
            "permalink": sub.permalink,
            "score": sub.score,
            "url": sub.url
        }
        num_downloaded_submissions = num_downloaded_submissions + 1
        log.info(">> Submission info: {}".format(submission_info))

        submission = reddit_client.submission(id=sub.id)
        if submission is not None:
            num_comments = download_comments(sub, submission)
            num_downloaded_comments = num_downloaded_comments + num_comments

        last_submission = sub

    return last_submission, num_downloaded_submissions, num_downloaded_comments


def download_comments(sub, submission):
    log.info(">>> Downloading {} commments from submission {}".format(submission.num_comments, sub.id))
    submission.comments.replace_more(limit=None)
    num_downloaded_comments = 0
    for comment in submission.comments.list():
        num_downloaded_comments = num_downloaded_comments + 1
        comment_info = {
            "id": comment.id,
            "body": comment.body,
            "created_utc": int(comment.created_utc),
            "permalink": comment.permalink,
            "score": comment.score
        }
        if log.isEnabledFor(logging.DEBUG):
            log.debug(">>> Comment info: {}".format(comment_info))

    return num_downloaded_comments


def download():
    reddit_client = init_reddit_client()
    pushshift_client = init_pushshift_client(reddit_client)

    subreddit = reddit_client.subreddit(PARAMETER.SUBREDDIT)
    subreddit_info={
        "id": subreddit.id,
        "name": subreddit.name,
        "display_name": subreddit.display_name,
        "title": subreddit.title,
        "created_utc": subreddit.created_utc,
        "description": subreddit.description,
    }
    log.info(subreddit_info)

    start = PARAMETER.FROM_DATE
    end = PARAMETER.TO_DATE
    start_str = "the beginning"
    end_str = "the end"
    start_epoch = None
    end_epoch = None
    if start is not None:
        start_str = start.isoformat()
        start_epoch = int(start.timestamp())
    if end is not None:
        end_str = end.isoformat()
        end_epoch = int(end.timestamp())

    log.info("> Download submissions created from {} until {}".format(start_str, end_str))

    no_more_data = False

    num_iterations = PARAMETER.NUM_ITERATIONS

    step_counter = 1
    num_downloaded_submissions = 0
    num_downloaded_comments = 0
    while not no_more_data and (num_iterations < 0 or step_counter <= num_iterations):

        log.info("> Step {}: from_timestamp: {}, to_timestamp: {}".format(step_counter, start_epoch, end_epoch))
        last_submission, num_submissions, num_downloaded_comments = download_submissions(pushshift_client, reddit_client, start_epoch, end_epoch)
        num_downloaded_submissions = num_downloaded_submissions + num_submissions

        step_counter = step_counter + 1
        if last_submission is None:
            no_more_data = True
        else:
            start_epoch = int(last_submission.created_utc)

    log.info("Downloaded {} submissions".format(num_downloaded_submissions))
    log.info("Downloaded {} comments".format(num_downloaded_comments))
    log.info('finished downloading')
