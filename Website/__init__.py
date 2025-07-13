from dotenv import load_dotenv
import os
from flask import *
import mysql.connector

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'hello world'
    app.mydb = mysql.connector.connect(
        host= 'localhost', #os.getenv('DB_HOST'),
        user= 'root', #os.getenv('DB_USER'),
        password= 'fakepassword', #os.getenv('DB_PASS'),
        port=3306,
        database= 'Mission' #os.getenv('DB_NAME')
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
        if 'last search' not in session:
            session['last search'] = {'lsph': None, 'lcyl':None, 'laxis':None, 'ladd':None,
                                      'rsph':None, 'rcyl':None, 'raxis':None, 'radd':None,
                                      'bridge':None, 'gender':None, 'description':None}


    return app

