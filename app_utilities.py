
from os import environ
import urllib.parse


def get_auth_cookie():
    # Retrieve user data from cookie
    cookie = environ.get('HTTP_COOKIE', '')
    if cookie != '':
        data = cookie.split('; ')
        cookie = {}
        for param in data:
            pair = param.split('=')
            if len(pair) == 2:
                cookie[pair[0]] = pair[1]
    else:
        cookie = {}

    site = {
        'id': cookie.get('user', ''),
        # 'password': cookie.get('password', ''),
        'is_admin': cookie.get('user', '') == '000000'
    }
    return site


def get_get_data():
    data = environ.get('QUERY_STRING', '')
    if data != '':
        return urllib.parse.parse_qs(data)
    else:
        return {}
