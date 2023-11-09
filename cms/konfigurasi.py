import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Konfigurasi:
    SECRET_KEY = os.getenv('SECRET_KEY', default='PytHoneNEsia')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', default='sqlite:///permadi.db')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('EMAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    UPLOADED_PATH = os.path.join(basedir, 'static/upload')
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_HEIGHT = 400
    CKEDITOR_EXTRA_PLUGINS = ['youtube']
    CKEDITOR_FILE_UPLOADER = 'admin.upload'
    CKEDITOR_ENABLE_CSRF = True
    DIREKTORI = basedir
    SQLALCHEMY_TRACK_MODIFICATIONS = False
