# File: authenticator.py
# Desc: auth0-based authentication system
# Date: December 01, 2016 @ 4:54 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai


import base64
import jwt
import mongoengine
import sys
import requests
from flask import _request_ctx_stack, jsonify, request
from functools import wraps
from werkzeug.local import LocalProxy
from app.app_config import AUTH0_KEY, AUTH0_AUDIENCE
from app.constants.response_constants import ResponseConstants as ReCon
from app.constants.route_constants import RouteConstants as RoCon
from app.non_db_models.action_response import ActionResponse
from app.models.user_profiles import UserProfiles


current_user = LocalProxy(lambda: _request_ctx_stack.top.current_user)


def authenticate(error):
    response = jsonify(error)
    response.status_code = 401
    return response


def requires_authentication(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get(RoCon.HTTP_HEADER_AUTH, None)
        response = ActionResponse(action_name='authenticate_api')

        if not auth:
            response.set_data(action_message=ReCon.ERR_AUTH_HEADER_MISSING, action_data={
                ReCon.KEY_ACTION_DATA_DETAIL: 'Authentication header not presented'
            })
            return authenticate(error=response.to_dict())

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            response.set_data(action_message=ReCon.ERR_AUTH_HEADER_INVALID, action_data={
                ReCon.KEY_ACTION_DATA_DETAIL: 'Authentication header was invalid'
            })
            return jsonify(response.to_dict())
        elif len(parts) == 1:
            response.set_data(action_message=ReCon.ERR_AUTH_TOKEN_MISSING, action_data={
                ReCon.KEY_ACTION_DATA_DETAIL: 'Authentication token is missing'
            })
            return jsonify(response.to_dict())
        elif len(parts) > 2:
            response.set_data(action_message=ReCon.ERR_AUTH_HEADER_INVALID, action_data={
                ReCon.KEY_ACTION_DATA_DETAIL: 'Authentication header was invalid'
            })
            return jsonify(response.to_dict())

        token = parts[1]

        try:
            payload = jwt.decode(
                token,
                base64.b64decode(
                    s=AUTH0_KEY.replace('_', '/').replace('-', '+')
                ),
                audience=AUTH0_AUDIENCE
            )
        except jwt.ExpiredSignatureError:
            response.set_data(action_message=ReCon.ERR_AUTH_TOKEN_EXPIRED, action_data={
                ReCon.KEY_ACTION_DATA_DETAIL: ''
            })
            return authenticate(error=response.to_dict())
        except jwt.InvalidAudienceError:
            response.set_data(action_message=ReCon.ERR_AUTH_AUDIENCE_INVALID, action_data={
                ReCon.KEY_ACTION_DATA_DETAIL: ''
            })
            return authenticate(error=response.to_dict())
        except jwt.InvalidIssuedAtError:
            response.set_data(action_message=ReCon.ERR_AUTH_ISSUED_AT_INVALID, action_data={

            })
            return authenticate(error=response.to_dict())
        except jwt.DecodeError:
            response.set_data(action_message=ReCon.ERR_AUTH_DECODE_ERROR, action_data={

            })
            return authenticate(error=response.to_dict())

        _request_ctx_stack.top.current_user = payload
        _request_ctx_stack.top.current_user['session_jwt'] = token

        return f(*args, **kwargs)

    return decorated


def get_user_details():

    jwt_or_none = get_session_jwt()

    if jwt_or_none is None:
        return None

    json_payload = {
        'id_token': jwt_or_none
    }

    try:
        user_detail = requests.post(url=RoCon.AUTH0_ENDPOINT_USER_DETAIL, json=json_payload)
    except:
        return None
    else:
        json_data_or_none = user_detail.json()

        if json_data_or_none is None or type(json_data_or_none) is not dict:
            return None

        user_dict = {
            'auth0_identifier': json_data_or_none['user_id'],
            'display_name': json_data_or_none['name'],
            'email_address': json_data_or_none['email'],
            'display_image': json_data_or_none['picture']
        }

        return user_dict


def get_or_update_profile():

    if not hasattr(_request_ctx_stack.top, 'current_user'):
        return None

    session_jwt_or_none = get_session_jwt()

    if session_jwt_or_none is None:
        return None

    user_obj = _request_ctx_stack.top.current_user

    try:
        profile = UserProfiles.objects(auth0_idr=user_obj['sub']).get()
    except mongoengine.DoesNotExist:
        user_info = get_user_details()

        if not user_info or type(user_info) is not dict:
            return None

        profile = UserProfiles(**user_info)

        try:
            profile.save()
        except:
            print(sys.exc_info())
        else:
            get_or_update_profile()
    except:
        print(sys.exc_info())
        return None
    else:
        return profile


def get_session_jwt():

    if not hasattr(_request_ctx_stack.top, 'current_user'):
        return None

    if 'session_jwt' not in _request_ctx_stack.top.current_user:
        return None

    return _request_ctx_stack.top.current_user['session_jwt']
