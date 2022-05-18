from unittest.mock import patch

from werkzeug.datastructures import ImmutableMultiDict

from conftest import auth_session


@patch("dataengine.server.routes.note.put_note")
def test_new_stores_note(put_note_mock, client):
    user_id = auth_session(client)
    note_form_data = ImmutableMultiDict({
        'body': 'My note',
        'geo-name': 'NewYork',
        'geo-lat': '-40.00000',
        'geo-lng': '20.023423'
    })

    resp = client.post('/note/', data=note_form_data)

    assert resp.status_code == 302
    put_note_mock.assert_called_with(user_id, note_form_data)
