# File: orders.py
# Desc: Orders routes
# Date: November 30, 2016 @ 11:56 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

from flask import jsonify, request
from app import app
from app.api.authenticator.authenticator import requires_authentication
from app.constants.route_constants import RouteConstants as RoCon
from app.non_db_models.action_response import ActionResponse
from app.resources.orders_resource import OrdersResource


orders_res = OrdersResource()
target_url = RoCon.ROUTE_API_BASE + RoCon.ROUTE_ORDERS


@app.route(target_url, methods=[RoCon.HTTP_METHOD_GET])
@app.route(target_url + '/<string:order_id>', methods=[RoCon.HTTP_METHOD_GET])
def api_get_orders(order_id=None):

    if order_id:

        return jsonify(orders_res.get_resource_json(resource_id=order_id))
    else:

        try:
            page = int(request.args.get(RoCon.PARAM_PAGE))
        except:
            page = 0

        return jsonify(orders_res.get_resources_json(page=page))


@app.route(target_url, methods=[RoCon.HTTP_METHOD_POST])
@requires_authentication
def api_post_orders():

    return jsonify(orders_res.create_resource(resource_data=request.get_json()))


@app.route(target_url + '/<string:order_id>', methods=[RoCon.HTTP_METHOD_PUT])
@requires_authentication
def api_patch_order(order_id=None):
    # ?action=set_status {'order_status': 'in_progress'}
    if request.args.get(RoCon.PARAM_ACTION) == RoCon.PARAM_ACTION_SET_STATUS:
        return jsonify(orders_res.update_order_status(order_id=order_id, order_data=request.get_json(), user_obj=None))

    response = ActionResponse(action_name='update_order')
    response.set_data(action_message='invalid_action')
    return jsonify(response.to_dict())


@app.route(target_url + '/<string:order_id>', methods=[RoCon.HTTP_METHOD_DELETE])
@requires_authentication
def api_delete_order(order_id=None):

    return jsonify(orders_res.delete_resource(resource_id=order_id))
