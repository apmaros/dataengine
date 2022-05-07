import pytest

from dataengine import app


@pytest.fixture
def client():
    """Configures the app for testing

    :return: App for testing
    """

    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'mysecret'
    client = app.test_client()

    yield client
