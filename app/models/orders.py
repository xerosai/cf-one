# File: orders.py
# Desc: Model representing orders and related items
# Date: November 30, 2016 @ 5:22 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

import datetime
import mongoengine
from app.constants.model_constants import ModelConstants as MoCon
from .cafe_items import CafeItems
from .user_profiles import UserProfiles


class OrderItem(mongoengine.EmbeddedDocument):
    related_item = mongoengine.ReferenceField(CafeItems, required=True)
    quantity = mongoengine.IntField(required=True, min_value=1, default=1)
    unit_cost = mongoengine.FloatField(required=True, min_value=1.0, default=1.0)
    item_size = mongoengine.StringField(required=True)

    def to_dict(self):
        return {
            'related_item': self.related_item.to_dict() if getattr(self.related_item, 'to_dict', None) else self.related_item.to_json(),
            'quantity': self.quantity,
            'unit_cost': self.unit_cost,
            'item_size': self.item_size
        }


class Orders(mongoengine.Document):
    created_at = mongoengine.DateTimeField(required=True, default=datetime.datetime.now)
    updated_at = mongoengine.DateTimeField()
    assoc_user = mongoengine.ReferenceField(UserProfiles, required=True)
    order_status = mongoengine.StringField(required=True, choices=['new', 'in_progress', 'ready'], default='new')
    order_items = mongoengine.EmbeddedDocumentListField(OrderItem, required=True)
    updated_by = mongoengine.ReferenceField(UserProfiles)

    @mongoengine.queryset_manager
    def objects(self, queryset):
        return queryset.order_by('-created_at')

    @mongoengine.queryset_manager
    def open_orders(self, queryset):
        return queryset.filter(order_status='new')

    @mongoengine.queryset_manager
    def ready_orders(self, queryset):
        return queryset.filter(order_status='ready')

    @staticmethod
    def get_required_fields():
        return [
            MoCon.COMMON_ASSOC_USER,
            MoCon.ORDERS_ORDER_ITEMS
        ]

    def to_dict(self):
        output = {
            MoCon.COMMON_OBJECT_ID: str(self.id),
            MoCon.COMMON_CREATED_AT: self.created_at.isoformat(),
            MoCon.COMMON_ASSOC_USER: self.assoc_user.to_dict() if getattr(self.assoc_user, 'to_dict', None) else self.assoc_user.to_json(),
            MoCon.ORDERS_ORDER_STATUS: self.order_status,
            MoCon.ORDERS_ORDER_ITEMS: [
                i.to_dict() if getattr(i, 'to_dict', None) else i.to_json() for i in self.order_items
            ]
        }

        return output
