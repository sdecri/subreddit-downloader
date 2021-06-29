import inspect
import logging
from logging import config
import os

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
LOGGING_CONFIG_FILE_PATH = os.path.realpath(os.path.join(SCRIPT_DIRECTORY, "logging.conf"))
logging.config.fileConfig(LOGGING_CONFIG_FILE_PATH)

# logging.basicConfig()
log_console = logging.getLogger('onlyconsole')
log = logging.getLogger()

