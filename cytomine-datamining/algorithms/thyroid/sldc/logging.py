# -*- coding: utf-8 -*-
import os
import threading
from abc import abstractmethod

__author__ = "Mormont Romain <romain.mormont@gmail.com>"
__version__ = "0.1"


class Logger(object):
    """A class encaspulating logging
    """
    ERROR = 1
    WARNING = 2
    INFO = 3
    DEBUG = 4

    def __init__(self, level, prefix=True):
        """Build a logger object with the given level of verbosity
        Parameters
        ----------
        level: int
            Verbosity level
        """
        self._level = level
        self._prefix = prefix
        self._lock = threading.Lock()

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level

    def d(self, msg):
        """Alias for self.debug
        Parameters
        ----------
        msg: string
            The message to log
        """
        self.debug(msg)

    def debug(self, msg):
        """Logs a information message if the level of verbosity is above or equal DEBUG
        Parameters
        ----------
        msg: string
            The message to log
        """
        self._log(Logger.DEBUG, msg)

    def i(self, msg):
        """Alias for self.info
        Parameters
        ----------
        msg: string
            The message to log
        """
        self.info(msg)

    def info(self, msg):
        """Logs a information message if the level of verbosity is above or equal INFO
        Parameters
        ----------
        msg: string
            The message to log
        """
        self._log(Logger.INFO, msg)

    def w(self, msg):
        """Alias for self.warning
        Parameters
        ----------
        msg: string
            The message to log
        """
        self.warning(msg)

    def warning(self, msg):
        """Logs a information message if the level of verbosity is above or equal WARNING
        Parameters
        ----------
        msg: string
            The message to log
        """
        self._log(Logger.WARNING, msg)

    def e(self, msg):
        """Alias for self.error
        Parameters
        ----------
        msg: string
            The message to log
        """
        self.error(msg)

    def error(self, msg):
        """Logs a information message if the level of verbosity is above or equal ERROR
        Parameters
        ----------
        msg: string
            The message to log
        """
        self._log(Logger.ERROR, msg)

    def _log(self, level, msg):
        """Check the verbosity level, if it is above, actually prints the message
        Parameters
        ----------
        level: int
            Verbosity level of the message
        msg: string
            The message
        """
        if self._level <= level:
            formatted = self._format_msg(level, msg)
            self._lock.acquire()
            self._print(formatted)
            self._lock.release()

    @abstractmethod
    def _print(self, formatted_msg):
        pass

    @classmethod
    def prefix(cls, level):
        from datetime import datetime
        now = datetime.now().isoformat()
        tid = threading.current_thread().zfill(10)
        if level == cls.DEBUG:
            return "[tid:{}][{}][DEBUG]".format(tid, now)
        elif level == cls.WARNING:
            return "[tid:{}][{}][WARN ]".format(tid, now)
        elif level == cls.ERROR:
            return "[tid:{}][{}][ERROR]".format(tid, now)
        else:  # info
            return "[tid:{}][{}][INFO ]".format(tid, now)

    def _format_msg(self, level, msg):
        if self._prefix:
            rows = ["{} {}".format(self.prefix(level), row) for row in msg.split(os.linesep)]
            rows.append("")  # append a row so that there is an end of line at the end of the message
            return os.linesep.join(rows)
        else:
            return msg


class StandardOutputLogger(Logger):
    """A logger printing the messages on the standard output
    """
    def _print(self, formatted_msg):
        print formatted_msg


class FileLogger(Logger):
    """A logger printing the messages into a file
    """
    def __init__(self, filepath, level, prefix=True):
        """Create a FileLogger
        Parameters
        ----------
        filepath: string
            Path to the logging file
        level: int
            Verbosity level
        prefix: bool
            True for adding a prefix for the logger
        """
        Logger.__init__(self, level, prefix=prefix)
        self._file = open(filepath, "w+")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _print(self, formatted_msg):
        self._file.write(formatted_msg)

    def close(self):
        """Close the logging file
        """
        self._file.close()