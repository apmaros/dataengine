from src.view import transactions_view
from src.server import dash_app


def start():
    transactions_view.init(app=dash_app)


if __name__ == '__main__':
    start()
