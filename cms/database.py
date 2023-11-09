from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from flask_select2.contrib.sqla.ajax import QueryAjaxModelLoader
from hashlib import md5
from cms import dbase, login, select2

@login.user_loader
def load_user(idpengguna):
    return Pengguna.query.get(int(idpengguna))

class Pengguna(dbase.Model, UserMixin):
    id = dbase.Column(dbase.Integer, primary_key=True)
    nama = dbase.Column(dbase.String(20), nullable=False)
    surel = dbase.Column(dbase.String(120), unique=True, nullable=False)
    gambar = dbase.Column(dbase.String(20), nullable=False, default='default.jpg')
    kunci = dbase.Column(dbase.String(60), nullable=False)
    biodata = dbase.Column(dbase.String(255))
    sebagai = dbase.Column(dbase.String(60))
    aktifasi = dbase.Column(dbase.Boolean(), nullable=False, default=False)
    tgldaftar = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
    artikel = dbase.relationship('Artikel', backref='penulis', lazy=True)
    halaman = dbase.relationship('Halaman', backref='penulis_halaman', lazy=True)
    kategori = dbase.relationship('Kategori', backref='isikategori', lazy=True)
    def __init__(self, **kwargs):
        super(Pengguna, self).__init__(**kwargs)
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'idpengguna': self.id}).decode('utf-8')
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            idpengguna = s.loads(token)['idpengguna']
        except:
            return None
        return Pengguna.query.get(idpengguna)
    def __repr__(self):
        return "Pengguna('{self.nama}', '{self.surel}', '{self.gambar}')"

class Judul(dbase.Model):
    id = dbase.Column(dbase.Integer, primary_key=True)
    judul = dbase.Column(dbase.String(100), nullable=False)
    deskripsi = dbase.Column(dbase.String(300), nullable=False)
    @staticmethod
    def tambahjudul():
        judul = ['CMSFlask']
        for r in judul:
            judul = Judul.query.filter_by(judul=r).first()
            if judul is None:
                judul = Judul(judul='CMSFlask', deskripsi='Layanan Website Dengan CMSFlask PythonesiaORG')
            dbase.session.add(judul)
        dbase.session.commit()

class Halaman(dbase.Model):
    id = dbase.Column(dbase.Integer, primary_key=True)
    judul = dbase.Column(dbase.String(255), nullable=False)
    isi = dbase.Column(dbase.Text, nullable=False)
    tanggaldibuat = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
    tanggalupdate = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    slug = dbase.Column(dbase.String(255), nullable=False)
    publish = dbase.Column(dbase.Boolean(), nullable=False, server_default='1')
    idpengguna = dbase.Column(dbase.Integer, dbase.ForeignKey('pengguna.id'), nullable=False)
    def __repr__(self):
        return "Artikel('{self.judul}', '{self.tanggaldibuat}')"

class Tag(dbase.Model):
    id = dbase.Column(dbase.Integer, primary_key=True)
    nama = dbase.Column(dbase.Unicode(64))
    slug = dbase.Column(dbase.String(255), nullable=False)
    def __repr__(self):
        return f"{self.nama}"

class Kategori(dbase.Model):
    id = dbase.Column(dbase.Integer, primary_key=True)
    nama = dbase.Column(dbase.String(255), nullable=False)
    slug = dbase.Column(dbase.String(255), nullable=False)
    tanggaldibuat = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
    idpengguna = dbase.Column(dbase.Integer, dbase.ForeignKey('pengguna.id'), nullable=False)
    isiartikel = dbase.relationship('Artikel', backref='kategori', lazy=True)
    def __repr__(self):
        return "Artikel('{self.nama}', '{self.tanggaldibuat}')"

class Komentar(dbase.Model):
    id = dbase.Column(dbase.Integer, primary_key=True)
    nama = dbase.Column(dbase.String(255), nullable=False)
    surel = dbase.Column(dbase.String(120))
    website = dbase.Column(dbase.String(255))
    komentar = dbase.Column(dbase.Text, nullable=False)
    idbalasan = dbase.Column(dbase.Integer, dbase.ForeignKey('komentar.id'))
    tanggalkomen = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
    publish = dbase.Column(dbase.Boolean())
    idartikel = dbase.Column(dbase.Integer, dbase.ForeignKey('artikel.id'), nullable=False)
    dibalas = dbase.relationship('Komentar', backref=dbase.backref('balasan', remote_side=[id]))
    def avatar(self, size):
        digest = md5(self.nama.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    def __repr__(self):
        return "Komentar('{self.komentar}', '{self.tanggalkomen}')"

class Hubungi(dbase.Model):
    id = dbase.Column(dbase.Integer, primary_key=True)
    nama = dbase.Column(dbase.String(255), nullable=False)
    surel = dbase.Column(dbase.String(120), nullable=False)
    pesan = dbase.Column(dbase.TEXT, nullable=False)
    tanggaldibuat = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return "Hubungi('{self.nama}', '{self.tanggaldibuat}')"

class Pengikut(dbase.Model):
    id = dbase.Column(dbase.Integer, primary_key=True)
    surel = dbase.Column(dbase.String(120), unique=True, nullable=False)
    tanggaldibuat = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return "Hubungi('{self.email}', '{self.tanggaldibuat}')"

tag_loader = QueryAjaxModelLoader(
    name='tag',
    session=dbase.session,
    model=Tag,
    fields=['nama'],
    order_by=[Tag.nama.asc()],
    page_size=20,
    placeholder="Pilih tags"
)

select2.add_loader(loader=tag_loader)

tagartikel = dbase.Table('tagartikel', dbase.Model.metadata,dbase.Column('idartikel', dbase.Integer, dbase.ForeignKey('artikel.id')),dbase.Column('idtag', dbase.Integer, dbase.ForeignKey('tag.id')))

class Artikel(dbase.Model):
    id = dbase.Column(dbase.Integer, primary_key=True)
    judul = dbase.Column(dbase.String(255), nullable=False)
    tanggaldibuat = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
    tanggalupdate = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    isi = dbase.Column(dbase.Text, nullable=False)
    gambar = dbase.Column(dbase.String(255), nullable=False, default='default.jpg')
    slug = dbase.Column(dbase.String(255), nullable=False)
    publish = dbase.Column(dbase.Boolean(), nullable=False)
    headline = dbase.Column(dbase.Boolean(), nullable=False)
    private = dbase.Column(dbase.Boolean(), nullable=False)
    dibaca = dbase.Column(dbase.Integer, nullable=False, default=0)
    idpengguna = dbase.Column(dbase.Integer, dbase.ForeignKey('pengguna.id'), nullable=False)
    idkategori = dbase.Column(dbase.Integer, dbase.ForeignKey('kategori.id'), nullable=False)
    tags = dbase.relationship('Tag', secondary=tagartikel, lazy='dynamic', backref='tagger')
    komentar = dbase.relationship('Komentar', backref='isikomentar', lazy='dynamic')
    def __repr__(self):
        return "Artikel('{self.judul}', '{self.tanggaldibuat}')"

class Mesin1(dbase.Model):
     no = dbase.Column(dbase.Integer, primary_key=True)
     ads = dbase.Column(dbase.TEXT, nullable=False)
     ph = dbase.Column(dbase.TEXT, nullable=False)
     air = dbase.Column(dbase.TEXT, nullable=False)
     lembab = dbase.Column(dbase.TEXT, nullable=False)
     hum = dbase.Column(dbase.TEXT, nullable=False)
     temp = dbase.Column(dbase.TEXT, nullable=False)
     hujan = dbase.Column(dbase.TEXT, nullable=False)
     tgl = dbase.Column(dbase.TEXT, nullable=False)
     jam = dbase.Column(dbase.TEXT, nullable=False)
     def __repr__(self):
        return "Mesin1('{self.no}', '{self.tgl}')"

class Mesin2(dbase.Model):
     no = dbase.Column(dbase.Integer, primary_key=True)
     ads = dbase.Column(dbase.TEXT, nullable=False)
     ph = dbase.Column(dbase.TEXT, nullable=False)
     air = dbase.Column(dbase.TEXT, nullable=False)
     lembab = dbase.Column(dbase.TEXT, nullable=False)
     hum = dbase.Column(dbase.TEXT, nullable=False)
     temp = dbase.Column(dbase.TEXT, nullable=False)
     hujan = dbase.Column(dbase.TEXT, nullable=False)
     tgl = dbase.Column(dbase.TEXT, nullable=False)
     jam = dbase.Column(dbase.TEXT, nullable=False)
     def __repr__(self):
        return "Mesin2('{self.no}', '{self.tgl}')"

class Mesin3(dbase.Model):
     no = dbase.Column(dbase.Integer, primary_key=True)
     ads = dbase.Column(dbase.TEXT, nullable=False)
     ph = dbase.Column(dbase.TEXT, nullable=False)
     air = dbase.Column(dbase.TEXT, nullable=False)
     lembab = dbase.Column(dbase.TEXT, nullable=False)
     hum = dbase.Column(dbase.TEXT, nullable=False)
     temp = dbase.Column(dbase.TEXT, nullable=False)
     hujan = dbase.Column(dbase.TEXT, nullable=False)
     tgl = dbase.Column(dbase.TEXT, nullable=False)
     jam = dbase.Column(dbase.TEXT, nullable=False)
     def __repr__(self):
        return "Mesin3('{self.no}', '{self.tgl}')"

class Mesin4(dbase.Model):
     no = dbase.Column(dbase.Integer, primary_key=True)
     ads = dbase.Column(dbase.TEXT, nullable=False)
     ph = dbase.Column(dbase.TEXT, nullable=False)
     air = dbase.Column(dbase.TEXT, nullable=False)
     lembab = dbase.Column(dbase.TEXT, nullable=False)
     hum = dbase.Column(dbase.TEXT, nullable=False)
     temp = dbase.Column(dbase.TEXT, nullable=False)
     hujan = dbase.Column(dbase.TEXT, nullable=False)
     tgl = dbase.Column(dbase.TEXT, nullable=False)
     jam = dbase.Column(dbase.TEXT, nullable=False)
     def __repr__(self):
        return "Mesin4('{self.no}', '{self.tgl}')"

class Anggotatani(dbase.Model):
     no = dbase.Column(dbase.Integer, primary_key=True)
     nama = dbase.Column(dbase.TEXT, nullable=False)
     alamat = dbase.Column(dbase.TEXT, nullable=False)
     luas = dbase.Column(dbase.TEXT, nullable=False)
     lati = dbase.Column(dbase.TEXT, nullable=False)
     longi = dbase.Column(dbase.TEXT, nullable=False)
     gambar = dbase.Column(dbase.TEXT, nullable=False)
     tanggaldibuat = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
     sesi = dbase.Column(dbase.TEXT, nullable=False)

class Pupuk(dbase.Model):
     no = dbase.Column(dbase.Integer, primary_key=True)
     nama = dbase.Column(dbase.TEXT, nullable=False)
     alamat = dbase.Column(dbase.TEXT, nullable=False)
     namapupuk = dbase.Column(dbase.TEXT, nullable=False)
     stok = dbase.Column(dbase.TEXT, nullable=False)
     longi = dbase.Column(dbase.TEXT, nullable=False)
     gambar = dbase.Column(dbase.TEXT, nullable=False)
     tanggaldibuat = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
     sesi = dbase.Column(dbase.TEXT, nullable=False)

class Pemeliharaan(dbase.Model):
     no = dbase.Column(dbase.Integer, primary_key=True)
     nama = dbase.Column(dbase.TEXT, nullable=False)
     pekerjaan = dbase.Column(dbase.TEXT, nullable=False)
     luas = dbase.Column(dbase.TEXT, nullable=False)
     lati = dbase.Column(dbase.TEXT, nullable=False)
     longi = dbase.Column(dbase.TEXT, nullable=False)
     gambar = dbase.Column(dbase.TEXT, nullable=False)
     tanggaldibuat = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
     sesi = dbase.Column(dbase.TEXT, nullable=False)

class Penanaman(dbase.Model):
     no = dbase.Column(dbase.Integer, primary_key=True)
     nama = dbase.Column(dbase.TEXT, nullable=False)
     luas = dbase.Column(dbase.TEXT, nullable=False)
     varitas = dbase.Column(dbase.TEXT, nullable=False)
     lati = dbase.Column(dbase.TEXT, nullable=False)
     longi = dbase.Column(dbase.TEXT, nullable=False)
     gambar = dbase.Column(dbase.TEXT, nullable=False)
     tanggaldibuat = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
     sesi = dbase.Column(dbase.TEXT, nullable=False)

class Panen(dbase.Model):
     no = dbase.Column(dbase.Integer, primary_key=True)
     nama = dbase.Column(dbase.TEXT, nullable=False)
     hasilpanen = dbase.Column(dbase.TEXT, nullable=False)
     luas = dbase.Column(dbase.TEXT, nullable=False)
     tanggaldibuat = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
     sesi = dbase.Column(dbase.TEXT, nullable=False)

class Gudang(dbase.Model):
     no = dbase.Column(dbase.Integer, primary_key=True)
     nama = dbase.Column(dbase.TEXT, nullable=False)
     beras = dbase.Column(dbase.TEXT, nullable=False)
     jumlah = dbase.Column(dbase.TEXT, nullable=False)
     tanggaldibuat = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
     sesi = dbase.Column(dbase.TEXT, nullable=False)

class Namaalat(dbase.Model):
     no = dbase.Column(dbase.Integer, primary_key=True)
     nama = dbase.Column(dbase.TEXT, nullable=False)
     alamat = dbase.Column(dbase.TEXT, nullable=False)
     lati = dbase.Column(dbase.TEXT, nullable=False)
     longi = dbase.Column(dbase.TEXT, nullable=False)
     gambar = dbase.Column(dbase.TEXT, nullable=False)
     tanggaldibuat = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
     sesi = dbase.Column(dbase.TEXT, nullable=False)

class Kondisialato(dbase.Model):
     no = dbase.Column(dbase.Integer, primary_key=True)
     nama = dbase.Column(dbase.TEXT, nullable=False)
     kondisi = dbase.Column(dbase.TEXT, nullable=False)
     gambar= dbase.Column(dbase.TEXT, nullable=False)
     tanggaldibuat = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
     sesi = dbase.Column(dbase.TEXT, nullable=False)





