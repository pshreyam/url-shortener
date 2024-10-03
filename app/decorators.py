from functools import wraps

from flask import redirect, session, url_for


def login_required(f):
    """Protect the endpoint from being accessed by unauthenticated user."""

    @wraps(f)
    def wrap(*args, **kwargs):
        if "email" in session.keys():
            return f(*args, **kwargs)
        return redirect(url_for("login"))

    return wrap


def logout_required(f):
    """Protect the endpoint from being accessed by authenticated user."""

    @wraps(f)
    def wrap(*args, **kwargs):
        if "email" not in session.keys():
            return f(*args, **kwargs)
        return redirect(url_for("index"))

    return wrap
