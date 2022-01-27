from dataclasses import dataclass

from authlib.integrations.flask_client import OAuth
from flask import Flask
from sqlalchemy.orm import Session


@dataclass
class ApplicationContext:
    app: Flask
    auth0: OAuth
    db_session: Session


class Context(object):
    _instance: ApplicationContext = None

    @property
    def instance(self) -> ApplicationContext:
        return self._instance

    @staticmethod
    def set_context(app: Flask, oauth: OAuth, db_session: Session):
        Context._instance = ApplicationContext(app, oauth, db_session)

    @staticmethod
    def app() -> Flask:
        validate_context()
        return Context._instance.app

    @staticmethod
    def auth0() -> OAuth:
        validate_context()
        return Context._instance.auth0

    @staticmethod
    def db_session() -> Session:
        validate_context()
        return Context._instance.db_session


def validate_context():
    if not Context.instance:
        raise ValueError("Context is not set")
