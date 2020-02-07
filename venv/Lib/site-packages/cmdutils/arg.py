"""Support for argparser and CmdUtils logging
"""

import sys
import os
from cmdutils.log import Logger

__all__ = ['add_logging', 'add_verbose', 'create_logger']


def add_logging(arg_parser, log_file=None):
    """Adds a logging argument to the given parser"""
    arg_parser.add_argument(
        '-l', '--log',
        dest='log_file',
        metavar='FILENAME',
        help='Log verbosely to the given file',
        default=log_file)


def add_verbose(arg_parser, add_quiet=True, add_log=False):
    """Adds --verbose/--quiet options to a parser"""
    arg_parser.add_argument(
        '-v', '--verbose',
        dest='verbosity',
        help="Make the command more verbose (use multiple times "
        "to increase verbosity)",
        default=0,
        action="count")
    if add_quiet:
        arg_parser.add_argument(
            '-q', '--quiet',
            dest="quietness",
            help="Make the command quieter (use multiple times "
            "to increase quietness)",
            default=0,
            action="count")


def create_logger(args):
    """Creates a logger from an args option"""
    logger = Logger([])
    verbosity = Logger.LEVELS.index(Logger.NOTIFY)
    verbosity -= getattr(args, 'verbosity', 0)
    verbosity += getattr(args, 'quietness', 0)
    level = Logger.level_for_integer(verbosity)
    logger.consumers.append((level, sys.stdout))
    if getattr(args, 'log_file', None):
        log_file = args.log_file
        log_dir = os.path.dirname(os.path.abspath(log_file))
        if not os.path.exists(log_dir):
            logger.notify('Creating directory for log file: %s' % log_dir)
            os.makedirs(log_dir)
        f = open(log_file, 'a')
        logfile_level = min(Logger.level_for_integer(verbosity),
                            Logger.DEBUG)
        logger.consumers.append((logfile_level, f))
    args.logger = logger
    return logger
