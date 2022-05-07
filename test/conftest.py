from dataengine.common.util import random_str
from fixtures.test_client import client


def auth_session(client, user_id=random_str()):
    with client.session_transaction() as sess:
        sess['profile'] = {'user_id': user_id}

    return user_id
