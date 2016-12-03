# File: store_locations_resource.py
# Desc:
# Date: December 02, 2016 @ 8:06 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai


from app.resources.model_resource import ModelResource
from app.models.store_location import StoreLocations


class StoreLocationsResource(ModelResource):
    model_or_none = StoreLocations
