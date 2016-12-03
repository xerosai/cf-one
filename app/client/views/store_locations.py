# File: store_locations.py
# Desc:
# Date: December 02, 2016 @ 8:23 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

from flask import render_template, request
from app import app
from app.client.utils import session_tools
from app.constants.route_constants import RouteConstants as RoCon
from app.resources.store_locations_resource import StoreLocationsResource
from app.resources.user_profiles_resource import UserProfilesResource


store_loc_res = StoreLocationsResource()
up_res = UserProfilesResource()


@app.route(RoCon.ROUTE_STORE_LOCATIONS, methods=[RoCon.HTTP_METHOD_GET])
def client_get_locations():

    session_profile_or_none = session_tools.get_session_profile()
    current_user_or_none = up_res.get_user_by_auth(
        auth_id=session_tools.get_session_user_id(), user_data=session_profile_or_none
    )

    location_id = request.args.get(RoCon.PARAM_ID)

    if location_id:
        location_data = store_loc_res.get_resource_raw(resource_id=location_id)
        return render_template(
            template_name_or_list='location.html', location_data=location_data, current_user=current_user_or_none
        )
    else:
        try:
            page = int(request.args.get(RoCon.PARAM_PAGE))
        except:
            page = 0

        location_data = store_loc_res.get_resources_json(page=page)

        return render_template(
            template_name_or_list='locations.html', location_data=location_data, current_user=current_user_or_none
        )
