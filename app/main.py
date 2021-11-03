from app.view import transactions_view
from app.server import dash_app


def start():
    transactions_view.init(app=dash_app)


if __name__ == '__main__':
    start()