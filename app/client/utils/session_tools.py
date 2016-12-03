# File: session_tools.py
# Desc:
# Date: December 02, 2016 @ 3:13 AM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

import base64
import jwt
from app.app_config import AUTH0_AUDIENCE, AUTH0_KEY
from flask import redirect, session, url_for


def get_session_user_id():

    if 'profile' not in session:
        return None

    if 'sub' in session['profile']:
        return session['profile']['sub']

    return None


def get_session_profile():

    if 'profile' not in session:
        return None

    return session['profile']


def get_session_audience():

    if 'current_audience' in session:
        return session['current_audience']

    return None


def get_session_token():

    if 'current_jwt' in session:
        return session['current_jwt']

    return None


def session_valid():

    token = get_session_token()

    if not token:
        return False

    try:
        jwt.decode(
            token,
            base64.b64decode(s=AUTH0_KEY.replace("_", "/").replace("-", "+")),
            audience=AUTH0_AUDIENCE
        )
    except jwt.ExpiredSignature:
        return False
    except:
        return False
    else:
        return True


# def get_self_profile():
#
#     if not session_valid():
#         return None
#
#     headers = {
#         'authorization': 'Bearer ' + get_session_token()
#     }
#
#     response = shared_utils.perform_get_request(
#         target_url='http://localhost:6400/profiles/self',
#         headers=headers
#     )
#
#     return response


def remove_session_data():

    if session_valid():
        if 'profile' in session:
            del session['profile']

        if 'current_jwt' in session:
            # session.__de
            pass

        return redirect(url_for('client_home'))
