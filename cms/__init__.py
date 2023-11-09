import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_select2 import Select2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_wtf import CSRFProtect
from .waktu import indonesia_time
from .konfigurasi import Konfigurasi

basedir = os.path.abspath(os.path.dirname(__file__))

dbase = SQLAlchemy()
migrasi = Migrate()
ma = Marshmallow()
bcrypt = Bcrypt()
select2 = Select2()
mail = Mail()
ckeditor = CKEditor()
csrf = CSRFProtect()

login = LoginManager()
login.login_view = 'admin.login'
login.login_message_category = 'is-warning'
login.login_message = "Silahkan login untuk akses halaman ini."

def create_app(config_class=Konfigurasi):
    app = Flask(__name__)
    app.config.from_object(Konfigurasi)
    dbase.init_app(app)
    mail.init_app(app)
    migrasi.init_app(app, dbase)
    ma.init_app(app)
    bcrypt.init_app(app)
    ckeditor.init_app(app)
    csrf.init_app(app)  
    select2.init_app(app)
    login.init_app(app)
    from cms.admin.view import admin
    app.register_blueprint(admin)
    from cms.main.view import main
    app.register_blueprint(main)
    app.jinja_env.filters['indonesia_time'] = indonesia_time
    return app

