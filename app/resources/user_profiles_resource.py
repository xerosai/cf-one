# File: user_profiles_resource.py
# Desc: Subclass of Model Resource; User Profiles Data Access Class
# Date: November 30, 2016 @ 8:06 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai


import sys
from app.constants.response_constants import ResponseConstants as ReCon
from app.models.orders import Orders
from app.models.user_profiles import UserProfiles
from app.non_db_models.action_response import ActionResponse
from .model_resource import ModelResource


class UserProfilesResource(ModelResource):
    model_or_none = UserProfiles

    def get_user_orders(self, user_id=None, page=0, ipp=10):
        """
        Given a user id, gets orders for a user.

        Keyword arguments:
        user_id -- the user's object id
        page -- the page
        ipp -- the number of items returned per 'page'
        :return:
        """
        response = ActionResponse(action_name='get_orders_for_user')

        user_or_none = self.get_resource_raw(resource_id=user_id)

        if user_or_none is None:
            response.set_data(action_message=ReCon.ERR_RESOURCE_NOT_FOUND)
            return response.to_dict()

        if page < 0 or type(page) is not int:
            page = 0
        if ipp < 10 or type(ipp) is not int:
            ipp = 10

        try:
            orders = Orders.objects(assoc_user=user_or_none).skip(page * ipp).limit(ipp)

            total_items = Orders.objects(assoc_user=user_or_none).count()

            if total_items % ipp == 0:
                total_pages = int(total_items / ipp)
            else:
                total_pages = int(total_items / ipp) + 1
        except:
            response.set_data(action_message=ReCon.ERR_DATABASE_OPERATION, action_data={
                ReCon.KEY_ACTION_DATA_DETAIL: str(sys.exc_info())
            })
            return response.to_dict()
        else:
            if not total_items:
                response.set_data(action_message=ReCon.ERR_RESOURCE_NOT_FOUND, action_data={
                    ReCon.KEY_ACTION_DATA_DETAIL: 'Query returned no results'
                })
                return response.to_dict()

            response.action_result = True
            response.set_data(action_message=ReCon.INFO_RESOURCE_FOUND, action_data={
                ReCon.KEY_ACTION_DATA_DETAIL: 'Query returned a total of {num_res} result(s)'.format(num_res=total_items),
                ReCon.KEY_ACTION_DATA_TOTAL_PAGES: total_pages,
                ReCon.KEY_ACTION_DATA_TOTAL_ITEMS: total_items,
                ReCon.KEY_ACTION_DATA_PAGE: page,
                ReCon.KEY_ACTION_DATA_IPP: ipp,
                ReCon.KEY_ACTION_DATA_DATA_SET: [
                    o.to_dict() if getattr(o, 'to_dict', None) else o.to_json() for o in orders
                ]
            })
            return response.to_dict()
