import datetime
from flask import url_for,current_app
from flask_mail import Message
from cms.form import FormPengikut
from cms.database import Kategori, Tag, Artikel, Halaman, Judul
from cms import mail

def main_context():
    form = FormPengikut()
    kategori = Kategori.query.all()
    blog_name = Judul.query.filter_by(id=1).first()
    topik = Tag.query.all()
    populer = Artikel.query.filter_by(publish = True).order_by(Artikel.dibaca.desc()).limit(5).all()
    halaman = Halaman.query.filter_by(publish=True).all()
    return dict(now=datetime.date.today().year, kategori=kategori, topik=topik, populer=populer, pages=halaman, blog_name=blog_name.judul, form=form,deskripsi_name=blog_name.deskripsi)
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender=current_app.config['MAIL_USERNAME'],recipients=[user.email])
    msg.body = f'''Untuk mereset password, Silahkan klik link ini:{url_for('admin.reset_token', token=token, _external=True)}Jika Anda tidak ingin mengganti password, abaikan pesan ini.'''
    mail.send(msg)