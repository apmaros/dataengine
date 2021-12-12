from dataclasses import dataclass
from flask import Flask
from authlib.integrations.flask_client import OAuth


@dataclass
class ApplicationContext:
    app: Flask
    auth0: OAuth


class Context(object):
    _instance: ApplicationContext = None

    @property
    def instance(self) -> ApplicationContext:
        return self._instance

    @staticmethod
    def set_context(app, oauth):
        Context._instance = ApplicationContext(app, oauth)

    @staticmethod
    def app() -> Flask:
        validate_context()
        return Context._instance.app

    @staticmethod
    def auth0() -> OAuth:
        validate_context()
        return Context._instance.auth0


def validate_context():
    if not Context.instance:
        raise ValueError("Context is not set")
