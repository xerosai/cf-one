# File: orders.py
# Desc:
# Date: November 30, 2016 @ 11:56 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

from flask import jsonify, request
from app import app
from app.constants.route_constants import RouteConstants as RoCon
from app.resources.orders_resource import OrdersResource


orders_res = OrdersResource()


@app.route(RoCon.ROUTE_ORDERS, methods=[RoCon.HTTP_METHOD_GET])
@app.route(RoCon.ROUTE_ORDERS + '/<string:order_id>', methods=[RoCon.HTTP_METHOD_GET])
def api_get_orders(order_id=None):

    if order_id:

        return jsonify(orders_res.get_resource_json(resource_id=order_id))
    else:

        try:
            page = int(request.args.get(RoCon.PARAM_PAGE))
        except:
            page = 0

        return jsonify(orders_res.get_resources_json(page=page))


@app.route(RoCon.ROUTE_ORDERS, methods=[RoCon.HTTP_METHOD_POST])
def api_post_orders():

    return jsonify(orders_res.create_resource(resource_data=request.get_json()))
