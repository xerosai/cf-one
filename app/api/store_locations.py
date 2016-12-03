# File: store_locations.py
# Desc:
# Date: December 02, 2016 @ 8:13 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

from flask import jsonify, request
from app import app
from app.api.authenticator.authenticator import requires_authentication
from app.constants.route_constants import RouteConstants as RoCon
from app.resources.store_locations_resource import StoreLocationsResource


store_loc_res = StoreLocationsResource()
target_url = RoCon.ROUTE_API_BASE + RoCon.ROUTE_STORE_LOCATIONS


@app.route(target_url, methods=[RoCon.HTTP_METHOD_GET])
@app.route(target_url + '/<string:location_id>', methods=[RoCon.HTTP_METHOD_GET])
def api_get_store_loc(location_id=None):

    if location_id:
        return jsonify(store_loc_res.get_resource_json(resource_id=location_id))
    else:
        try:
            page = int(request.args.get(RoCon.PARAM_PAGE))
        except:
            page = 0

        return jsonify(store_loc_res.get_resources_json(page=page))


@app.route(target_url, methods=[RoCon.HTTP_METHOD_POST])
@requires_authentication
def api_post_store_loc():

    return jsonify(store_loc_res.create_resource(resource_data=request.get_json()))


@app.route(target_url + '/<string:location_id>', methods=[RoCon.HTTP_METHOD_PUT])
@requires_authentication
def api_update_store_loc(location_id=None):

    return jsonify(store_loc_res.update_resource(resource_id=location_id, resource_data=request.get_json()))


@app.route(target_url + '/<string:location_id>', methods=[RoCon.HTTP_METHOD_DELETE])
@requires_authentication
def api_delete_store_loc(location_id=None):

    return jsonify(store_loc_res.delete_resource(resource_id=location_id))
