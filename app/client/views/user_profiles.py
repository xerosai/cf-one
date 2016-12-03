# File: dashboard.py
# Desc:
# Date: December 02, 2016 @ 12:45 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

from flask import render_template
from app import app
from app.client.authenticator import requires_auth
from app.client.utils import session_tools
from app.constants.route_constants import RouteConstants as RoCon
from app.resources.user_profiles_resource import UserProfilesResource


up_res = UserProfilesResource()


@app.route(RoCon.ROUTE_PROFILES, methods=[RoCon.HTTP_METHOD_GET])
@requires_auth
def client_get_profile_self():

    session_profile_or_none = session_tools.get_session_profile()
    current_user_or_none = up_res.get_user_by_auth(
        auth_id=session_tools.get_session_user_id(), user_data=session_profile_or_none
    )

    return render_template(
        template_name_or_list='profile.html',
        user_token=session_tools.get_session_token(),
        user_data=current_user_or_none
    )
