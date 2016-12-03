# File: authenticator.py
# Desc:
# Date: December 02, 2016 @ 2:28 AM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

from flask import redirect, request, session
from functools import wraps


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            # Redirect to Login page here
            return redirect('/')
        # if not session_tools.session_valid():
        #     return redirect('/')
        return f(*args, **kwargs)

    return decorated
