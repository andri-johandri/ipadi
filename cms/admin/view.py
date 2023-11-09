import os
import secrets
import codecs
from flask import render_template, url_for, flash, redirect, request, abort, send_from_directory, Blueprint, current_app,session
from flask_login import login_user
from flask_mail import Message
from flask_ckeditor import  upload_fail, upload_success
from slugify import slugify
from sqlalchemy import func
from cms import dbase, bcrypt, mail
from cms.database import Pengguna, Artikel, Komentar, Kategori, Tag, Halaman, Hubungi, Pengikut, Anggotatani, Mesin1, Mesin2, Mesin3, Mesin4, Pupuk, Pemeliharaan, Penanaman, Panen, Gudang, Namaalat, Kondisialato
from cms.form import FormArtikel, FormKategori, FormTag, FormHalaman, FormUpdateAkun, FormRegistrasi, FormLogin, FormPermintaanReset, FormResetPassword, FormMasuk, FormAnggotatani, FormPupuk, FormPenanaman, FormPemeliharaan, FormPanen, FormGudang, FormAlat, FormTambahadmin
from cms.admin.util import save_picture, save_picture_profile
from cms.main.util import send_reset_email, main_context

admin = Blueprint('admin', __name__, url_prefix='/administrator')

@admin.context_processor
def admin_konteks():
    penulisartikel = Pengguna.query.all()
    return dict(penulisartikel=penulisartikel, **main_context())

@admin.route("/")
def admin_index():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        halaman = request.args.get('halaman', 1, type=int)
        artikel = Artikel.query.filter_by(idpengguna=session['id']).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=5)
        a1 = Mesin1.query.order_by(Mesin1.tgl.desc()).limit(30).all()
        a2 = Mesin2.query.order_by(Mesin2.tgl.desc()).limit(30)
        a3 = Mesin3.query.order_by(Mesin3.tgl.desc()).limit(30)
        a4 = Mesin4.query.order_by(Mesin4.tgl.desc()).limit(30)
        return render_template('admin/home.html', posts=artikel,a1=a1,a2=a2,a3=a3,a4=a4)
    return redirect(url_for('admin.login'))

@admin.route("/dashalbarokah")
def admin_albarokah():
    if 'login' in session:
        if session['sebagai'] == 'admin':
            halaman = request.args.get('halaman', 1, type=int)
            artikel = Artikel.query.filter_by(idpengguna=session['id']).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=5)
            a1 = Mesin1.query.order_by(Mesin1.tgl.desc()).limit(10).all()
            a2 = Mesin2.query.order_by(Mesin2.tgl.desc()).limit(10).all()
            a3 = Mesin3.query.order_by(Mesin3.tgl.desc()).limit(10).all()
            a4 = Mesin4.query.order_by(Mesin4.tgl.desc()).limit(10).all()
            jmla = Anggotatani.query.count()
            jmlb = Anggotatani.query.with_entities(func.sum(Anggotatani.luas)).all()
            return render_template('admin/indexalbarokah.html', posts=artikel,a1=a1,a2=a2,a3=a3,a4=a4,jmla=jmla,jmlb=jmlb)
        elif session['sebagai'] == 'adminsela':
            halaman = request.args.get('halaman', 1, type=int)
            artikel = Artikel.query.filter_by(idpengguna=session['id']).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=5)
            a1 = Mesin1.query.order_by(Mesin1.tgl.desc()).limit(10).all()
            a2 = Mesin2.query.order_by(Mesin2.tgl.desc()).limit(10).all()
            a3 = Mesin3.query.order_by(Mesin3.tgl.desc()).limit(10).all()
            a4 = Mesin4.query.order_by(Mesin4.tgl.desc()).limit(10).all()
            jmla = Anggotatani.query.filter_by(sesi='4').count()
            jmlb = Anggotatani.query.with_entities(func.sum(Anggotatani.luas)).filter_by(sesi='4').all()
            return render_template('admin/indexsela.html', posts=artikel,a1=a1,a2=a2,a3=a3,a4=a4,jmla=jmla,jmlb=jmlb)
        else:
            return redirect(url_for('admin.logout'))
    return redirect(url_for('admin.albarokah'))

@admin.route("/isipos")
def isipos():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        halaman = request.args.get('halaman', 1, type=int)
        artikel = Artikel.query.filter_by(idpengguna=session['id']).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=5)
        return render_template('admin/home.html', posts=artikel)
        
    return redirect(url_for('admin.login'))
    
@admin.route("/kategori")
def admin_kategori():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        kategori = Kategori.query.all()
        return render_template('admin/kategori.html', kategori=kategori)
    return redirect(url_for('admin.login'))

@admin.route('/tambahkategori', methods=['GET','POST'])
def tambahkategori():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        form = FormKategori()
        if form.validate_on_submit():
            if request.form.get('gutters'):
                kategori = Kategori(nama=form.nama.data, slug=slugify(form.nama.data), idpengguna=session['id'], gutters=True)
            else:
                kategori = Kategori(nama=form.nama.data, slug=slugify(form.nama.data), idpengguna=session['id'])
            dbase.session.add(kategori)
            dbase.session.commit()
            flash('Kategori Berhasil ditambah!', 'is-success')
            return redirect(url_for('admin.admin_kategori'))
        return render_template('admin/tambah_kategori.html', form=form)
    return redirect(url_for('admin.login'))

@admin.route('/ubahkategori/<int:idkategori>', methods=['GET','POST'])
def ubahkategori(idkategori):
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        kategori = Kategori.query.get_or_404(idkategori)
        form = FormKategori()
        if form.validate_on_submit():
            kategori.nama = form.nama.data
            dbase.session.commit()
            flash("Kategori berhasil diupdated!", 'is-success')
            return redirect(url_for('admin.admin_kategori'))
        form.nama.data = kategori.nama
        return render_template('admin/tambah_kategori.html', form=form)
    return redirect(url_for('admin.login'))

@admin.route("/hapuskategori/<int:idkategori>")
def hapuskategori(idkategori):
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        kategori = Kategori.query.get_or_404(idkategori)
        dbase.session.delete(kategori)
        dbase.session.commit()
        flash('Kategori berhasil dihapus', 'is-success')
        return redirect(url_for('admin.admin_kategori'))
    return redirect(url_for('admin.login'))

@admin.route("/tag")
def tag():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        tags = Tag.query.all()
        return render_template('admin/tag.html', tags=tags)
    return redirect(url_for('admin.login'))

@admin.route('/tambahtag', methods=['GET','POST'])
def tambahtag():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        form = FormTag()
        if form.validate_on_submit():
            tag = Tag(nama=form.nama.data, slug=slugify(form.nama.data))
            dbase.session.add(tag)
            dbase.session.commit()
            flash('Tag Berhasil ditambah!', 'is-success')
            return redirect(url_for('admin.tag'))
        return render_template('admin/add_tag.html', form=form)
    return redirect(url_for('admin.login'))

@admin.route('/ubahtag/<int:idtag>', methods=['GET','POST'])
def ubahtag(idtag):
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        tag = Tag.query.get_or_404(idtag)
        form = FormTag()
        if form.validate_on_submit():
            tag.nama = form.nama.data
            dbase.session.commit()
            flash("Tag berhasil diupdated!", 'is-success')
            return redirect(url_for('admin.tag'))
        form.nama.data = tag.nama
        return render_template('admin/add_tag.html', form=form)
    return redirect(url_for('admin.login'))

@admin.route("/hapustag/<int:idtag>")
def hapustag(idtag):
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        tag = Tag.query.get_or_404(idtag)
        dbase.session.delete(tag)
        dbase.session.commit()
        flash('Tag berhasil dihapus', 'is-success')
        return redirect(url_for('admin.tag'))
    return redirect(url_for('admin.login'))

@admin.route("/artikel/baru", methods=['GET', 'POST'])
def artikelbaru():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        form = FormArtikel()
        form.kategori.choices = [(str(kategori.id), kategori.nama)for kategori in Kategori.query.all()]
        form.kategori.choices.insert(0,('', '== Pilih Kategori =='))
        topik = Tag.query.all()
        if form.validate_on_submit():
            ujung=str(".html")
            url_link = slugify(form.title.data)+ujung
            if form.thumbnail.data:
                picture_file = save_picture(form.thumbnail.data)
                artikel = Artikel(judul=form.title.data, isi=form.content.data, gambar=picture_file, slug=url_link, headline=form.is_headline.data, publish=form.publish.data,private=form.private.data, idpengguna=session['id'], idkategori=form.kategori.data)
            else:
                artikel = Artikel(judul=form.title.data, isi=form.content.data, slug=url_link,headline=form.is_headline.data, publish=form.publish.data,private=form.private.data, idpengguna=session['id'], idkategori=form.kategori.data)
            selected_tags = request.form.get('multiple_company')
            if selected_tags:
                my_tag = selected_tags.split(',')
                for checkbox in my_tag:
                    check = Tag.query.get(checkbox)
                    artikel.tags.append(check)
                dbase.session.add(artikel)
            dbase.session.commit()
            flash('Artikel Anda berhasil dibuat!', 'is-success is-light')
            return redirect(url_for('admin.admin_index'))
        return render_template('admin/create_post.html', title='Post Baru',form=form, legend='New Post', topik=topik)
    return redirect(url_for('admin.login'))

@admin.route('/uploads/<filename>')
def uploaded_files(filename):
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        path = current_app.config['UPLOADED_PATH']
        return send_from_directory(path, filename)
    return redirect(url_for('admin.login'))

@admin.route('/upload', methods=['POST'])
def upload():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        random_hex = secrets.token_hex(8)
        f = request.files.get('upload')
        extension = f.filename.split('.')[-1].lower()
        nama_gambar = f.filename.split('.')[0]
        nama_tersimpan = nama_gambar + '-' + random_hex + '.' + extension
        if extension not in ['jpg', 'gif', 'png', 'jpeg']:
            return upload_fail(message='Image only!')
        f.save(os.path.join(current_app.config['UPLOADED_PATH'], nama_tersimpan))
        url = url_for('admin.uploaded_files', filename=nama_tersimpan)
        return upload_success(url=url)
    return redirect(url_for('admin.login'))

@admin.route("/ubahartikel/<int:idartikel>", methods=['GET', 'POST'])
def ubahartikel(idartikel):
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        artikel = Artikel.query.get_or_404(idartikel)
        topik = Tag.query.all()
        form = FormArtikel(kategori=artikel.idkategori)
        form.kategori.choices = [(str(kategori.id), kategori.nama)for kategori in Kategori.query.all()]
        if form.validate_on_submit():
            if form.thumbnail.data:
                picture_file = save_picture(form.thumbnail.data)
                artikel.gambar = picture_file
            artikel.judul = form.title.data
            artikel.isi = form.content.data
            artikel.headline = form.is_headline.data
            artikel.idkategori = form.kategori.data
            hapus_tag = artikel.tags
            for hapus in hapus_tag:
                checkbox = Tag.query.get(hapus.id)
                artikel.tags.remove(checkbox)
            if form.multiple_company.data:
                selected_tags = request.form.get('multiple_company')
                my_tag = selected_tags.split(',')
                for checkbox in my_tag:
                    check = Tag.query.get(checkbox)
                    artikel.tags.append(check)
            dbase.session.commit()
            flash("Artikel berhasil diupdate", 'is-success')
            return redirect(url_for('admin.isipos'))
        elif request.method == 'GET':
            form.title.data = artikel.judul
            form.content.data = artikel.isi
            form.multiple_company.data = artikel.tags
            form.is_headline.data = artikel.headline
        return render_template('admin/create_post.html', title='Update Post',form=form, legend='Update Post', topik=topik, post=artikel)
    return redirect(url_for('admin.login'))

@admin.route("/hapusartikel/<int:idartikel>")
def hapusartikel(idartikel):
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        artikel = Artikel.query.get_or_404(idartikel)
        dbase.session.delete(artikel)
        dbase.session.commit()
        flash('Artikel berhasil dihapus', 'is-success')
        return redirect(url_for('admin.admin_index'))
    return redirect(url_for('admin.login'))

@admin.route("/kirimkepengikut/<int:idartikel>")
def kirimkepengikut(idartikel):
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        artikel = Artikel.query.get_or_404(idartikel)
        subscribers = Pengikut.query.all()
        msg = Message(artikel.title,sender='noreply@demo.com',recipients=[subscriber.email for subscriber in subscribers])
        msg.html = render_template('admin/mail.html', post=artikel, link=url_for('posts.artikel', berita=artikel.category.slug, idartikel=artikel.slug))
        mail.send(msg)
        flash('Artikel berhasil dikirim ke-email pelanggan', 'is-success')
        return redirect(url_for('admin.admin_index'))
    return redirect(url_for('admin.login'))

@admin.route("/ubahakun/<int:id>", methods=['GET', 'POST'])
def ubahakun(id):
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        user = Pengguna.query.get_or_404(id)
        form = FormUpdateAkun(sebagai=user.nama)
        form.role.choices = [(str(role.id), role.nama)for role in Sebagai.query.all()]
        form.role.choices.insert(0,('', '== Pilih Role =='))
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture_profile(form.picture.data)
                user.image_file = picture_file
            user.nama = form.username.data
            user.sebagai = form.role.data
            user.biodata = form.biografi.data
            user.aktifasi = form.active.data
            dbase.session.commit()
            flash('Akun Anda berhasil diupdate!', 'is-success')
            return redirect(url_for('admin.pengguna'))
        form.username.data = user.nama
        form.email.data = user.surel
        form.role.data = user.sebagai
        form.active.data = user.aktifasi
        form.biografi.data = user.biodata
        return render_template('admin/account.html', user=user, title='Account', form=form)
    return redirect(url_for('admin.login'))

# Pages
@admin.route("/halaman/baru", methods=['GET', 'POST'])
def halamanbaru():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        form = FormHalaman()
        if form.validate_on_submit():
            halaman = Halaman(judul=form.title.data, isi=form.content.data, slug=slugify(form.title.data), idpengguna=session['id'])
            dbase.session.add(halaman)
            dbase.session.commit()
            flash('Halaman berhasil dibuat!', 'is-success')
            return redirect(url_for('admin.halaman'))
        return render_template('admin/create_page.html', title='Halaman Baru',form=form, legend='Halaman Baru')
    return redirect(url_for('admin.login'))

@admin.route("/halaman")
def halaman():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        page = request.args.get('halaman', 1, type=int)
        halaman = Halaman.query.order_by(Halaman.tanggaldibuat.desc()).paginate(page=page, per_page=5)
        return render_template('admin/pages.html', pages=halaman)
    return redirect(url_for('admin.login'))


@admin.route("/ubahhalaman/<int:idhalaman>", methods=['GET', 'POST'])
def ubahhalaman(idhalaman):
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        halaman = Halaman.query.get_or_404(idhalaman)
        form = FormHalaman()
        if form.validate_on_submit():
            halaman.judul = form.title.data
            halaman.isi = form.content.data
            halaman.publish = form.is_active.data
            dbase.session.commit()
            flash('Halaman berhasil diupdate!', 'is-success')
            return redirect(url_for('admin.halaman'))
        elif request.method == 'GET':
            form.title.data = halaman.judul
            form.content.data = halaman.isi
            form.is_active.data = halaman.publish
        return render_template('admin/create_page.html', title='Update Page',form=form, legend='Update Page')
    return redirect(url_for('admin.login'))

@admin.route("/hapushalaman/<int:idhalaman>")
def hapushalaman(idhalaman):
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        page = Halaman.query.get_or_404(idhalaman)
        dbase.session.delete(page)
        dbase.session.commit()
        flash('Halaman berhasil dihapus', 'is-success is-light')
        return redirect(url_for('admin.halaman'))
    return redirect(url_for('admin.login'))

@admin.route("/pengguna")
def pengguna():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        users = Pengguna.query.all()
        return render_template('admin/users.html', users=users)
    return redirect(url_for('admin.login'))

@admin.route("/penggunaadmin")
def penggunaadmin():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        users = Pengguna.query.all()
        return render_template('admin/useradmin.html', users=users)
    return redirect(url_for('admin.login'))

@admin.route("/pesan")
def pesan():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        users = Hubungi.query.all()
        return render_template('admin/pesan.html', users=users)
    return redirect(url_for('admin.login'))

@admin.route("/tema", methods=['GET','POST'])
def tema():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        if request.method == 'POST':
            isimain=request.form['mainhtml']
            ambil = isimain.replace('\n', '')
            isinya=os.path.join(current_app.config['DIREKTORI'], 'templates/main/')
            wz = open(isinya+"main.html", "w")
            wz = open(isinya+"main.html", "a")
            wz.write(ambil)
            wz.close()
            return redirect(url_for('admin.tema'))
        filenya=os.path.join(current_app.config['DIREKTORI'], 'templates/main/')
        fin = codecs.open(filenya+'main.html', 'r')
        isi=fin.read()
        return render_template('admin/tema.html', isi=isi)
    return redirect(url_for('admin.login'))

@admin.route("/landing", methods=['GET','POST'])
def landing():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        if request.method == 'POST':
            isimain=request.form['mainhtml']
            ambil = isimain.replace('\n', '')
            isinya=os.path.join(current_app.config['DIREKTORI'], 'templates/main/')
            wz = open(isinya+"landing.html", "w")
            wz = open(isinya+"landing.html", "a")
            wz.write(ambil)
            wz.close()
            return redirect(url_for('admin.landing'))
        filenya=os.path.join(current_app.config['DIREKTORI'], 'templates/main/')
        fin = codecs.open(filenya+'landing.html', 'r')
        isi=fin.read()
        return render_template('admin/landing.html', isi=isi)
    return redirect(url_for('admin.login'))

@admin.route("/beranda", methods=['GET','POST'])
def beranda():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        if request.method == 'POST':
            isimain=request.form['mainhtml']
            ambil = isimain.replace('\n', '')
            isinya=os.path.join(current_app.config['DIREKTORI'], 'templates/main/')
            wz = open(isinya+"home.html", "w")
            wz = open(isinya+"home.html", "a")
            wz.write(ambil)
            wz.close()
            return redirect(url_for('admin.beranda'))
        filenya=os.path.join(current_app.config['DIREKTORI'], 'templates/main/')
        fin = codecs.open(filenya+'home.html', 'r')
        isi=fin.read()
        return render_template('admin/beranda.html', isi=isi)
    return redirect(url_for('admin.login'))

@admin.route("/isihalaman", methods=['GET','POST'])
def isihalaman():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        if request.method == 'POST':
            isimain=request.form['mainhtml']
            ambil = isimain.replace('\n', '')
            isinya=os.path.join(current_app.config['DIREKTORI'], 'templates/main/')
            wz = open(isinya+"halaman.html", "w")
            wz = open(isinya+"halaman.html", "a")
            wz.write(ambil)
            wz.close()
            return redirect(url_for('admin.halaman'))
        filenya=os.path.join(current_app.config['DIREKTORI'], 'templates/main/')
        fin = codecs.open(filenya+'halaman.html', 'r')
        isi=fin.read()
        return render_template('admin/halaman.html', isi=isi)
    return redirect(url_for('admin.login'))

@admin.route("/kelompok", methods=['GET','POST'])
def kelompok():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        if request.method == 'POST':
            isimain=request.form['mainhtml']
            ambil = isimain.replace('\n', '')
            isinya=os.path.join(current_app.config['DIREKTORI'], 'templates/main/')
            wz = open(isinya+"category.html", "w")
            wz = open(isinya+"category.html", "a")
            wz.write(ambil)
            wz.close()
            return redirect(url_for('admin.kelompok'))
        filenya=os.path.join(current_app.config['DIREKTORI'], 'templates/main/')
        fin = codecs.open(filenya+'category.html', 'r')
        isi=fin.read()
        return render_template('admin/category.html', isi=isi)
    return redirect(url_for('admin.login'))

@admin.route("/detil", methods=['GET','POST'])
def detil():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        if request.method == 'POST':
            isimain=request.form['mainhtml']
            ambil = isimain.replace('\n', '')
            isinya=os.path.join(current_app.config['DIREKTORI'], 'templates/main/')
            wz = open(isinya+"detail.html", "w")
            wz = open(isinya+"detail.html", "a")
            wz.write(ambil)
            wz.close()
            return redirect(url_for('admin.detil'))
        filenya=os.path.join(current_app.config['DIREKTORI'], 'templates/main/')
        fin = codecs.open(filenya+'detail.html', 'r')
        isi=fin.read()
        return render_template('admin/detil.html', isi=isi)
    return redirect(url_for('admin.login'))

@admin.route("/artikel", methods=['GET','POST'])
def artikel():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        if request.method == 'POST':
            isimain=request.form['mainhtml']
            ambil = isimain.replace('\n', '')
            isinya=os.path.join(current_app.config['DIREKTORI'], 'templates/main/')
            wz = open(isinya+"post.html", "w")
            wz = open(isinya+"post.html", "a")
            wz.write(ambil)
            wz.close()
            return redirect(url_for('admin.artikel'))
        filenya=os.path.join(current_app.config['DIREKTORI'], 'templates/main/')
        fin = codecs.open(filenya+'post.html', 'r')
        isi=fin.read()
        return render_template('admin/artikel.html', isi=isi)
    return redirect(url_for('admin.login'))

@admin.route("/kirim", methods=['GET','POST'])
def kirim():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        if request.method == 'POST':
            isimain=request.form['mainhtml']
            ambil = isimain.replace('\n', '')
            isinya=os.path.join(current_app.config['DIREKTORI'], 'templates/main/')
            wz = open(isinya+"subscribe.html", "w")
            wz = open(isinya+"subscribe.html", "a")
            wz.write(ambil)
            wz.close()
            return redirect(url_for('admin.kirim'))
        filenya=os.path.join(current_app.config['DIREKTORI'], 'templates/main/')
        fin = codecs.open(filenya+'subscribe.html', 'r')
        isi=fin.read()
        return render_template('admin/kirim.html', isi=isi)
    return redirect(url_for('admin.login'))

@admin.route("/costumcss", methods=['GET','POST'])
def costumcss():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        if request.method == 'POST':
            isimain=request.form['mainhtml']
            ambil = isimain.replace('\n', '')
            isinya=os.path.join(current_app.config['DIREKTORI'], 'static/css/')
            wz = open(isinya+"costum.css", "w")
            wz = open(isinya+"costum.css", "a")
            wz.write(ambil)
            wz.close()
            return redirect(url_for('admin.costumcss'))
        filenya=os.path.join(current_app.config['DIREKTORI'], 'static/css/')
        fin = codecs.open(filenya+'costum.css', 'r')
        isi=fin.read()
        return render_template('admin/costum.html', isi=isi)
    return redirect(url_for('admin.login'))

@admin.route("/komentar")
def komentar():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        halaman = request.args.get('halaman', 1, type=int)
        isikomentar = Komentar.query.order_by(Komentar.publish==False, Komentar.tanggalkomen.desc()).paginate(page=halaman, per_page=10)
        return render_template('admin/comments.html', comments=isikomentar)
    return redirect(url_for('admin.login'))

@admin.route("/unpubkomentar/<int:id>")

def unpubkomentar(id):
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        comment = Komentar.query.get_or_404(id)
        if comment.publish:
            comment.publish = False
        else:
            comment.publish = True
        dbase.session.commit()
        flash('Komentar berhasil diupdate', 'is-success')
        return redirect(url_for('admin.komentar'))
    return redirect(url_for('admin.login'))
    

@admin.route("/hapuskomentar/<int:id>")
def hapuskomentar(id):
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        comment = Komentar.query.get_or_404(id)
        dbase.session.delete(comment)
        dbase.session.commit()
        flash('Komentar berhasil dihapus', 'is-success')
        return redirect(url_for('admin.komentar'))
    return redirect(url_for('admin.login'))

@admin.route("/pengikut")
def daftarpengikut():
    if 'login' in session:
        if session['sebagai'] != 'admin':
            return redirect(url_for('admin.logout'))
        pengikut = Pengikut.query.order_by(Pengikut.tanggaldibuat.desc()).all()
        return render_template('admin/pengikut.html', subscribers=pengikut)
    return redirect(url_for('admin.login'))

@admin.route("/signup", methods=['GET', 'POST'])
def register():
    if 'login' in session:
        if session['sebagai'] == 'admin':
            return redirect(url_for('admin.admin_index'))    
    form = FormRegistrasi()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Pengguna(nama=form.username.data, surel=form.email.data, kunci=hashed_password,sebagai=3,aktifasi=1)
        dbase.session.add(user)
        dbase.session.commit()
        flash('Akun berhasil dibuat! Silahkan Login', 'is-success')
        return redirect(url_for('admin.login'))
    return render_template('admin/register.html', title='Signup', form=form)
    #return redirect(url_for('admin.login'))

@admin.route("/signin", methods=['GET', 'POST'])
def login():
    if 'login' in session:
        if session['sebagai'] == 'admin':
            return redirect(url_for('admin.admin_index')) 
    form = FormLogin()
    if form.validate_on_submit():       
        pengguna = Pengguna.query.filter_by(surel=form.email.data).first()
        if pengguna and bcrypt.check_password_hash(pengguna.kunci, form.password.data):
            login_user(pengguna, remember=form.remember.data)
            session['login']=pengguna.surel
            session['sebagai']=pengguna.sebagai
            session['id']=pengguna.id
            session['gambar']=pengguna.gambar         
            return redirect(url_for('admin.admin_albarokah'))
        else:
            flash('Login Gagal. Cek email dan password Anda', 'is-danger')
    return render_template('admin/login.html', title='Signin', form=form)


@admin.route("/adminutama", methods=['GET', 'POST'])
def adminutama():
    if 'login' in session:
        if session['sebagai'] == 'admin':
            return redirect(url_for('admin.admin_index')) 
    form = FormLogin()
    if form.validate_on_submit():       
        pengguna = Pengguna.query.filter_by(surel=form.email.data).first()
        if pengguna and bcrypt.check_password_hash(pengguna.kunci, form.password.data):
            login_user(pengguna, remember=form.remember.data)
            session['login']=pengguna.surel
            session['sebagai']=pengguna.sebagai
            session['id']=pengguna.id
            session['gambar']=pengguna.gambar         
            return redirect(url_for('admin.admin_index'))
        else:
            flash('Login Gagal. Cek email dan password Anda', 'is-danger')
    return render_template('admin/login.html', title='Signin', form=form)

@admin.route("/tambahadmin", methods=['GET', 'POST'])
def tambahadmin():
    if 'login' in session:
        if session['sebagai'] == 'admin':    
            form = FormTambahadmin()
            if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = Pengguna(nama=form.username.data, surel=form.email.data, kunci=hashed_password,sebagai=form.sebagai.data,aktifasi=1)
                dbase.session.add(user)
                dbase.session.commit()
                flash('Akun berhasil dibuat! Silahkan Login', 'is-success')
                return redirect(url_for('admin.adminutama'))
            return render_template('admin/tambahadmin.html', title='Signup', form=form)



@admin.route("/albarokah", methods=['GET', 'POST'])
def albarokah():
    if 'login' in session:
        if session['sebagai'] == 'admin':
            return redirect(url_for('admin.admin_index')) 
    form = FormLogin()
    if form.validate_on_submit():       
        pengguna = Pengguna.query.filter_by(surel=form.email.data).first()
        if pengguna and bcrypt.check_password_hash(pengguna.kunci, form.password.data):
            login_user(pengguna, remember=form.remember.data)
            session['login']=pengguna.surel
            session['sebagai']=pengguna.sebagai
            session['id']=pengguna.id
            session['gambar']=pengguna.gambar         
            return redirect(url_for('admin.admin_albarokah'))
        else:
            flash('Login Gagal. Cek email dan password Anda', 'is-danger')
    return render_template('admin/albarokah.html', title='Albarokah Signin', form=form)

@admin.route("/masuk", methods=['GET', 'POST'])
def masuk():
    if 'masuk' in session:
        if session['sebagai'] == 'admin':
            return redirect(url_for('admin.dash_index')) 
    form = FormMasuk()
    if form.validate_on_submit():       
        pengguna = Pengguna.query.filter_by(surel=form.email.data).first()
        if pengguna and bcrypt.check_password_hash(pengguna.kunci, form.password.data):
            login_user(pengguna, remember=form.remember.data)
            session['masuk']=pengguna.surel
            session['sebagai']=pengguna.sebagai
            session['id']=pengguna.id
            session['gambar']=pengguna.gambar         
            return redirect(url_for('admin.admin_index'))
        else:
            flash('Login Gagal. Cek email dan password Anda', 'is-danger')
    return render_template('main/masuk.html', title='Signin', form=form)

@admin.route("/logout")
def logout():
    session.pop('login', None)
    session.pop('sebagai', None)
    session.pop('gambar', None)
    return redirect(url_for('main.home'))

@admin.route("/permintaanreset", methods=['GET', 'POST'])
def permintaanreset():
    if 'login' in session:
        if session['sebagai'] == 'admin':
            return redirect(url_for('admin.admin_index')) 
    form = FormPermintaanReset()
    if form.validate_on_submit():
        user = Pengguna.query.filter_by(surel=form.email.data).first()
        send_reset_email(user)
        flash('Kami telah mengirimkan email intruksi untuk mengganti password. Silahkan cek email Anda', 'is-info')
        return redirect(url_for('admin.login'))
    return render_template('admin/reset_request.html', title='Reset Password', form=form)

@admin.route("/resetpassword/<token>", methods=['GET', 'POST'])
def passwordreset(token):
    if 'login' in session:
        if session['sebagai'] == 'admin':
            return redirect(url_for('admin.admin_index')) 
    pengguna = Pengguna.verify_reset_token(token)
    if pengguna is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('admin.reset_request'))
    form = FormResetPassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        pengguna.kunci = hashed_password
        dbase.session.commit()
        flash('Password Anda telah diupdate! silahkan login', 'is-success')
        return redirect(url_for('admin.login'))
    return render_template('admin/reset_token.html', title='Reset Password', form=form)

@admin.route("/updatedb")
def updatedb():
    if 'login' in session:
        if session['sebagai'] == 'admin':
            dbase.create_all()
            return redirect(url_for('admin.admin_index'))
    return redirect(url_for('admin.login')) 

@admin.route("/anggotatani")
def anggotatani():
    if 'sebagai' in session:
        if session['sebagai']=='admin':
            kategori = Anggotatani.query.all()
            return render_template('admin/anggotatani.html', kategori=kategori)
        elif session['sebagai']=='adminsela':
            kategori = Anggotatani.query.filter_by(sesi='4').all()
            return render_template('admin/anggotatani.html', kategori=kategori)
        return redirect(url_for('admin.logout'))
    return redirect(url_for('admin.logout'))

@admin.route('/tambahanggotatani', methods=['GET','POST'])
def tambahanggotatani():
    if 'sebagai' in session:
        if session['sebagai']=='admin':
            form = FormAnggotatani()
            if form.validate_on_submit():
                if form.gambar.data:
                    picture_file = save_picture(form.gambar.data)
                    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                    kategori = Anggotatani(nama=form.nama.data,alamat=form.alamat.data,luas=form.luas.data,lati=form.lati.data,longi=form.longi.data,gambar=picture_file, sesi=session['id'])
                    user = Pengguna(nama=form.nama.data, surel=form.surel.data, kunci=hashed_password,sebagai='anggota',aktifasi=1)
                else:
                    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                    kategori = Anggotatani(nama=form.nama.data,alamat=form.alamat.data,luas=form.luas.data,lati=form.lati.data,longi=form.longi.data,gambar='default.png', sesi=session['id'])
                    user = Pengguna(nama=form.nama.data, surel=form.surel.data, kunci=hashed_password,sebagai='anggota',aktifasi=1)
                dbase.session.add(kategori)
                dbase.session.add(user)
                dbase.session.commit()
                flash('Tambah Anggota Berhasil ditambah!', 'is-success')
                return redirect(url_for('admin.anggotatani'))
            return render_template('admin/tambah_anggotatani.html', form=form)
        elif session['sebagai']=='adminsela':
            form = FormAnggotatani()
            if form.validate_on_submit():
                if form.gambar.data:
                    picture_file = save_picture(form.gambar.data)
                    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                    kategori = Anggotatani(nama=form.nama.data,alamat=form.alamat.data,luas=form.luas.data,lati=form.lati.data,longi=form.longi.data,gambar=picture_file, sesi='4')
                    user = Pengguna(nama=form.nama.data, surel=form.surel.data, kunci=hashed_password,sebagai='anggota',aktifasi=1)
                else:
                    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                    kategori = Anggotatani(nama=form.nama.data,alamat=form.alamat.data,luas=form.luas.data,lati=form.lati.data,longi=form.longi.data,gambar='default.png', sesi='4')
                    user = Pengguna(nama=form.nama.data, surel=form.surel.data, kunci=hashed_password,sebagai='anggota',aktifasi=1)
                dbase.session.add(kategori)
                dbase.session.add(user)
                dbase.session.commit()
                flash('Tambah Anggota Berhasil ditambah!', 'is-success')
                return redirect(url_for('admin.anggotatani'))
            return render_template('admin/tambah_anggotatani.html', form=form)
        return redirect(url_for('admin.logout'))
    return redirect(url_for('admin.logout'))

@admin.route("/pupuk")
def pupuk():
    if 'sebagai' in session:
        if session['sebagai']=='admin':
            kategori = Pupuk.query.all()
            return render_template('admin/pupuk.html', kategori=kategori)
        elif session['sebagai']=='adminsela':
            kategori = Pupuk.query.all()
            return render_template('admin/pupuk.html', kategori=kategori)
        return redirect(url_for('admin.logout'))
    return redirect(url_for('admin.logout'))

@admin.route('/tambahpupuk', methods=['GET','POST'])
def tambahpupuk():
    if 'sebagai' in session:
        if session['sebagai']=='admin':
            form = FormPupuk()
            if form.validate_on_submit():
                if form.gambar.data:
                    picture_file = save_picture(form.gambar.data)
                    kategori = Pupuk(nama=form.nama.data,alamat=form.alamat.data,namapupuk=form.namapupuk.data,stok=form.stok.data,longi=form.ket.data,gambar=picture_file, sesi=session['id'])
                else:
                    kategori = Pupuk(nama=form.nama.data,alamat=form.alamat.data,namapupuk=form.namapupuk.data,stok=form.stok.data,longi=form.ket.data,gambar='default.png', sesi=session['id'])
                dbase.session.add(kategori)
                dbase.session.commit()
                flash('Data Pupuk Berhasil ditambah!', 'is-success')
                return redirect(url_for('admin.pupuk'))
            return render_template('admin/tambah_pupuk.html', form=form)
        elif session['sebagai']=='adminsela':
            form = FormPupuk()
            if form.validate_on_submit():
                if form.gambar.data:
                    picture_file = save_picture(form.gambar.data)
                    kategori = Pupuk(nama=form.nama.data,alamat=form.alamat.data,namapupuk=form.namapupuk.data,stok=form.stok.data,longi=form.ket.data,gambar=picture_file, sesi='4')
                else:
                    kategori = Pupuk(nama=form.nama.data,alamat=form.alamat.data,namapupuk=form.namapupuk.data,stok=form.stok.data,longi=form.ket.data,gambar='default.png', sesi='4')
                dbase.session.add(kategori)
                dbase.session.commit()
                flash('Data Pupuk Berhasil ditambah!', 'is-success')
                return redirect(url_for('admin.pupuk'))
            return render_template('admin/tambah_pupuk.html', form=form)
        return redirect(url_for('admin.logout'))
    return redirect(url_for('admin.logout'))


@admin.route("/pemeliharaan")
def pemeliharaan():
    if 'sebagai' in session:
        if session['sebagai']=='admin':
            kategori = Pemeliharaan.query.all()
            return render_template('admin/pemeliharaan.html', kategori=kategori)
        if session['sebagai']=='adminsela':
            kategori = Pemeliharaan.query.all()
            return render_template('admin/pemeliharaan.html', kategori=kategori)
        return redirect(url_for('admin.logout'))
    return redirect(url_for('admin.logout'))

@admin.route('/tambahpemeliharaan', methods=['GET','POST'])
def tambahpemeliharaan():
    if 'sebagai' in session:
        if session['sebagai']=='admin':
            form = FormPemeliharaan()
            if form.validate_on_submit():
                if form.gambar.data:
                    picture_file = save_picture(form.gambar.data)
                    kategori = Pemeliharaan(nama=form.nama.data,pekerjaan=form.pekerjaan.data,luas=form.luas.data,lati=form.lati.data,longi=form.longi.data,gambar=picture_file, sesi=session['id'])
                else:
                    kategori = Pemeliharaan(nama=form.nama.data,pekerjaan=form.pekerjaan.data,luas=form.luas.data,lati=form.lati.data,longi=form.longi.data,gambar='default.png', sesi=session['id'])
                dbase.session.add(kategori)
                dbase.session.commit()
                flash('Data Pemeliharaan Berhasil ditambah!', 'is-success')
                return redirect(url_for('admin.pemeliharaan'))
            return render_template('admin/tambah_pemeliharaan.html', form=form)
        if session['sebagai']=='adminsela':
            form = FormPemeliharaan()
            if form.validate_on_submit():
                if form.gambar.data:
                    picture_file = save_picture(form.gambar.data)
                    kategori = Pemeliharaan(nama=form.nama.data,pekerjaan=form.pekerjaan.data,luas=form.luas.data,lati=form.lati.data,longi=form.longi.data,gambar=picture_file, sesi='4')
                else:
                    kategori = Pemeliharaan(nama=form.nama.data,pekerjaan=form.pekerjaan.data,luas=form.luas.data,lati=form.lati.data,longi=form.longi.data,gambar='default.png', sesi='4')
                dbase.session.add(kategori)
                dbase.session.commit()
                flash('Data Pemeliharaan Berhasil ditambah!', 'is-success')
                return redirect(url_for('admin.pemeliharaan'))
            return render_template('admin/tambah_pemeliharaan.html', form=form)
        return redirect(url_for('admin.logout'))
    return redirect(url_for('admin.logout'))

@admin.route("/penanaman")
def penanaman():
    if 'sebagai' in session:
        if session['sebagai']=='admin':
            kategori = Penanaman.query.all()
            return render_template('admin/penanaman.html', kategori=kategori)
        return redirect(url_for('admin.logout'))
    return redirect(url_for('admin.logout'))

@admin.route('/tambahpenanaman', methods=['GET','POST'])
def tambahpenanaman():
    if 'sebagai' in session:
        if session['sebagai']=='admin':
            form = FormPenanaman()
            if form.validate_on_submit():
                if form.gambar.data:
                    picture_file = save_picture(form.gambar.data)
                    kategori = Penanaman(nama=form.nama.data,luas=form.luas.data,varitas=form.varitas.data,lati=form.lati.data,longi=form.longi.data,gambar=picture_file, sesi=session['id'])
                else:
                    kategori = Penanaman(nama=form.nama.data,luas=form.luas.data,varitas=form.varitas.data,lati=form.lati.data,longi=form.longi.data,gambar='default.png', sesi=session['id'])
                dbase.session.add(kategori)
                dbase.session.commit()
                flash('Data Penanaman Berhasil ditambah!', 'is-success')
                return redirect(url_for('admin.penanaman'))
            return render_template('admin/tambah_penanaman.html', form=form)
        return redirect(url_for('admin.logout'))
    return redirect(url_for('admin.logout'))

@admin.route("/panen")
def panen():
    if 'sebagai' in session:
        if session['sebagai']=='admin':
            kategori = Panen.query.all()
            return render_template('admin/panen.html', kategori=kategori)
        return redirect(url_for('admin.logout'))
    return redirect(url_for('admin.logout'))

@admin.route('/tambahpanen', methods=['GET','POST'])
def tambahpanen():
    if 'sebagai' in session:
        if session['sebagai']=='admin':
            form = FormPanen()
            if form.validate_on_submit():
                kategori = Panen(nama=form.nama.data,hasilpanen=form.hasil.data,luas=form.luas.data,sesi=session['id'])
                dbase.session.add(kategori)
                dbase.session.commit()
                flash('Data Panen Berhasil ditambah!', 'is-success')
                return redirect(url_for('admin.panen'))
            return render_template('admin/tambah_panen.html', form=form)
        return redirect(url_for('admin.logout'))
    return redirect(url_for('admin.logout'))

@admin.route("/gudang")
def gudang():
    if 'sebagai' in session:
        if session['sebagai']=='admin':
            kategori = Gudang.query.all()
            return render_template('admin/gudang.html', kategori=kategori)
        return redirect(url_for('admin.logout'))
    return redirect(url_for('admin.logout'))

@admin.route('/tambahgudang', methods=['GET','POST'])
def tambahgudang():
    if 'sebagai' in session:
        if session['sebagai']=='admin':
            form = FormGudang()
            if form.validate_on_submit():
                kategori = Gudang(nama=form.nama.data,beras=form.beras.data,jumlah=form.jumlah.data, sesi=session['id'])
                dbase.session.add(kategori)
                dbase.session.commit()
                flash('Laporan Kegiatan Berhasil ditambah!', 'is-success')
                return redirect(url_for('admin.gudang'))
            return render_template('admin/tambah_gudang.html', form=form)
        return redirect(url_for('admin.logout'))
    return redirect(url_for('admin.logout'))

@admin.route("/alat")
def alat():
    if 'sebagai' in session:
        if session['sebagai']=='admin':
            kategori = Namaalat.query.all()
            return render_template('admin/alat.html', kategori=kategori)
        return redirect(url_for('admin.logout'))
    return redirect(url_for('admin.logout'))

@admin.route('/tambahalat', methods=['GET','POST'])
def tambahalat():
    if 'sebagai' in session:
        if session['sebagai']=='admin':
            form = FormAlat()
            if form.validate_on_submit():
                if form.gambar.data:
                    picture_file = save_picture(form.gambar.data)
                    kategori = Namaalat(nama=form.nama.data,alamat=form.alamat.data,lati=form.lati.data,longi=form.longi.data,gambar=picture_file, sesi=session['id'])
                else:
                    kategori = Namaalat(nama=form.nama.data,alamat=form.alamat.data,lati=form.lati.data,longi=form.longi.data,gambar='default.png', sesi=session['id'])
                dbase.session.add(kategori)
                dbase.session.commit()
                flash('Tambah Alat Berhasil ditambah!', 'is-success')
                return redirect(url_for('admin.alat'))
            return render_template('admin/tambah_alat.html', form=form)
        return redirect(url_for('admin.logout'))
    return redirect(url_for('admin.logout'))

@admin.route("/data")
def data():
    if 'login' in session:
        if session['sebagai'] == 'admin':
            halaman = request.args.get('halaman', 1, type=int)
            artikel = Artikel.query.filter_by(idpengguna=session['id']).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=5)
            a1 = Mesin1.query.order_by(Mesin1.tgl.desc()).limit(10).all()
            a2 = Mesin2.query.order_by(Mesin2.tgl.desc()).limit(10).all()
            a3 = Mesin3.query.order_by(Mesin3.tgl.desc()).limit(10).all()
            a4 = Mesin4.query.order_by(Mesin4.tgl.desc()).limit(10).all()
            return render_template('admin/data.html', posts=artikel,a1=a1,a2=a2,a3=a3,a4=a4)
        elif session['sebagai'] == 'adminsela':
            halaman = request.args.get('halaman', 1, type=int)
            artikel = Artikel.query.filter_by(idpengguna=session['id']).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=5)
            a4 = Mesin4.query.order_by(Mesin4.tgl.desc()).limit(10).all()
            return render_template('admin/datasela.html', posts=artikel,a4=a4)
        return redirect(url_for('admin.logout'))
    return redirect(url_for('admin.albarokah'))

@admin.route("/kondisi")
def kondisi():
    if 'sebagai' in session:
        if session['sebagai']=='admin':
            kategori = Anggotatani.query.all()
            return render_template('admin/kondisi.html', kategori=kategori)
        return redirect(url_for('admin.logout'))
    return redirect(url_for('admin.logout'))