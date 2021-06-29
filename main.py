__author__ = 'simone.decristofaro'

import getopt
import sys

# INIT LOG <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
import dateutil

import PARAMETER
import downloader
from logger_manager import *

from enum import Enum


class ParameterName(Enum):
    REDDIT_CLIENT_ID = 'reddit_client_id'
    REDDIT_USERNAME = 'reddit_username'
    REDDIT_SECRET = 'reddit_secret'
    SUBREDDIT = 'subreddit'
    FROM_DATE = 'from_date'
    TO_DATE = 'to_date'
    SUBMISSIONS_BATCH_SIZE = 'submissions_batch_size'
    NUM_ITERATIONS = 'num_iterations'


def get_long_option(parameter_name):
    return '--{}'.format(parameter_name)


def get_option_declaration(parameter_name):
    return '{}='.format(parameter_name)


def check_existence_required_parameter(parameter_name, parameter_value):
    if parameter_value is None:
        print("No value specified for required parameter {}".format(parameter_name))
        print(__help())
        sys.exit(2)


def main(argv):
    parse_command_line(argv)
    downloader.download()


def parse_command_line(argv):
    # Parse command line parameters
    try:
        opts, args = getopt.getopt(argv, "h", [
            "help"
            , get_option_declaration(ParameterName.REDDIT_USERNAME.value)
            , get_option_declaration(ParameterName.REDDIT_CLIENT_ID.value)
            , get_option_declaration(ParameterName.REDDIT_SECRET.value)
            , get_option_declaration(ParameterName.SUBREDDIT.value)
            , get_option_declaration(ParameterName.SUBMISSIONS_BATCH_SIZE.value)
            , get_option_declaration(ParameterName.NUM_ITERATIONS.value)
            , get_option_declaration(ParameterName.FROM_DATE.value)
            , get_option_declaration(ParameterName.TO_DATE.value)
        ])
    except getopt.GetoptError:
        log.exception("ERROR parsing command line arguments")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(__help())
            sys.exit()
        elif opt == get_long_option(ParameterName.REDDIT_USERNAME.value):
            PARAMETER.REDDIT_USERNAME = arg
        elif opt == get_long_option(ParameterName.REDDIT_CLIENT_ID.value):
            PARAMETER.REDDIT_CLIENT_ID = arg
        elif opt == get_long_option(ParameterName.REDDIT_SECRET.value):
            PARAMETER.REDDIT_SECRET = arg
        elif opt == get_long_option(ParameterName.SUBREDDIT.value):
            PARAMETER.SUBREDDIT = arg
        elif opt == get_long_option(ParameterName.SUBMISSIONS_BATCH_SIZE.value):
            PARAMETER.SUBMISSIONS_BATCH_SIZE = int(arg)
        elif opt == get_long_option(ParameterName.NUM_ITERATIONS.value):
            PARAMETER.NUM_ITERATIONS = int(arg)
        elif opt == get_long_option(ParameterName.FROM_DATE.value):
            PARAMETER.FROM_DATE = dateutil.parser.parse(arg)
        elif opt == get_long_option(ParameterName.TO_DATE.value):
            PARAMETER.TO_DATE = dateutil.parser.parse(arg)

    # check type value
    check_existence_required_parameter(ParameterName.REDDIT_USERNAME.value, PARAMETER.REDDIT_USERNAME)
    check_existence_required_parameter(ParameterName.REDDIT_CLIENT_ID.value, PARAMETER.REDDIT_CLIENT_ID)
    check_existence_required_parameter(ParameterName.REDDIT_SECRET.value, PARAMETER.REDDIT_SECRET)
    check_existence_required_parameter(ParameterName.SUBREDDIT.value, PARAMETER.SUBREDDIT)

    # global appType
    # appType = OUTPUT.getOutPutTypeByName(PARAMETER.TYPE)


def __help():
    """
    :rtype: str
    """
    return os.linesep.join([
        os.linesep
        , "----------- configuration -----------: "
        , "-h, --help:               usage"
        , get_long_option(ParameterName.REDDIT_USERNAME.value) + ":          [REQUIRED] Reddit username."
        , get_long_option(ParameterName.REDDIT_CLIENT_ID.value) + ":          [REQUIRED] Reddit client id."
        , get_long_option(ParameterName.REDDIT_SECRET.value) + ":          [REQUIRED] Reddit secret."
        , get_long_option(
            ParameterName.SUBMISSIONS_BATCH_SIZE.value) + ":  Number of submissions to download in batch each time. Default: " + PARAMETER.SUBMISSIONS_BATCH_SIZE
        , get_long_option(
            ParameterName.NUM_ITERATIONS.value) + ":  Number of iterations to download submissions in batch. Negative number means no limit. Default: " + PARAMETER.NUM_ITERATIONS
        , get_long_option(
            ParameterName.FROM_DATE.value) + ":          Download only submissions created after this date in ISO-8601 . Default: ." + PARAMETER.FROM_DATE
        , get_long_option(
            ParameterName.TO_DATE.value) + ":          Download only submissions created before this date in ISO-8601 . Default: ." + PARAMETER.TO_DATE
        , os.linesep
    ])


if __name__ == '__main__':
    main(sys.argv[1:])
