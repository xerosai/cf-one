# File: order_items.py
# Desc: Contains order items routes
# Date: November 30, 2016 @ 8:11 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

from flask import jsonify, request
from app import app
from app.constants.route_constants import RouteConstants as RoCon
from app.resources.cafe_items_resource import CafeItemsResource


cafe_item_res = CafeItemsResource()


@app.route(RoCon.ROUTE_ITEMS, methods=[RoCon.HTTP_METHOD_GET])
@app.route(RoCon.ROUTE_ITEMS + '/<string:resource_id>', methods=[RoCon.HTTP_METHOD_GET])
def api_get_items(resource_id=None):

    if resource_id:
        return jsonify(cafe_item_res.get_resource_json(resource_id=resource_id))
    else:
        try:
            page = int(request.args.get('page'))
        except:
            page = 0

        item_type_or_none = request.args.get(RoCon.PARAM_ITEM_TYPE)

        query_doc = {'item_type': item_type_or_none} if item_type_or_none is not None else None

        return jsonify(cafe_item_res.get_resources_json(page=page, query_doc=query_doc))


@app.route(RoCon.ROUTE_ITEMS, methods=[RoCon.HTTP_METHOD_POST])
def api_post_items():

    return jsonify(cafe_item_res.create_resource(resource_data=request.get_json()))


@app.route(RoCon.ROUTE_ITEMS + '/<string:resource_id>', methods=[RoCon.HTTP_METHOD_PUT])
def api_update_items(resource_id=None):

    return jsonify(cafe_item_res.update_resource(resource_id=resource_id, resource_data=request.get_json()))


@app.route(RoCon.ROUTE_ITEMS + '/<string:resource_id>', methods=[RoCon.HTTP_METHOD_DELETE])
def api_delete_items(resource_id=None):

    return jsonify(cafe_item_res.delete_resource(resource_id=resource_id))
