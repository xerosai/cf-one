# File: items.py
# Desc: Model representing items for sale in our fake coffee shop
# Date: November 30, 2016 @ 2:46 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

import datetime
import mongoengine
from app.constants.model_constants import ModelConstants as MoCon


class CafeItemCostSpec(mongoengine.EmbeddedDocument):
    spec_item_size = mongoengine.StringField(required=True, choices=['s', 'm', 'l', 'xl'], default='m')
    spec_item_cost = mongoengine.FloatField(required=True, min_value=1.0)

    @staticmethod
    def get_required_fields():
        return [
            MoCon.ITEM_COST_SPEC_SIZE,
            MoCon.ITEM_COST_SPEC_COST
        ]

    def to_dict(self):
        return {
            MoCon.ITEM_COST_SPEC_SIZE: self.spec_item_size,
            MoCon.ITEM_COST_SPEC_COST: self.spec_item_cost
        }


class CafeItems(mongoengine.Document):
    created_at = mongoengine.DateTimeField(required=True, default=datetime.datetime.now)
    updated_at = mongoengine.DateTimeField()
    item_img = mongoengine.StringField(required=True)
    item_name = mongoengine.StringField(required=True, min_length=5)
    item_desc = mongoengine.StringField(required=True, min_length=10)
    item_type = mongoengine.StringField(required=True, min_length=3)
    item_cost_spec = mongoengine.EmbeddedDocumentListField(CafeItemCostSpec, required=True)

    @mongoengine.queryset_manager
    def objects(self, queryset):
        return queryset.order_by('-created_at')

    @mongoengine.queryset_manager
    def objects_by_name(self, queryset):
        return queryset.order_by('item_name')

    @staticmethod
    def get_required_fields():
        return [
            MoCon.CAFE_ITEM_IMG,
            MoCon.CAFE_ITEM_NAME,
            MoCon.CAFE_ITEM_DESC,
            MoCon.CAFE_ITEM_TYPE,
            MoCon.CAFE_ITEM_COST_SPEC
        ]

    def to_dict(self):
        output = {
            MoCon.COMMON_OBJECT_ID: str(self.id),
            MoCon.COMMON_CREATED_AT: self.created_at.isoformat(),
            MoCon.CAFE_ITEM_IMG: self.item_img,
            MoCon.CAFE_ITEM_NAME: self.item_name,
            MoCon.CAFE_ITEM_DESC: self.item_desc,
            MoCon.CAFE_ITEM_TYPE: self.item_type,
            MoCon.CAFE_ITEM_COST_SPEC: [
                i.to_dict() if getattr(i, 'to_dict', None) else i.to_json() for i in self.item_cost_spec
            ]
        }
        if self.item_img:
            output[MoCon.CAFE_ITEM_IMG] = self.item_img

        if self.updated_at:
            output[MoCon.COMMON_UPDATED_AT] = self.updated_at

        return output
