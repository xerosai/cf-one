# File: orders_resource.py
# Desc: Subclass of Model Resource; Orders Data Access Class
# Date: November 30, 2016 @ 11:59 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai


from app.models.orders import Orders
from app.models.user_profiles import UserProfiles
from .model_resource import ModelResource


class OrdersResource(ModelResource):
    model_or_none = Orders
