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

    @staticmethod
    def get_instance() -> ApplicationContext:
        return Context._instance

    @staticmethod
    def set_context(app, oauth, db_session):
        print("setting context")
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
    if not Context.get_instance():
        raise ValueError("Context is not set")
