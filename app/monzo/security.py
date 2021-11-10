_MONZO_ACCESS_TOKEN_COOKIE_NAME = 'monzo_api_token'


def set_access_token(resp, token):
    resp.set_cookie(_MONZO_ACCESS_TOKEN_COOKIE_NAME, token)


def get_access_token(req):
    return req.cookies.get(_MONZO_ACCESS_TOKEN_COOKIE_NAME)


def logout(resp):
    resp.delete_cookie(_MONZO_ACCESS_TOKEN_COOKIE_NAME)
