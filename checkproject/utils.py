"""Utility functions for this module"""

def remove_prefix(path, prefix):
    """Remove a given prefix from a path

    @param path: The path to clean up.

    @param prefix: The prefix to remove.

    @return: The string without the prefix, or, if the prefix is
    not present in the path, raise a ValueError.

    """
    import os

    path = os.path.abspath(path)
    prefix = os.path.abspath(prefix)

    if not path.startswith(prefix):
        raise ValueError('path and prefix do not match')

    return str(path[len(prefix) + 1:])
