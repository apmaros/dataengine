_MONZO_ACCESS_TOKEN_COOKIE_NAME = 'monzo_api_token'
_MONZO_ACCOUNT_ID_COOKIE_NAME = 'monzo_account_id'


def set_access_token(resp, token):
    resp.set_cookie(_MONZO_ACCESS_TOKEN_COOKIE_NAME, token)


def set_account_id(resp, account_id):
    resp.set_cookie(_MONZO_ACCOUNT_ID_COOKIE_NAME, account_id)


def get_access_token(req):
    return req.cookies.get(_MONZO_ACCESS_TOKEN_COOKIE_NAME)


def get_account_id(req):
    return req.cookies.get(_MONZO_ACCOUNT_ID_COOKIE_NAME)


def logout(resp):
    resp.delete_cookie(_MONZO_ACCESS_TOKEN_COOKIE_NAME)
