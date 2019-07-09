import sys


class BaseCustomError(Exception):
    """
    Base error class from which any other exception classes should be inherited. Also, this exception
    class can be easily for wrapping other exceptions

    Prints just message passed to constructor. When invoked with 'from' clause, adds original exception
    message.
    """
    def __init__(self, message):
        super(BaseCustomError, self).__init__(self, message)
        self.message = message

    def __str__(self):
        return self.message + (" : " + str(self.__cause__) if self.__cause__ else "")


# TODO: should be added base class for general JSON error not related to server
# TODO: write docstring
class UnexpectedServerJson(BaseCustomError):
    def __init__(self, action, doc):
        super(UnexpectedServerJson, self).__init__("Got unexpected JSON on '%s'" % action)
        self.action = action
        self.doc = doc

    def __str__(self):
        return super(UnexpectedServerJson, self).__str__() + "\nServer answer: '%s'" % self.doc


def make_stdout_unbuffered():
    """Allows to correctly log stdout via systemd"""
    sys.stdout = Unbuffered(sys.stdout)


class Unbuffered(object):
    """Makes stream unbuffered by flushing it after any write operation"""

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)
