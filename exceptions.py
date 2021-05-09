from __future__ import unicode_literals


class SpiderKeeperError(Exception):
    """
    Base class for SpiderKeeper API exceptions.
    """
    default_detail = 'SpiderKeeper Error'

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail

    def __str__(self):
        return self.detail

    def __repr__(self):
        return '{0}("{1}")'.format(self.__class__.__name__, self.detail)


class SpiderKeeperResponseError(SpiderKeeperError):

    default_detail = 'SpiderKeeper Response Error'