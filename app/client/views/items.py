# File: items.py
# Desc:
# Date: December 01, 2016 @ 5:35 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

from flask import render_template, request
from app import app
from app.client.utils import session_tools
from app.constants.route_constants import RouteConstants as RoCon
from app.resources.cafe_items_resource import CafeItemsResource
from app.resources.user_profiles_resource import UserProfilesResource


item_res = CafeItemsResource()
up_res = UserProfilesResource()


@app.route(RoCon.ROUTE_ITEMS, methods=[RoCon.HTTP_METHOD_GET])
def client_get_items():

    session_profile_or_none = session_tools.get_session_profile()
    current_user_or_none = up_res.get_user_by_auth(
        auth_id=session_tools.get_session_user_id(), user_data=session_profile_or_none
    )

    item_id = request.args.get(RoCon.PARAM_ID)

    if item_id:
        # get item data
        item_data = item_res.get_item_and_related(item_id=item_id)
        # check mode
        if request.args.get(RoCon.PARAM_ACTION) == 'edit':
            # check user session and perms
            return 'edit item'

        return render_template(
            template_name_or_list='item.html', item_data=item_data, current_user=current_user_or_none
        )
    else:
        try:
            page = int(request.args.get(RoCon.PARAM_PAGE))
        except:
            page = 0

        # get data
        item_data = item_res.get_resources_json(page=page)

        return render_template(
            template_name_or_list='items.html', item_listing=item_data, current_user=current_user_or_none
        )
