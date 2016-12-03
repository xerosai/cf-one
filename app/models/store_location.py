# File: store_location.py
# Desc:
# Date: December 02, 2016 @ 7:58 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

import datetime
import mongoengine
from app.constants.model_constants import ModelConstants as MoCon


class StoreLocations(mongoengine.Document):
    created_at = mongoengine.DateTimeField(required=True, default=datetime.datetime.now)
    updated_at = mongoengine.DateTimeField()
    image_path = mongoengine.StringField(required=True, default='location_1.jpg')
    store_name = mongoengine.StringField(required=True)
    store_addr = mongoengine.StringField(required=True)
    store_city = mongoengine.StringField(required=True)
    country = mongoengine.StringField()

    @mongoengine.queryset_manager
    def objects(self, queryset):
        return queryset.order_by('-created_at')

    @staticmethod
    def get_required_fields():
        return [
            MoCon.STORE_LOCATION_IMG_PATH,
            MoCon.STORE_LOCATION_STORE_NAME,
            MoCon.STORE_LOCATION_STORE_ADDR,
            MoCon.STORE_LOCATION_STORE_CITY,
            MoCon.STORE_LOCATION_COUNTRY
        ]

    def to_dict(self):

        output = {
            MoCon.COMMON_OBJECT_ID: str(self.id),
            MoCon.COMMON_CREATED_AT: self.created_at.isoformat(),
            MoCon.STORE_LOCATION_IMG_PATH: self.image_path,
            MoCon.STORE_LOCATION_STORE_NAME: self.store_name,
            MoCon.STORE_LOCATION_STORE_ADDR: self.store_addr,
            MoCon.STORE_LOCATION_STORE_CITY: self.store_city,
            MoCon.STORE_LOCATION_COUNTRY: self.country
        }

        return output
