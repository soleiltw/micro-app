from bottle import run

from app.app import init_app

app = application = init_app()

if __name__ == '__main__':
    run(app, debug=True, reloader=True, port=1000)
