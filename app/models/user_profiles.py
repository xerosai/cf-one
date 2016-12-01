# File: user_profiles.py
# Desc: Model representing a User's Profile
# Date: November 30, 2016 @ 7:13 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai

import datetime
import mongoengine
from app.constants.model_constants import ModelConstants as MoCon


class UserProfiles(mongoengine.Document):
    created_at = mongoengine.DateTimeField(required=True, default=datetime.datetime.now)
    updated_at = mongoengine.DateTimeField()
    auth0_id = mongoengine.StringField(required=True, unique=True)
    display_picture = mongoengine.StringField(required=True)
    display_name = mongoengine.StringField(required=True, min_length=10)
    email_address = mongoengine.StringField(required=True)
    profile_enabled = mongoengine.BooleanField(required=True, default=True)

    @mongoengine.queryset_manager
    def objects(self, queryset):
        return queryset.order_by('-created_at')

    @mongoengine.queryset_manager
    def active_users(self, queryset):
        return queryset.filter(profile_enabled=True)

    @staticmethod
    def get_required_fields():
        return [
            MoCon.USER_PROFILE_AUTH0_ID,
            MoCon.USER_PROFILE_DISPLAY_NAME,
            MoCon.USER_PROFILE_EMAIL_ADDRESS,
            MoCon.USER_PROFILE_DISPLAY_PICTURE
        ]

    def to_dict(self):

        output = {
            MoCon.COMMON_OBJECT_ID: str(self.id),
            MoCon.COMMON_CREATED_AT: self.created_at.isoformat(),
            MoCon.USER_PROFILE_DISPLAY_NAME: self.display_name,
            MoCon.USER_PROFILE_EMAIL_ADDRESS: self.email_address,
            MoCon.USER_PROFILE_DISPLAY_PICTURE: self.display_picture
        }

        if self.updated_at:
            output[MoCon.COMMON_UPDATED_AT] = self.updated_at

        return output
