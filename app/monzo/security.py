import os

MONZO_API_CODE_COOKIE_NAME = 'monzo_api_code'
MONZO_ACCESS_TOKEN_COOKIE_NAME = 'monzo_api_token'


def set_access_token(resp, token):
    resp.set_cookie(MONZO_ACCESS_TOKEN_COOKIE_NAME, token)


def get_access_token(req):
    return req.cookies.get(MONZO_ACCESS_TOKEN_COOKIE_NAME)


def get_authenticated_headers(req):
    return {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f"Bearer {get_access_token(req)}"
    }


def logout(resp):
    resp.delete_cookie(MONZO_ACCESS_TOKEN_COOKIE_NAME)
