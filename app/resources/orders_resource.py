# File: orders_resource.py
# Desc: Subclass of Model Resource; Orders Data Access Class
# Date: November 30, 2016 @ 11:59 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai


import datetime
import sys
from app.constants.model_constants import ModelConstants as MoCon
from app.constants.response_constants import ResponseConstants as ReCon
from app.non_db_models.action_response import ActionResponse
from app.models.orders import Orders
from app.models.user_profiles import UserProfiles
from .model_resource import ModelResource


class OrdersResource(ModelResource):
    model_or_none = Orders

    def update_order_status(self, order_id=None, order_data=None, user_obj=None):
        """
        Updates an order's status

        Keyword arguments:
        order_id -- the object id for the order
        order_data -- a dictionary containing the order status
        user_obj -- the user responsible for making the update
        """
        response = ActionResponse(action_name='update_order_status')

        order_or_none = self.get_resource_raw(resource_id=order_id)

        if order_or_none is None:
            response.set_data(action_message=ReCon.ERR_RESOURCE_NOT_FOUND)
            return response.to_dict()

        if not order_data or type(order_data) is not dict:
            response.set_data(action_message=ReCon.ERR_MISSING_JSON_OBJ)
            return response.to_dict()

        if MoCon.ORDERS_ORDER_STATUS not in order_data:
            response.set_data(action_message=ReCon.ERR_MISSING_JSON_KEY)
            return response.to_dict()

        # if not user_obj or type(user_obj) is not UserProfiles:
        #     response.set_data(action_message=ReCon.ERR_MISSING_USER_OBJ)
        #     return response.to_dict()

        order_or_none.order_status = order_data[MoCon.ORDERS_ORDER_STATUS]
        order_or_none.updated_at = datetime.datetime.now()
        # order_or_none.updated_by = user_obj

        try:
            order_or_none.save()
        except:
            response.set_data(action_message=ReCon.ERR_DATABASE_OPERATION, action_data={
                ReCon.KEY_ACTION_DATA_DETAIL: str(sys.exc_info())
            })
            return response.to_dict()
        else:
            response.action_result = True
            response.set_data(action_message=ReCon.INFO_RESOURCE_SAVED)
            return response.to_dict()
