# File: response_constants.py
# Desc:
# Date: November 30, 2016 @ 3:43 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai


class ResponseConstants(object):

    INFO_RESOURCE_FOUND = 'info_resource_s_found'
    INFO_RESOURCE_SAVED = 'info_resource_saved'
    INFO_RESOURCE_DELETED = 'info_resource_deleted'

    ERR_RESOURCE_NOT_FOUND = 'err_resource_not_found'
    ERR_RESOURCE_NOT_SAVED = 'err_resource_not_saved'
    ERR_RESOURCE_NOT_DELETED = 'err_resource_not_deleted'
    ERR_DATABASE_OPERATION = 'err_database_operation'
    ERR_MISSING_JSON_OBJ = 'err_missing_json_obj'
    ERR_MISSING_JSON_KEY = 'err_missing_json_key'
    ERR_NOTHING_TO_UPDATE = 'err_no_data_to_update'

    KEY_ACTION_DATA_DETAIL = 'detail'
    KEY_ACTION_DATA_DATA_SET = 'data_set'
    KEY_ACTION_DATA_DATA_ITEM = 'data_item'
    KEY_ACTION_DATA_PAGE = 'page'
    KEY_ACTION_DATA_IPP = 'items_per_page'
    KEY_ACTION_DATA_TOTAL_ITEMS = 'total_items'
    KEY_ACTION_DATA_TOTAL_PAGES = 'total_pages'
