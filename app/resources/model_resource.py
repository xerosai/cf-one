# File: model_resource.py
# Desc: Generic Data Access Class, CRUD operations
# Date: November 30, 2016 @ 3:26 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai


import sys
from app.constants.response_constants import ResponseConstants as ReCon
from app.non_db_models.action_response import ActionResponse


class ModelResource(object):
    model_or_none = None

    # Create
    def create_resource(self, resource_data=None):
        """
        Given some data, creates a resource and returns a JSON-compatible response
        resource_data -- dictionary containing resource data
        """
        response = ActionResponse(action_name='create_resource')

        if not resource_data:
            response.set_data(action_message=ReCon.ERR_MISSING_JSON_OBJ)
            return response.to_dict()

        if getattr(self.model_or_none, 'get_required_fields', None):
            for r_key in self.model_or_none.get_required_fields():
                if r_key not in resource_data:
                    response.set_data(action_message=ReCon.ERR_MISSING_JSON_KEY, action_data={
                        ReCon.KEY_ACTION_DATA_DETAIL: 'Missing JSON Key -> {json_key}'.format(json_key=r_key)
                    })
                    return response.to_dict()

        resource = self.model_or_none(**resource_data)

        try:
            resource.save()
        except:
            response.set_data(action_message=ReCon.ERR_DATABASE_OPERATION, action_data={
                ReCon.KEY_ACTION_DATA_DETAIL: str(sys.exc_info())
            })
            return response.to_dict()
        else:
            response.action_result = True
            response.set_data(action_message=ReCon.INFO_RESOURCE_SAVED)
            return response.to_dict()

    # Read
    def get_resource_raw(self, resource_id):
        """
        Given a model (self.model_or_none), returns a resource.

        Keyword arguments:
        resource_id -- the object id for a resource
        """
        if not resource_id:
            return None

        if self.model_or_none is None:
            return None

        try:
            resource = self.model_or_none.objects(id=resource_id).get()
        except:
            return None
        else:
            return resource

    def get_resource_json(self, resource_id):
        """
        Gets a resource or None as a JSON-compatible object

        Keyword arguments:
        resource_id -- the object id for a resource
        """
        response = ActionResponse(action_name='get_resource')

        resource_or_none = self.get_resource_raw(resource_id=resource_id)

        if resource_or_none is None:
            response.set_data(action_message=ReCon.ERR_RESOURCE_NOT_FOUND, action_data={
                ReCon.KEY_ACTION_DATA_DETAIL: 'resource not found for given identifier'
            })
            return response.to_dict()

        response.action_result = True
        response.set_data(action_message=ReCon.INFO_RESOURCE_FOUND, action_data={
            ReCon.KEY_ACTION_DATA_DETAIL: 'resource found',
            ReCon.KEY_ACTION_DATA_DATA_ITEM: resource_or_none.to_dict() if getattr(resource_or_none, 'to_dict', None) else resource_or_none.to_json()
        })
        return response.to_dict()

    def get_resources_json(self, page=0, ipp=10, query_doc=None):
        """
        Gets a list of resources as a JSON-compatible object.

        Keyword arguments:
        page -- when used in conjunction with ipp (items per page) defines pagination
        ipp -- controls the maximum number of items returned per 'page'
        query_doc -- a dictionary to be used as a query document
        """
        response = ActionResponse(action_name='get_resources')

        if page < 0 or type(page) is not int:
            page = 0

        if ipp < 3 or type(ipp) is not int:
            ipp = 10

        if not query_doc or type(query_doc) is not dict:
            query_doc = {}

        try:
            resources = self.model_or_none.objects(__raw__=query_doc).skip(page * ipp).limit(ipp)

            total_items = self.model_or_none.objects(__raw__=query_doc).count()

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
                ReCon.KEY_ACTION_DATA_DETAIL: 'Query returned a total of {num_res} result(s)'.format(
                    num_res=total_items
                ),
                ReCon.KEY_ACTION_DATA_TOTAL_ITEMS: total_items,
                ReCon.KEY_ACTION_DATA_TOTAL_PAGES: total_pages,
                ReCon.KEY_ACTION_DATA_DATA_SET: [
                    r.to_dict() if getattr(r, 'to_dict', None) else r.to_json() for r in resources
                ],
                ReCon.KEY_ACTION_DATA_PAGE: page,
                ReCon.KEY_ACTION_DATA_IPP: ipp
            })
            return response.to_dict()

    # Update
    def update_resource(self, resource_id=None, resource_data=None):
        """
        Given some data, updates a resource specified by an identifier.

        Keyword arguments:
        resource_id -- the object id for the resource
        resource_data -- dictionary containing data
        """
        response = ActionResponse(action_name='update_resource')

        resource_or_none = self.get_resource_raw(resource_id=resource_id)

        if resource_or_none is None:
            response.set_data(action_message=ReCon.ERR_RESOURCE_NOT_FOUND)
            return response.to_dict()

        if not resource_data or type(resource_data) is not dict:
            response.set_data(action_message=ReCon.ERR_MISSING_JSON_OBJ)
            return response.to_dict()

        should_update = False

        for k, v in resource_data.items():
            if hasattr(resource_or_none, 'k'):
                resource_or_none.k = v
                should_update = True

        if should_update:
            try:
                resource_or_none.save()
            except:
                response.set_data(action_message=ReCon.ERR_DATABASE_OPERATION, action_data={
                    ReCon.KEY_ACTION_DATA_DETAIL: str(sys.exc_info())
                })
                return response.to_dict()
            else:
                response.action_result = True
                response.set_data(action_message=ReCon.INFO_RESOURCE_SAVED)
                return response.to_dict()
        else:
            response.set_data(action_message=ReCon.ERR_NOTHING_TO_UPDATE)
            return response.to_dict()

    # Delete
    def delete_resource(self, resource_id=None):
        """
        Given an identifier, deletes a resource and returns a JSON-compatible response.
        ** Subclasses can override this method to add additional checks

        Keyword arguments:
        resource_id -- the object id for the resource
        """
        response = ActionResponse(action_name='delete_resource')

        resource_or_none = self.get_resource_raw(resource_id=resource_id)

        if resource_or_none is None:
            response.set_data(action_message=ReCon.ERR_RESOURCE_NOT_FOUND)
            return response.to_dict()

        try:
            resource_or_none.delete()
        except:
            response.set_data(action_message=ReCon.ERR_DATABASE_OPERATION, action_data={
                ReCon.KEY_ACTION_DATA_DETAIL: str(sys.exc_info())
            })
            return response.to_dict()
        else:
            response.action_result = True
            response.set_data(action_message=ReCon.INFO_RESOURCE_DELETED)
            return response.to_dict()
