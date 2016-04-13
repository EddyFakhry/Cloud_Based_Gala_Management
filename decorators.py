"""
AUTHOR: EDDY FAKHRY
DATE:   15/10/2016
"""
from functools import wraps
from flask import redirect, url_for,session


def check_admin_login(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if 'username' in session:
            return func(*args, **kwargs)
        return redirect(url_for('main'))
    return wrapped_function


def check_admin_or_swimmer(func):
    """
    Lower permission for swimmer entries
    :param func:
    :return: wrapped_function
    """
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if 'username' in session or 'swimmer' in session:
            return func(*args, **kwargs)
        return redirect(url_for('main'))
    return wrapped_function


def is_club_owner(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        # TODO :For website administrator
        return func(*args, **kwargs)
    return wrapped_function

