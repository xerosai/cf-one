# File: cafe_items_resource.py
# Desc: Subclass of Model Resource; Cafe Items Data Access Class
# Date: November 30, 2016 @ 4:44 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai


from app.constants.response_constants import ResponseConstants as ReCon
from app.models.cafe_items import CafeItems
from app.non_db_models.action_response import ActionResponse
from app.resources.model_resource import ModelResource


class CafeItemsResource(ModelResource):
    model_or_none = CafeItems

    def get_item_and_related(self, item_id=None):
        """
        Gets item and related

        Keyword arguments:
        item_id -- item object id
        """
        response = ActionResponse(action_name='get_item_with_related')

        resource_or_none = self.get_resource_raw(resource_id=item_id)

        if resource_or_none is None:
            response.set_data(action_message=ReCon.ERR_RESOURCE_NOT_FOUND)
            return response.to_dict()

        response.action_result = True

        item_data = {
            ReCon.KEY_ACTION_DATA_DETAIL: 'item found',
            ReCon.KEY_ACTION_DATA_DATA_ITEM: resource_or_none.to_dict() if getattr(resource_or_none, 'to_dict', None) else resource_or_none.to_json()
        }

        try:
            related_items = CafeItems.objects(item_type=resource_or_none.item_type, id__ne=resource_or_none.id)
        except:
            related_items = []

        item_data[ReCon.KEY_ACTION_DATA_RELATED_ITEMS] = [
            r.to_dict() if getattr(r, 'to_dict', None) else r.to_json() for r in related_items
        ]

        response.set_data(action_message=ReCon.INFO_RESOURCE_FOUND, action_data=item_data)
        return response.to_dict()