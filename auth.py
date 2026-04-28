import os
from functools import wraps
from flask import session, redirect, url_for, request


def google_configured():
    return bool(os.getenv("GOOGLE_CLIENT_ID") and os.getenv("GOOGLE_CLIENT_SECRET"))


def current_user():
    return session.get("user")


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login_page", next=request.path))
        return f(*args, **kwargs)
    return wrapper
