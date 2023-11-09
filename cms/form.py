from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField
from flask_select2.model.fields import AjaxSelectMultipleField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import EmailField
from cms.database import Pengguna, tag_loader, Pengikut

class FormUpdateAkun(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', render_kw={'disabled':True})
    role = SelectField('Role', validators=[DataRequired()], choices = [])
    biografi = TextAreaField('Biografi')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    active = BooleanField('Active')
    submit = SubmitField('Update')
    def validate_email(self, email):
        if email.data:
            raise ValidationError('Email tidak dapat diganti')

class FormArtikel(FlaskForm):
    title = StringField('Judul', validators=[DataRequired()])
    kategori = SelectField('Kategori', validators=[DataRequired()], choices = [])
    content = CKEditorField('Isi', validators=[DataRequired()])
    thumbnail = FileField('Gambar Thumbnail', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    is_headline = BooleanField('Headline', default=False)
    private = BooleanField('Private', default=False)
    publish = BooleanField('Publish', default=False)
    multiple_company = AjaxSelectMultipleField(loader=tag_loader,label='Masukkan Tags',allow_blank=False,validators=[DataRequired()])
    submit = SubmitField('Kirim')

class FormHalaman(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    is_active = BooleanField('Tayangkan', default=True)
    submit = SubmitField('Kirim')

class FormKategori(FlaskForm):
    nama = StringField('Nama kategori', validators=[DataRequired()])
    is_gutters = BooleanField('Jadikan Gutters', default=False)
    submit = SubmitField('Submit')
    def validate_nama(form, field):
        if len(field.data) < 3:
            raise ValidationError('Nama harus lebih dari 3 huruf')

class FormRegistrasi(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)], render_kw={'placeholder': 'Nama', 'autocomplete': 'off'})
    email = StringField('Email',validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email', 'autocomplete': 'off'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'Password', 'autocomplete': 'off'})
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder': 'ConfirmPassword'})
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = Pengguna.query.filter_by(nama=username.data).first()
        if user:
            raise ValidationError('Username sudah ada yang mendaftar. Silahkan pilih yang lain')

class FormTambahadmin(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)], render_kw={'placeholder': 'Nama', 'autocomplete': 'off'})
    email = StringField('Email',validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email', 'autocomplete': 'off'})
    sebagai = StringField('Sebagai',validators=[DataRequired(), Length(min=2, max=20)], render_kw={'placeholder': 'Sebagai', 'autocomplete': 'off'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'Password', 'autocomplete': 'off'})
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder': 'ConfirmPassword'})
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = Pengguna.query.filter_by(nama=username.data).first()
        if user:
            raise ValidationError('Username sudah ada yang mendaftar. Silahkan pilih yang lain')

class FormLogin(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email','autocomplete': 'off'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'Password','autocomplete': 'off'})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class FormMasuk(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email','autocomplete': 'off'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'Password','autocomplete': 'off'})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class FormPermintaanReset(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email'})
    submit = SubmitField('Request Password Reset')
    def validate_email(self, email):
        user = Pengguna.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email belum pernah didaftarkan. Anda dapat registrasi dengan email tersebut.')

class FormResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'Password baru'})
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(message='Tidak boleh kosong'), EqualTo('password', message='Harus sama dengan field diatas')], render_kw={'placeholder': 'Ulangi password baru'})
    submit = SubmitField('Reset Password')
    
class FormTag(FlaskForm):
    nama = StringField('Nama Tag', validators=[DataRequired()])
    submit = SubmitField('Submit')

class FormSebagai(FlaskForm):
    nama = StringField('Nama Role', validators=[DataRequired()])
    submit = SubmitField('Submit')

class FormPengikut(FlaskForm):
    email = EmailField(validators=[DataRequired(), Email()], render_kw={"placeholder": "Alamat Anda Email"})
    submit = SubmitField('Berlangganan')
    def validate_email(self, email):
        subscriber = Pengikut.query.filter_by(surel=email.data).first()
        if subscriber:
            raise ValidationError('Email sudah pernah didaftarkan, cek email Anda')

class FormKomentar(FlaskForm):
    nama = StringField('Nama',validators=[DataRequired(), Length(min=3)], render_kw={'placeholder': 'Nama'})
    email = StringField('Email',validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email'})
    website = StringField('Website', render_kw={'placeholder': 'http://www.pythonensia.org'})
    comment = TextAreaField('Komentar', validators=[DataRequired()], render_kw={'placeholder': 'Tinggalkan komentar'})
    submit = SubmitField('Submit')

class FormBalasan(FlaskForm):
    nama = StringField('Nama',validators=[DataRequired(), Length(min=3)], render_kw={'placeholder': 'Nama'})
    email = StringField('Email',validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email'})
    website = StringField('Website', render_kw={'placeholder': 'http://www.pythonesia.org'})
    comment = TextAreaField('Komentar', validators=[DataRequired()], render_kw={'placeholder': 'Tinggalkan komentar'})
    submit = SubmitField('Submit')

class FormHubungi(FlaskForm):
    nama = StringField('Nama',validators=[DataRequired(), Length(min=3)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    pesan = TextAreaField('Pesan', validators=[DataRequired()])
    submit = SubmitField('Submit')

class FormInstall(FlaskForm):
    title = StringField('Titel',validators=[DataRequired(), Length(min=2, max=100)], render_kw={'placeholder': 'Title'})
    deskripsi = StringField('Deskrispi',validators=[DataRequired(), Length(min=2, max=300)], render_kw={'placeholder': 'Deskripsi'})
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)], render_kw={'placeholder': 'Nama'})
    email = StringField('Email',validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'Password'})
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder': 'ConfirmPassword'})
    submit = SubmitField('Install')
    def validate_username(self, username):
        user = Pengguna.query.filter_by(nama=username.data).first()
        if user:
            raise ValidationError('Username sudah ada yang mendaftar. Silahkan pilih yang lain')

class FormAnggotatani(FlaskForm):
    nama = StringField('Nama Lengkap', validators=[DataRequired()])
    alamat = StringField('Alamat Lahan', validators=[DataRequired()])
    luas = StringField('Luas Tanah m2', validators=[DataRequired()])
    lati = StringField('Latitude', validators=[DataRequired()])
    longi = StringField('Longitude', validators=[DataRequired()])
    surel = StringField('Surel', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    gambar = FileField('Gambar Anggota', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Simpan')

class FormPupuk(FlaskForm):
    nama = StringField('Nama Pembuat', validators=[DataRequired()])
    alamat = StringField('Alamat Lengkap', validators=[DataRequired()])
    namapupuk = StringField('Nama Pupuk', validators=[DataRequired()])
    stok = IntegerField('Stok', validators=[DataRequired()])
    ket = StringField('Keterangan Pupuk', validators=[DataRequired()])
    gambar = FileField('Gambar Pupuk', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Simpan')

class FormPenanaman(FlaskForm):
    nama = StringField('Nama Lengkap', validators=[DataRequired()])
    luas = IntegerField('Luas Tanah m2', validators=[DataRequired()])
    varitas = StringField('Varitas / Tanaman', validators=[DataRequired()])
    lati = StringField('Latitude', validators=[DataRequired()])
    longi = StringField('Longitude', validators=[DataRequired()])
    gambar = FileField('Gambar Penanaman', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Simpan')

class FormPemeliharaan(FlaskForm):
    nama = StringField('Nama Lengkap', validators=[DataRequired()])
    pekerjaan = StringField('Pekerjaan Pemeliharaan', validators=[DataRequired()])
    luas = IntegerField('Luas Tanah m2', validators=[DataRequired()])
    lati = StringField('Latitude', validators=[DataRequired()])
    longi = StringField('Longitude', validators=[DataRequired()])
    gambar = FileField('Gambar Pemeliharaan', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Simpan')

class FormPanen(FlaskForm):
    nama = StringField('Nama Lengkap', validators=[DataRequired()])
    hasil = IntegerField('Hasil Panen KG', validators=[DataRequired()])
    luas = IntegerField('Luas Lahan', validators=[DataRequired()])
    submit = SubmitField('Simpan')

class FormGudang(FlaskForm):
    nama = StringField('Nama Lengkap', validators=[DataRequired()])
    beras = StringField('Varitas Beras', validators=[DataRequired()])
    jumlah = IntegerField('Jumlah', validators=[DataRequired()])
    submit = SubmitField('Simpan')

class FormAlat(FlaskForm):
    nama = StringField('Nama Alat', validators=[DataRequired()])
    alamat = StringField('Nama Lokasi', validators=[DataRequired()])
    lati = StringField('Latitude', validators=[DataRequired()])
    longi = StringField('Longitude', validators=[DataRequired()])
    gambar = FileField('Gambar Alat', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Simpan')