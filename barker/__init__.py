from __future__ import absolute_import
from os import path

# This is the absolute, real path to the repo base
_base = path.abspath(path.join(path.dirname(__file__), '..'))


class AppPath(object):
    """Collection of class methods to build paths relative to any directory."""

    @classmethod
    def base(cls, subpath):
        return path.join(_base, subpath)

    @classmethod
    def barker(cls, subpath):
        return path.join(_base, 'barker', subpath)

    @classmethod
    def models(cls, subpath):
        return path.join(_base, 'barker', 'models', subpath)
