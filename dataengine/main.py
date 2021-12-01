from dataengine import app


def start_app():
    app.run('0.0.0.0', port=5000)


if __name__ == '__main__':
    start_app()
