# File: user_profiles.py
# Desc:
# Date: November 30, 2016 @ 11:46 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

from flask import jsonify, request
from app import app
from app.constants.route_constants import RouteConstants as RoCon
from app.resources.user_profiles_resource import UserProfilesResource
from app.api.authenticator.authenticator import requires_authentication


user_profile_res = UserProfilesResource()
target_url = RoCon.ROUTE_API_BASE + RoCon.ROUTE_PROFILES


@app.route(target_url, methods=[RoCon.HTTP_METHOD_GET])
@app.route(target_url + '/<string:resource_id>', methods=[RoCon.HTTP_METHOD_GET])
def api_get_profiles(resource_id=None):

    if resource_id:

        return jsonify(user_profile_res.get_resource_json(resource_id=resource_id))
    else:
        try:
            page = int(request.args.get(RoCon.PARAM_PAGE))
        except:
            page = 0

        return jsonify(user_profile_res.get_resources_json(page=page))


@app.route(target_url + '/<string:resource_id>/orders', methods=[RoCon.HTTP_METHOD_GET])
@requires_authentication
def api_get_profile_orders(resource_id=None):

    try:
        page = int(request.args.get(RoCon.PARAM_PAGE))
    except:
        page = 0

    return jsonify(user_profile_res.get_user_orders(user_id=resource_id, page=page))


@app.route(target_url, methods=[RoCon.HTTP_METHOD_POST])
@requires_authentication
def api_post_profiles():

    return jsonify(user_profile_res.create_resource(resource_data=request.get_json()))


@app.route(target_url + '/<string:resource_id>', methods=[RoCon.HTTP_METHOD_PUT])
@requires_authentication
def api_patch_profiles(resource_id=None):

    return jsonify(user_profile_res.update_resource(resource_id=resource_id, resource_data=request.get_json()))


@app.route(target_url + '/<string:resource_id>', methods=[RoCon.HTTP_METHOD_DELETE])
@requires_authentication
def api_delete_profiles(resource_id=None):

    return jsonify(user_profile_res.delete_resource(resource_id=resource_id))
