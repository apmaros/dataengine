import os


def is_dev():
    return os.getenv('FLASK_ENV') == "development"
