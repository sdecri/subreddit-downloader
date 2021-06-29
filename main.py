__author__ = 'simone.decristofaro'

import getopt
import inspect
import logging
import os
import sys
from logging import config

# INIT LOG <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
import PARAMETER

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
LOGGING_CONFIG_FILE_PATH = os.path.realpath(os.path.join(SCRIPT_DIRECTORY, "logging.conf"))
logging.config.fileConfig(LOGGING_CONFIG_FILE_PATH)

# logging.basicConfig()
log_console = logging.getLogger('onlyconsole')
log = logging.getLogger()

PARAMETER_REDDIT_CLIENT_ID = "reddit_client_id"
PARAMETER_REDDIT_USERNAME = "reddit_username"
PARAMETER_REDDIT_SECRET = "reddit_secret"


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
    log_console.debug("Start trajectory persisting process")


def parse_command_line(argv):
    # Parse command line parameters
    try:
        opts, args = getopt.getopt(argv, "ht:f:c:", [
            "help"
            , get_option_declaration(PARAMETER_REDDIT_USERNAME)
            , get_option_declaration(PARAMETER_REDDIT_CLIENT_ID)
            , get_option_declaration(PARAMETER_REDDIT_SECRET)
        ])
    except getopt.GetoptError:
        log.exception("ERROR parsing command line arguments")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(__help())
            sys.exit()
        elif opt == get_long_option(PARAMETER_REDDIT_USERNAME):
            PARAMETER.REDDIT_USERNAME = arg
        elif opt == get_long_option(PARAMETER_REDDIT_CLIENT_ID):
            PARAMETER.REDDIT_CLIENT_ID = arg
        elif opt == get_long_option(PARAMETER_REDDIT_SECRET):
            PARAMETER.REDDIT_SECRET = arg

    # check type value
    check_existence_required_parameter(PARAMETER_REDDIT_USERNAME, PARAMETER.REDDIT_USERNAME)
    check_existence_required_parameter(PARAMETER_REDDIT_CLIENT_ID, PARAMETER.REDDIT_CLIENT_ID)
    check_existence_required_parameter(PARAMETER_REDDIT_SECRET, PARAMETER.REDDIT_SECRET)

    # global appType
    # appType = OUTPUT.getOutPutTypeByName(PARAMETER.TYPE)

    log.info("Start downloading subreddit")


def __help():
    """
    :rtype: str
    """
    return os.linesep.join([
        os.linesep
        , "----------- trajectories-to-db configuration -----------: "
        , "-h, --help:               usage"
        , "-f, --file-path:          [REQUIRED] csv file containing trajectories."
        , "--chunk-size:             size of the chunk to export = " + str(PARAMETER.CHUNK_SIZE)
        , "--table-prefix:           table prefix, default = " + PARAMETER.TABLE_PREFIX
        , "--dbhost:                 database host, default = " + PARAMETER.DB_HOST
        , "--dbport:                 database port, default = " + PARAMETER.DB_PORT
        , "--dbname:                 database name, default = " + PARAMETER.DB_NAME
        , "--dbuser:                 database user, default = " + PARAMETER.DB_USER
        , "--dbpassword:             database password, default = " + PARAMETER.DB_PASSWORD
        , "--drop-table:             drop tables = " + ('y' if PARAMETER.DROP_TABLE else 'n')
        , os.linesep
    ])


if __name__ == '__main__':
    main(sys.argv[1:])
