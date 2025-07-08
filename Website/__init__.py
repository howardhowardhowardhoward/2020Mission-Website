from flask import *
import mysql.connector

def create_app():
    app = Flask(__name__)
    app.secret_key = 'hello world'
    app.mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='fakepassword',
        port=3306,
        database="Mission"
    )

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    @app.before_request
    def logged_in():
        if 'logged_in' not in session:
            session['logged_in'] = False
    @app.before_request
    def keep_results():
        if 'attributes' not in session:
            session['attributes'] = ''
        if 'id' not in session:
            session['id'] = ''

    return app

