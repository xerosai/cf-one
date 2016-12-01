# File: action_response.py
# Desc: JSON-compatible object
# Date: November 30, 2016 @ 3:35 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai


class ActionResponse(object):

    def __init__(self, action_name, action_result=False):
        self.action_name = action_name
        self.action_result = action_result
        self.action_message = ''
        self.action_data = {}

    def set_data(self, action_message, action_data=None):
        self.action_message = action_message

        if action_data and type(action_data) is dict:
            self.action_data = action_data

    def to_dict(self):
        return {
            'action_name': self.action_name,
            'action_result': self.action_result,
            'action_message': self.action_message,
            'action_data': self.action_data
        }
