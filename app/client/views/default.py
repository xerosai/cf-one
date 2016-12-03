# File: default.py
# Desc:
# Date: December 02, 2016 @ 1:42 AM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

import json
import requests
from flask import redirect, render_template, request, session, url_for
from app import app
from app.app_config import AUTH0_KEY, AUTH0_AUDIENCE
from app.constants.route_constants import RouteConstants as RoCon
from app.client import authenticator
from app.client.utils import session_tools
from app.resources.user_profiles_resource import UserProfilesResource
from app.resources.cafe_items_resource import CafeItemsResource
from app.resources.store_locations_resource import StoreLocationsResource


@app.route(RoCon.ROUTE_CLIENT_AUTHORIZE)
def client_authorization():
    code = request.args.get('code')

    json_header = {'content-type': 'application/json'}

    token_url = "https://{domain}/oauth/token".format(
        domain='xrscodeworks.auth0.com'
    )
    token_payload = {
        'client_id': AUTH0_AUDIENCE,
        'client_secret': AUTH0_KEY,
        'redirect_uri': 'http://0.0.0.0:7200/authorize',
        'code': code,
        'grant_type': 'authorization_code'
    }

    token_info = requests.post(token_url, data=json.dumps(token_payload), headers=json_header).json()

    user_url = "https://{domain}/userinfo?access_token={access_token}" \
        .format(domain='xrscodeworks.auth0.com', access_token=token_info['access_token'])

    user_info = requests.get(user_url).json()

    # We're saving all user information into the session
    session['profile'] = user_info
    session['current_jwt'] = token_info['id_token']

    # Create user or try to

    # Redirect to the User logged in page that you want here
    # In our case it's /dashboard
    if request.args.get('next_url'):
        return redirect(request.args.get('next_url'))

    return redirect('/')


@app.route(RoCon.ROUTE_CLIENT_LOGIN)
def client_login():

    if session_tools.session_valid():
        return redirect(url_for('client_home'))

    return render_template(template_name_or_list='login.html')


@app.route(RoCon.ROUTE_CLIENT_LOGOUT)
@authenticator.requires_auth
def client_logout():
    session_tools.remove_session_data()
    return redirect(url_for('client_home'))


@app.route(RoCon.ROUTE_CLIENT_ROOT)
@app.route(RoCon.ROUTE_CLIENT_HOME)
def client_home():
    cf_res = CafeItemsResource()
    up_res = UserProfilesResource()
    store_res = StoreLocationsResource()

    recent_items = cf_res.get_resources_json(page=0, ipp=3)
    store_items = store_res.get_resources_json(page=0, ipp=3)

    session_profile_or_none = session_tools.get_session_profile()

    current_user = up_res.get_user_by_auth(
        auth_id=session_tools.get_session_user_id(), user_data=session_profile_or_none
    )

    return render_template(
        template_name_or_list='dashboard.html',
        item_data=recent_items,
        store_data=store_items,
        current_user=current_user
    )
