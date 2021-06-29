__author__ = 'simone.decristofaro'

import sys
import getopt
import os
import logging
from logging import config

import time, math, inspect

# INIT LOG <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
import PARAMETER

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
LOGGING_CONFIG_FILE_PATH = os.path.realpath(os.path.join(SCRIPT_DIRECTORY, "logging.conf"))
logging.config.fileConfig(LOGGING_CONFIG_FILE_PATH)

# logging.basicConfig()
log_console = logging.getLogger('onlyconsole')


def main(argv):
    parse_command_line(argv)
    log_console.debug("Start trajectory persisting process")


def parse_command_line(argv):
    # Parse command line parameters
    try:
        opts, args = getopt.getopt(argv, "ht:f:c:", [
            "help"
            , "type="
            , "file-path="
            , "chunk-size="
            , "table-prefix="
            , "dbhost="
            , "dbport="
            , "dbname="
            , "dbuser="
            , "dbpassword="
            , "drop-table="
        ])
    except getopt.GetoptError:
        log_console.exception("ERROR parsing command line arguments")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(__help())
            sys.exit()
        elif opt in ("-t", "--run-type"):
            PARAMETER.TYPE = arg
        elif opt in ("-f", "--file-path"):
            PARAMETER.FILE_PATH = os.path.abspath(arg)
        elif opt in ("-c", "--chunk-size"):
            PARAMETER.CHUNK_SIZE = int(arg)
        elif opt == "--table-prefix":
            PARAMETER.TABLE_PREFIX = arg
        elif opt == "--dbhost":
            PARAMETER.DB_HOST = arg
        elif opt == "--dbport":
            PARAMETER.DB_PORT = arg
        elif opt == "--dbname":
            PARAMETER.DB_NAME = arg
        elif opt == "--dbuser":
            PARAMETER.DB_USER = arg
        elif opt == "--dbpassword":
            PARAMETER.DB_PASSWORD = arg
        elif opt == "--drop-table":
            PARAMETER.DROP_TABLE = arg == 'y'

    if PARAMETER.FILE_PATH is None:
        print(__help())
        sys.exit(2)

    # check type value
    # if (PARAMETER.TYPE is None or not PARAMETER.TYPE in PARAMETER.TYPE_AVAILABLE_VALUES):
    #     print("No valid run-type = {} value!".format(PARAMETER.TYPE))
    #     print(__help())
    #     sys.exit(2)

    # global appType
    # appType = OUTPUT.getOutPutTypeByName(PARAMETER.TYPE)

    log_console.info(os.linesep.join([
        os.linesep
        , "----------- trajectories-to-db configuration -----------: "
        , "parameters values: "
        , "--file-path:            csv file containing trajectories = " + PARAMETER.FILE_PATH
        , "--chunk-size:           size of the chunk to export = " + str(PARAMETER.CHUNK_SIZE)
        , "--table-prefix:         table prefix = " + PARAMETER.TABLE_PREFIX
        , "--dbhost:               database host = " + PARAMETER.DB_HOST
        , "--dbport:               database port = " + PARAMETER.DB_PORT
        , "--dbname:               database name = " + PARAMETER.DB_NAME
        , "--dbuser:               database user = " + PARAMETER.DB_USER
        , "--dbpassword:           database password = " + PARAMETER.DB_PASSWORD
        , "--drop-table:           drop tables = " + ('y' if PARAMETER.DROP_TABLE else 'n')

    ]))


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
