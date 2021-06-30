import praw
from psaw import PushshiftAPI
import mysql.connector

from logger_manager import *
import PARAMETER

TABLE_SUBREDDIT = "subreddit"
TABLE_SUBMISSION = "submission"
TABLE_COMMENT = "comment"


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


def persist_single_row(connection, table, info):
    cursor = None
    try:
        cursor = connection.cursor()
        values = ', '.join("'" + str(x).replace("'", "\\'") + "'" for x in info.values())
        sql = "INSERT INTO %s VALUES (%s)" % (table, values)
        if log.isEnabledFor(logging.DEBUG):
            log.debug("Executing sql: {}".format(sql))
        cursor.execute(sql)
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()


def download_submissions(subreddit_id, pushshift_client, reddit_client, connection, start_epoch, end_epoch):
    sub_generator = pushshift_client.search_submissions(
        subreddit=PARAMETER.SUBREDDIT,
        sort='asc',
        sort_type='created_utc',
        after=start_epoch,
        before=end_epoch,
        limit=PARAMETER.SUBMISSIONS_BATCH_SIZE,
    )
    # num_comments=">0"

    last_submission = None
    num_downloaded_submissions = 0
    num_downloaded_comments = 0
    for sub in sub_generator:
        submission_info = {
            "id": sub.id,
            "subreddit": subreddit_id,
            "created_utc": int(sub.created_utc),
            "score": int(sub.score),
            "title": sub.title,
            "num_comments": int(sub.num_comments),
            "permalink": sub.permalink,
            "url": sub.url
        }
        num_downloaded_submissions = num_downloaded_submissions + 1
        log.info(">> Submission info: {}".format(submission_info))
        persist_single_row(connection, TABLE_SUBMISSION, submission_info)

        submission = reddit_client.submission(id=sub.id)
        if submission is not None:
            num_comments = download_comments(sub, submission, connection)
            num_downloaded_comments = num_downloaded_comments + num_comments

        last_submission = sub

    return last_submission, num_downloaded_submissions, num_downloaded_comments


def download_comments(sub, submission, connection):
    log.info(">>> Downloading {} commments from submission {}".format(submission.num_comments, sub.id))
    submission.comments.replace_more(limit=None)
    num_downloaded_comments = 0
    persist_batch_size = PARAMETER.COMMENTS_PERSIST_BATCH_SIZE
    comments = []
    for comment in submission.comments.list():
        num_downloaded_comments = num_downloaded_comments + 1
        comment_info = {
            "id": comment.id,
            "submission": sub.id,
            "created_utc": int(comment.created_utc),
            "score": comment.score,
            "body": comment.body.replace("'", "\\'"),
            "permalink": comment.permalink,
        }

        if log.isEnabledFor(logging.DEBUG):
            log.debug(">>> Comment info: {}".format(comment_info))

        comments.append(tuple(comment_info.values()))
        if len(comments) >= persist_batch_size:
            persist_comments(len(comment_info), comments, connection)
            comments.clear()

        persist_comments(len(comment_info), comments, connection)
        comments.clear()

    return num_downloaded_comments


def persist_comments(num_values, comments, connection):
    if len(comments) > 0:
        cursor = None
        try:
            cursor = connection.cursor()
            placeholders = ', '.join(["%s"] * num_values)
            sql = "INSERT INTO {} VALUES ({})".format(TABLE_COMMENT, placeholders)
            # if log.isEnabledFor(logging.DEBUG):
            #     log.debug("Executing sql: {}".format(sql))
            cursor.executemany(sql, comments)
            connection.commit()
        finally:
            if cursor is not None:
                cursor.close()


def download():
    reddit_client = init_reddit_client()
    pushshift_client = init_pushshift_client(reddit_client)

    connection = None
    try:
        connection = mysql.connector.connect(user=PARAMETER.DB_USER, password=PARAMETER.DB_PASSWORD,
                                             host=PARAMETER.DB_HOST, port=PARAMETER.DB_PORT,
                                             database=PARAMETER.DB_NAME)

        download_subreddit(pushshift_client, reddit_client, connection)

    finally:
        if connection is not None:
            connection.close()

    log.info('finished downloading')


def download_subreddit(pushshift_client, reddit_client, connection):
    subreddit = reddit_client.subreddit(PARAMETER.SUBREDDIT)
    subreddit_info = {
        "id": subreddit.id,
        "name": subreddit.name,
        "display_name": subreddit.display_name,
        "title": subreddit.title,
        "created_utc": int(subreddit.created_utc),
    }
    log.info("Subreddit information: {}".format(subreddit_info))

    persist_single_row(connection, TABLE_SUBREDDIT, subreddit_info)

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
        last_submission, num_submissions, num_downloaded_comments = download_submissions(subreddit.id, pushshift_client,
                                                                                         reddit_client, connection,
                                                                                         start_epoch,
                                                                                         end_epoch)
        num_downloaded_submissions = num_downloaded_submissions + num_submissions

        step_counter = step_counter + 1
        if last_submission is None:
            no_more_data = True
        else:
            start_epoch = int(last_submission.created_utc)
    log.info("Downloaded {} submissions".format(num_downloaded_submissions))
    log.info("Downloaded {} comments".format(num_downloaded_comments))
