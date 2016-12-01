# File: cafe_items_resource.py
# Desc: Subclass of Model Resource; Cafe Items Data Access Class
# Date: November 30, 2016 @ 4:44 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai


from app.models.cafe_items import CafeItems
from app.resources.model_resource import ModelResource


class CafeItemsResource(ModelResource):
    model_or_none = CafeItems
