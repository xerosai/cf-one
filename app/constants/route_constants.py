# File: route_constants.py
# Desc:
# Date: November 30, 2016 @ 8:12 PM
# Auth: Simon Neufville (simon@xrscodeworks.com) / xerosai


class RouteConstants(object):

    AUTH0_ENDPOINT_USER_DETAIL = 'https://xrscodeworks.auth0.com/tokeninfo'

    HTTP_HEADER_AUTH = 'authorization'

    HTTP_METHOD_DELETE = 'DELETE'
    HTTP_METHOD_GET = 'GET'
    HTTP_METHOD_POST = 'POST'
    HTTP_METHOD_PUT = 'PUT'

    ROUTE_API_BASE = '/api'
    ROUTE_ITEMS = '/items'
    ROUTE_ORDERS = '/orders'
    ROUTE_PROFILES = '/profiles'
    ROUTE_STORE_LOCATIONS = '/locations'
    ROUTE_CLIENT_AUTHORIZE = '/authorize'
    ROUTE_CLIENT_LOGIN = '/login'
    ROUTE_CLIENT_LOGOUT = '/logout'
    ROUTE_CLIENT_HOME = '/home'
    ROUTE_CLIENT_ROOT = '/'

    PARAM_MODE = 'mode'
    PARAM_ID = 'id'
    PARAM_PAGE = 'page'
    PARAM_IPP = 'ipp'
    PARAM_ITEM_TYPE = 'item_type'
    PARAM_ACTION = 'action'

    PARAM_ACTION_SET_STATUS = 'set_status'

