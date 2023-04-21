import re, os, random, string
from typing_extensions import Self
from flask import Flask, request, template_rendered, Blueprint, url_for, redirect, flash, render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from numpy import identity, product
from sqlalchemy import null
from api.api import *
from api.sql import *
from camerastore.views.store import *
# from bookstore.views.store import *
from backstage.views.analysis import *
from backstage.views.manager_c import *
from backstage.views.manager_l import *
from link import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'Your Key' 

app.register_blueprint(api, url_prefix='/')
# app.register_blueprint(store, url_prefix='/camerastore')
app.register_blueprint(store, url_prefix='/camerastore')
# app.register_blueprint(analysis, url_prefix='/backstage')
app.register_blueprint(manager_c, url_prefix='/backstage')
app.register_blueprint(manager_l, url_prefix='/backstage')

login_manager.init_app(app)

@app.route('/') # 函式的裝飾(Decorator): 以函式為基礎，提供附加功能
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True
    app.secret_key = 'Your Key'
    app.run()