from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app,send_from_directory,make_response
from flask_login import current_user
from pathlib import Path
from cms import dbase, bcrypt
from cms.form import FormHubungi, FormPengikut, FormKomentar, FormInstall
from cms.database import Pengguna, Artikel, Komentar, Kategori, Tag, Halaman, Hubungi, Pengikut, Judul, Mesin1, Mesin2, Mesin3, Mesin4
from cms.main.util import main_context
import random
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

def generate_random_value(min_val, max_val):
    return round(random.uniform(min_val, max_val), 2)

def generate_time_series(start_date, end_date):
    current_time = start_date
    time_series = []

    while current_time <= end_date:
        if current_time.hour >= 5 and current_time.hour < 9:
            value = generate_random_value(20.0, 25.0)
        elif current_time.hour >= 9 and current_time.hour < 13:
            value = generate_random_value(25.1, 37.1)
        elif current_time.hour >= 13 and current_time.hour < 18:
            value = generate_random_value(37.1, 25.0)
        elif current_time.hour >= 18 and current_time.hour < 20:
            value = generate_random_value(25.0, 22.0)
        elif current_time.hour >= 20 or current_time.hour < 3:
            value = generate_random_value(22.0, 19.0)
        else:
            value = generate_random_value(19.0, 20.0)

        time_series.append((current_time, value))
        current_time += timedelta(minutes=5)

    return time_series

@main.app_errorhandler(404)
def page_not_found(e):
    return redirect(url_for('main.home'))


@main.app_errorhandler(403)
def page_deny(e):
    return redirect(url_for('main.home'))

@main.context_processor
def waktu():
    return main_context()

#proses awal install
@main.route("/install", methods=['GET', 'POST'])
def install():
    dbase.create_all()
    Judul.tambahjudul()
    isi=current_app.config['DIREKTORI']
    form = FormInstall()
    if Path(isi+'/install.txt').is_file():
        return redirect(url_for('main.home'))
    else:
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            emailnya = form.email.data
            titlenya = form.title.data
            wi = open(isi+"/install.txt", "w")
            wi = open(isi+"/install.txt", "a")
            wi.write("Email admin : '"+emailnya+"'\nTitle web :'"+titlenya+"'\n Create Installasi")
            wi.close()
            pengguna = Pengguna(nama=form.username.data, surel=form.email.data, kunci=hashed_password,sebagai='admin',aktifasi=1)
            dbase.session.add(pengguna)
            dbase.session.commit()
            judul = Judul.query.get_or_404(1)
            judul.judul = form.title.data
            judul.deskripsi = form.deskripsi.data
            dbase.session.commit()
            flash('Install Aplikasi berhasil dibuat! Silahkan Login', 'is-success')
            return redirect(url_for('admin.login'))
        return render_template('main/install.html',title='Install', form=form)

#halaman depan
@main.route("/")
def home():
    isi=current_app.config['DIREKTORI']
    if Path(isi+'/install.txt').is_file():
        halaman = request.args.get('halaman', 1, type=int)
        headline = Artikel.query.filter_by(headline = True).order_by(Artikel.tanggaldibuat.desc()).first()
        posts = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        tulisan = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        a1 = Mesin1.query.order_by(Mesin1.no.desc()).limit(30).all()
        #a2 = Mesin2.query.order_by(Mesin2.tgl.desc()).limit(30)
        #a3 = Mesin3.query.order_by(Mesin3.tgl.desc()).limit(30)
        #a4 = Mesin4.query.order_by(Mesin4.tgl.desc()).limit(30)
        return render_template('main/landing.html', posts=posts, headline=headline,tulisan=tulisan,title="Beranda",a1=a1)
    else:
        return redirect(url_for('main.install'))

@main.route("/sela1")
def sela1():
    isi=current_app.config['DIREKTORI']
    if Path(isi+'/install.txt').is_file():
        halaman = request.args.get('halaman', 1, type=int)
        headline = Artikel.query.filter_by(headline = True).order_by(Artikel.tanggaldibuat.desc()).first()
        posts = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        tulisan = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        a1 = Mesin4.query.order_by(Mesin4.no.desc()).limit(30).all()
        #a2 = Mesin2.query.order_by(Mesin2.tgl.desc()).limit(30)
        #a3 = Mesin3.query.order_by(Mesin3.tgl.desc()).limit(30)
        #a4 = Mesin4.query.order_by(Mesin4.tgl.desc()).limit(30)
        return render_template('main/sela1.html', posts=posts, headline=headline,tulisan=tulisan,title="Beranda",a1=a1)
    else:
        return redirect(url_for('main.install'))

@main.route("/jayapura2")
def jayapura2():
    isi=current_app.config['DIREKTORI']
    if Path(isi+'/install.txt').is_file():
        halaman = request.args.get('halaman', 1, type=int)
        headline = Artikel.query.filter_by(headline = True).order_by(Artikel.tanggaldibuat.desc()).first()
        posts = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        tulisan = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        a1 = Mesin2.query.order_by(Mesin2.no.desc()).limit(30).all()
        #a2 = Mesin2.query.order_by(Mesin2.tgl.desc()).limit(30)
        #a3 = Mesin3.query.order_by(Mesin3.tgl.desc()).limit(30)
        #a4 = Mesin4.query.order_by(Mesin4.tgl.desc()).limit(30)
        return render_template('main/alba2.html', posts=posts, headline=headline,tulisan=tulisan,title="Beranda",a1=a1)
    else:
        return redirect(url_for('main.install'))

@main.route("/jayapura3")
def jayapura3():
    isi=current_app.config['DIREKTORI']
    if Path(isi+'/install.txt').is_file():
        halaman = request.args.get('halaman', 1, type=int)
        headline = Artikel.query.filter_by(headline = True).order_by(Artikel.tanggaldibuat.desc()).first()
        posts = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        tulisan = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        a1 = Mesin3.query.order_by(Mesin3.no.desc()).limit(30).all()
        #a2 = Mesin2.query.order_by(Mesin2.tgl.desc()).limit(30)
        #a3 = Mesin3.query.order_by(Mesin3.tgl.desc()).limit(30)
        #a4 = Mesin4.query.order_by(Mesin4.tgl.desc()).limit(30)
        return render_template('main/alba3.html', posts=posts, headline=headline,tulisan=tulisan,title="Beranda",a1=a1)
    else:
        return redirect(url_for('main.install'))

#halaman blog
@main.route("/blog", methods=['GET', 'POST'])
def blog():
    isi=current_app.config['DIREKTORI']
    if Path(isi+'/install.txt').is_file():
        halaman = request.args.get('halaman', 1, type=int)
        headline = Artikel.query.filter_by(headline = True).order_by(Artikel.tanggaldibuat.desc()).limit(3).all()
        posts = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=6)
        tulisan = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        return render_template('main/home.html', posts=posts, headline=headline,tulisan=tulisan,title="Blog")
    else:
        return redirect(url_for('main.install'))

#halaman per artikel
@main.route("/artikel/<string:idartikel>", methods=['GET', 'POST'])
def artikel(idartikel=None):
    form = FormPengikut()
    halaman = request.args.get('halaman', 1, type=int)
    tulisan = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
    form_comment = FormKomentar(prefix='form_comment')
    form_reply = FormKomentar(prefix='form_reply')
    artikel = Artikel.query.filter_by(slug=idartikel, publish=True).first_or_404()
    similar = Artikel.query.join(Artikel.tags).filter(Tag.id==artikel.tags[0].id, Artikel.id != artikel.id).order_by(Artikel.tanggaldibuat.desc()).limit(3).all()
    if current_user.is_anonymous:
        artikel.dibaca += 1
        dbase.session.commit()
    if form.validate_on_submit():
        sub = Pengikut(surel=form.email.data)
        dbase.session.add(sub)
        dbase.session.commit()
        flash('Data Anda berhasil disimpan, kami akan mengirim email ke Anda jika ada pembaruan konten', 'is-success is-light')
        return redirect(request.url)
    if form_comment.validate_on_submit():
        comment = Komentar(nama=form_comment.nama.data, surel=form_comment.email.data, website=form_comment.website.data, komentar=form_comment.comment.data, publish=True,idartikel=artikel.id)
        dbase.session.add(comment)
        dbase.session.commit()
        flash('Komentar berhasil ditambahkan', 'is-success')
        return redirect(url_for('main.artikel', berita=artikel.kategori.slug, idartikel=artikel.slug))
    if form_reply.validate_on_submit():
        reply_id = request.form.get('balasanId')
        reply = Komentar(nama=form_reply.nama.data, surel=form_reply.email.data,
        website=form_reply.website.data, komentar=form_reply.comment.data, publish=True,
        idbalasan=reply_id, idartikel=artikel.id
        )
        dbase.session.add(reply)
        dbase.session.commit()
        flash('Balasan komentar berhasil ditambahkan', 'is-success')
        return redirect(url_for('main.artikel', berita=artikel.kategori.slug, idartikel=artikel.slug))   
    
    return render_template('main/detail.html', post=artikel, meta=artikel.judul, similar=similar, form_comment=form_comment, form_reply=form_reply,tulisan=tulisan)

#halaman per kategori
@main.route("/kategori/<string:permalinkkategori>")
def kategori(permalinkkategori):
    halaman = request.args.get('halaman', 1, type=int)
    tulisan = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
    kategori = Kategori.query.all()
    single_kategori = Kategori.query.filter_by(slug=permalinkkategori).first_or_404()
    halaman = request.args.get('halaman', 1, type=int)
    posts = Artikel.query.filter_by(idkategori=single_kategori.id).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=5)
    return render_template('main/category.html', kategori=kategori, posts=posts, single_kategori=single_kategori, label='kategori',tulisan=tulisan,title='Kategori')

#halaman pencarian
@main.route("/search")
def search():
    search = request.args.get('q', None)
    try:
        halaman = request.args.get('halaman', 1, type=int)
        tulisan = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        search = request.args.get('q', None)
        kata = search.split()
        single_kategori = dict(nama=search)
        halaman = request.args.get('halaman', 1, type=int)
        posts = Artikel.query.filter(Artikel.judul.like('%'+kata[0]+'%'), Artikel.publish==True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=30)
        return render_template('main/category.html', posts=posts, label='pencarian', single_kategori=single_kategori,tulisan=tulisan,title='Pencarian')
    except AttributeError:
        return redirect(url_for('main.home'))
    except IndexError:
        return redirect(url_for('main.home'))

#halaman tags
@main.route("/tags/<string:permalinktag>")
def topik(permalinktag):
    halaman = request.args.get('halaman', 1, type=int)
    tulisan = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
    single_kategori = Tag.query.filter_by(slug=permalinktag).first_or_404()
    halaman = request.args.get('halaman', 1, type=int)
    posts = Artikel.query.join(Artikel.tags).filter(Tag.slug==permalinktag).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=6)
    return render_template('main/tags.html', posts=posts, single_kategori=single_kategori, label='tags',tulisan=tulisan,title='Tags')

#halaman pages halaman
@main.route("/halaman/<string:permalink>")
def halaman(permalink):
    halaman = request.args.get('halaman', 1, type=int)
    isihalaman = Halaman.query.filter_by(slug=permalink).first_or_404()
    tulisan = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
    return render_template('main/halaman.html', halaman=isihalaman,tulisan=tulisan,title='Halaman')

#halaman sitemap
@main.route("/sitemap.xml")
def sitemap_xml():
    artikel = Artikel.query.order_by(Artikel.tanggaldibuat.desc()).all()
    halaman = Halaman.query.order_by(Halaman.tanggaldibuat.desc()).all()
    template = render_template('main/sitemap.xml', artikel=artikel, base_url='/',halaman=halaman)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response

#halaman robots.txt
@main.route("/robots.txt")
def robots_txt():
    return send_from_directory('static', request.path[1:])

#bagian subscriber
@main.route("/pengikut", methods=['GET', 'POST'])
def pengikut():
    form = FormPengikut()
    if form.validate_on_submit():
        alamat=request.form['kembali'] 
        sub = Pengikut(surel=form.email.data)
        dbase.session.add(sub)
        dbase.session.commit()
        flash('Data Anda berhasil disimpan, kami akan mengirim email ke Anda jika ada pembaruan konten', 'is-success is-light')
        return redirect(alamat)
    return redirect(url_for('main.home'))

#halaman kirim kontak
@main.route("/kontak", methods=['GET', 'POST'])
def kontak():
    form = FormHubungi()
    if form.validate_on_submit():
        sub = Hubungi(nama=form.nama.data,surel=form.email.data,pesan=form.pesan.data)
        dbase.session.add(sub)
        dbase.session.commit()
        flash('Pesan Anda berhasil disimpan, kami akan segera akan merespon seluruh pesan anda', 'is-success is-light')
        return redirect(request.url)
    halaman = request.args.get('halaman', 1, type=int)
    tulisan = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
    return render_template('main/hubungi.html',tulisan=tulisan,form=form,title='Kontak')

@main.route("/updatedb")
def updatedb():
    dbase.create_all()
    return ('Sukses')

@main.route("/dataiot")
def dataiot():
    isi=current_app.config['DIREKTORI']
    if Path(isi+'/install.txt').is_file():
        halaman = request.args.get('halaman', 1, type=int)
        headline = Artikel.query.filter_by(headline = True).order_by(Artikel.tanggaldibuat.desc()).first()
        posts = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        tulisan = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        a1 = Mesin1.query.order_by(Mesin1.tgl.desc()).limit(30)
        a2 = Mesin2.query.order_by(Mesin2.tgl.desc()).limit(30)
        a3 = Mesin3.query.order_by(Mesin3.tgl.desc()).limit(30)
        a4 = Mesin4.query.order_by(Mesin4.tgl.desc()).limit(30)
        
        return render_template('main/dataiot.html', posts=posts, headline=headline,tulisan=tulisan,title="Data PH",a1=a1,a2=a2,a3=a3,a4=a4)
    else:
        return redirect(url_for('main.install'))

@main.route("/datasuhu")
def datasuhu():
    isi=current_app.config['DIREKTORI']
    if Path(isi+'/install.txt').is_file():
        halaman = request.args.get('halaman', 1, type=int)
        headline = Artikel.query.filter_by(headline = True).order_by(Artikel.tanggaldibuat.desc()).first()
        posts = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        tulisan = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        a1 = Mesin1.query.order_by(Mesin1.tgl.desc()).limit(30)
        a2 = Mesin2.query.order_by(Mesin2.tgl.desc()).limit(30)
        a3 = Mesin3.query.order_by(Mesin3.tgl.desc()).limit(30)
        a4 = Mesin4.query.order_by(Mesin4.tgl.desc()).limit(30)
        
        return render_template('main/datasuhu.html', posts=posts, headline=headline,tulisan=tulisan,title="Data Suhu",a1=a1,a2=a2,a3=a3,a4=a4)
    else:
        return redirect(url_for('main.install'))

@main.route("/datalembab")
def datalembab():
    isi=current_app.config['DIREKTORI']
    if Path(isi+'/install.txt').is_file():
        halaman = request.args.get('halaman', 1, type=int)
        headline = Artikel.query.filter_by(headline = True).order_by(Artikel.tanggaldibuat.desc()).first()
        posts = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        tulisan = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        a1 = Mesin1.query.order_by(Mesin1.tgl.desc()).limit(30)
        a2 = Mesin2.query.order_by(Mesin2.tgl.desc()).limit(30)
        a3 = Mesin3.query.order_by(Mesin3.tgl.desc()).limit(30)
        a4 = Mesin4.query.order_by(Mesin4.tgl.desc()).limit(30)
        
        return render_template('main/datalembab.html', posts=posts, headline=headline,tulisan=tulisan,title="Data Kelembaban",a1=a1,a2=a2,a3=a3,a4=a4)
    else:
        return redirect(url_for('main.install'))

@main.route("/dataangin")
def dataangin():
    isi=current_app.config['DIREKTORI']
    if Path(isi+'/install.txt').is_file():
        halaman = request.args.get('halaman', 1, type=int)
        headline = Artikel.query.filter_by(headline = True).order_by(Artikel.tanggaldibuat.desc()).first()
        posts = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        tulisan = Artikel.query.filter_by(publish=True).order_by(Artikel.tanggaldibuat.desc()).paginate(page=halaman, per_page=3)
        a1 = Mesin1.query.order_by(Mesin1.tgl.desc()).limit(30)
        a2 = Mesin2.query.order_by(Mesin2.tgl.desc()).limit(30)
        a3 = Mesin3.query.order_by(Mesin3.tgl.desc()).limit(30)
        a4 = Mesin4.query.order_by(Mesin4.tgl.desc()).limit(30)
        
        return render_template('main/dataangin.html', posts=posts, headline=headline,tulisan=tulisan,title="Data Kecepatan Angin",a1=a1,a2=a2,a3=a3,a4=a4)
    else:
        return redirect(url_for('main.install'))

@main.route("/okt2021")
def okt2021():
    isi=current_app.config['DIREKTORI']
    if Path(isi+'/install.txt').is_file():
        start_date = datetime(2021, 10, 1, 0, 0)
        end_date = datetime(2021, 10, 31, 23, 55)
        time_series = generate_time_series(start_date, end_date)

        for entry in time_series:
            random_value = round(generate_random_value(6.1, 6.7), 2)
            
            if entry[0].hour >= 5 and entry[0].hour < 9:
                value = generate_random_value(20.0, 25.0)
                tds = generate_random_value(141, 211)
                air = generate_random_value(1411, 2011)
                lembab = generate_random_value(1121, 2210)
                hum = generate_random_value(45.1, 78.1)
            elif entry[0].hour >= 9 and entry[0].hour < 13:
                value = generate_random_value(25.1, 37.1)
                tds = generate_random_value(212, 312)
                air = generate_random_value(2012, 2113)
                lembab = generate_random_value(2211, 3210)
                hum = generate_random_value(78.2, 56.2)
            elif entry[0].hour >= 13 and entry[0].hour < 18:
                value = generate_random_value(37.1, 25.0)
                tds = generate_random_value(313, 201)
                air = generate_random_value(2114, 2010)
                lembab = generate_random_value(3211, 2878)
                hum = generate_random_value(56.2, 45.1)
            elif entry[0].hour >= 18 and entry[0].hour < 20:
                value = generate_random_value(25.1, 22.0)
                tds = generate_random_value(202, 151)
                air = generate_random_value(2010, 1879)
                lembab = generate_random_value(2778, 1299)
                hum = generate_random_value(45.1, 42.1)
            elif entry[0].hour >= 20 or entry[0].hour < 3:
                value = generate_random_value(22.1, 19.0)
                tds = generate_random_value(152, 121)
                air = generate_random_value(1879, 1567)
                lembab = generate_random_value(1299, 1223)
                hum = generate_random_value(42.0, 39.2)
            else:
                value = generate_random_value(19.1, 20.0)
                tds = generate_random_value(122, 151)
                air = generate_random_value(1657, 1423)
                lembab = generate_random_value(1223, 1120)
                hum = generate_random_value(39.2, 37.2)
            
            comment = Mesin4(ads=round(tds), ph=random_value, air=round(air), lembab=round(lembab), hum=round(hum),temp=round(value, 2),hujan='0',tgl=entry[0].strftime('%d-%m-%Y'),jam=entry[0].strftime('%H-%M-%S'))
            dbase.session.add(comment)
            dbase.session.commit()
        return "Sukses"
    else:
        return redirect(url_for('main.install'))

@main.route("/nov2021")
def nov2021():
    isi=current_app.config['DIREKTORI']
    if Path(isi+'/install.txt').is_file():
        start_date = datetime(2021, 11, 1, 0, 0)
        end_date = datetime(2021, 11, 30, 23, 55)
        time_series = generate_time_series(start_date, end_date)

        for entry in time_series:
            random_value = round(generate_random_value(5.7, 7.1), 2)
            
            if entry[0].hour >= 5 and entry[0].hour < 9:
                value = generate_random_value(21.0, 26.0)
                tds = generate_random_value(142, 212)
                air = generate_random_value(1412, 2012)
                lembab = generate_random_value(1122, 2211)
                hum = generate_random_value(45.2, 78.2)
            elif entry[0].hour >= 9 and entry[0].hour < 13:
                value = generate_random_value(25.1, 37.1)
                tds = generate_random_value(212, 312)
                air = generate_random_value(2012, 2113)
                lembab = generate_random_value(2211, 3210)
                hum = generate_random_value(78.2, 56.2)
            elif entry[0].hour >= 13 and entry[0].hour < 18:
                value = generate_random_value(37.1, 25.0)
                tds = generate_random_value(313, 201)
                air = generate_random_value(2114, 2010)
                lembab = generate_random_value(3211, 2878)
                hum = generate_random_value(56.2, 45.1)
            elif entry[0].hour >= 18 and entry[0].hour < 20:
                value = generate_random_value(25.1, 22.0)
                tds = generate_random_value(202, 151)
                air = generate_random_value(2010, 1879)
                lembab = generate_random_value(2778, 1299)
                hum = generate_random_value(45.1, 42.1)
            elif entry[0].hour >= 20 or entry[0].hour < 3:
                value = generate_random_value(22.1, 19.0)
                tds = generate_random_value(152, 121)
                air = generate_random_value(1879, 1567)
                lembab = generate_random_value(1299, 1223)
                hum = generate_random_value(42.0, 39.2)
            else:
                value = generate_random_value(19.1, 20.0)
                tds = generate_random_value(122, 151)
                air = generate_random_value(1657, 1423)
                lembab = generate_random_value(1223, 1120)
                hum = generate_random_value(39.2, 37.2)
            
            comment = Mesin1(ads=round(tds), ph=random_value, air=round(air), lembab=round(lembab), hum=round(hum),temp=round(value, 2),hujan='0',tgl=entry[0].strftime('%d-%m-%Y'),jam=entry[0].strftime('%H-%M-%S'))
            dbase.session.add(comment)
            dbase.session.commit()
        return "Sukses"
    else:
        return redirect(url_for('main.install'))

@main.route("/des2021")
def des2021():
    isi=current_app.config['DIREKTORI']
    if Path(isi+'/install.txt').is_file():
        start_date = datetime(2021, 12, 1, 0, 0)
        end_date = datetime(2021, 12, 31, 23, 55)
        time_series = generate_time_series(start_date, end_date)

        for entry in time_series:
            random_value = round(generate_random_value(6.2, 7.1), 2)
            
            if entry[0].hour >= 5 and entry[0].hour < 9:
                value = generate_random_value(22.0, 26.0)
                tds = generate_random_value(142, 212)
                air = generate_random_value(1412, 2012)
                lembab = generate_random_value(1122, 2211)
                hum = generate_random_value(55.2, 78.2)
            elif entry[0].hour >= 9 and entry[0].hour < 13:
                value = generate_random_value(25.1, 37.1)
                tds = generate_random_value(212, 312)
                air = generate_random_value(2112, 2113)
                lembab = generate_random_value(2211, 3210)
                hum = generate_random_value(76.2, 56.2)
            elif entry[0].hour >= 13 and entry[0].hour < 18:
                value = generate_random_value(32.1, 25.0)
                tds = generate_random_value(313, 201)
                air = generate_random_value(2114, 2010)
                lembab = generate_random_value(3211, 2878)
                hum = generate_random_value(56.2, 45.1)
            elif entry[0].hour >= 18 and entry[0].hour < 20:
                value = generate_random_value(25.1, 22.0)
                tds = generate_random_value(202, 151)
                air = generate_random_value(2010, 1879)
                lembab = generate_random_value(2778, 1299)
                hum = generate_random_value(45.1, 42.1)
            elif entry[0].hour >= 20 or entry[0].hour < 3:
                value = generate_random_value(22.1, 19.0)
                tds = generate_random_value(152, 121)
                air = generate_random_value(1879, 1567)
                lembab = generate_random_value(1299, 1223)
                hum = generate_random_value(42.0, 39.2)
            else:
                value = generate_random_value(19.1, 20.0)
                tds = generate_random_value(122, 151)
                air = generate_random_value(1657, 1423)
                lembab = generate_random_value(1223, 1120)
                hum = generate_random_value(39.2, 37.2)
            
            comment = Mesin1(ads=round(tds), ph=random_value, air=round(air), lembab=round(lembab), hum=round(hum),temp=round(value, 2),hujan='0',tgl=entry[0].strftime('%d-%m-%Y'),jam=entry[0].strftime('%H-%M-%S'))
            dbase.session.add(comment)
            dbase.session.commit()
        return "Sukses"
    else:
        return redirect(url_for('main.install'))

@main.route("/jan2022")
def jan2022():
    isi=current_app.config['DIREKTORI']
    if Path(isi+'/install.txt').is_file():
        start_date = datetime(2022, 1, 1, 0, 0)
        end_date = datetime(2022, 1, 31, 23, 55)
        time_series = generate_time_series(start_date, end_date)

        for entry in time_series:
            random_value = round(generate_random_value(5.9, 6.8), 2)
            
            if entry[0].hour >= 5 and entry[0].hour < 9:
                value = generate_random_value(22.0, 26.8)
                tds = generate_random_value(142, 212)
                air = generate_random_value(1412, 2012)
                lembab = generate_random_value(1122, 2211)
                hum = generate_random_value(55.2, 78.2)
            elif entry[0].hour >= 9 and entry[0].hour < 13:
                value = generate_random_value(25.1, 37.1)
                tds = generate_random_value(212, 312)
                air = generate_random_value(2112, 2113)
                lembab = generate_random_value(2211, 3210)
                hum = generate_random_value(76.2, 56.2)
            elif entry[0].hour >= 13 and entry[0].hour < 18:
                value = generate_random_value(32.1, 25.0)
                tds = generate_random_value(313, 201)
                air = generate_random_value(2114, 2010)
                lembab = generate_random_value(3211, 2878)
                hum = generate_random_value(56.2, 45.1)
            elif entry[0].hour >= 18 and entry[0].hour < 20:
                value = generate_random_value(25.1, 22.0)
                tds = generate_random_value(202, 151)
                air = generate_random_value(2010, 1879)
                lembab = generate_random_value(2778, 1299)
                hum = generate_random_value(45.1, 42.1)
            elif entry[0].hour >= 20 or entry[0].hour < 3:
                value = generate_random_value(22.1, 19.0)
                tds = generate_random_value(152, 121)
                air = generate_random_value(1879, 1567)
                lembab = generate_random_value(1299, 1223)
                hum = generate_random_value(42.0, 39.2)
            else:
                value = generate_random_value(19.1, 21.0)
                tds = generate_random_value(122, 151)
                air = generate_random_value(1657, 1423)
                lembab = generate_random_value(1223, 1120)
                hum = generate_random_value(39.2, 37.2)
            
            comment = Mesin1(ads=round(tds), ph=random_value, air=round(air), lembab=round(lembab), hum=round(hum),temp=round(value, 2),hujan='0',tgl=entry[0].strftime('%d-%m-%Y'),jam=entry[0].strftime('%H-%M-%S'))
            dbase.session.add(comment)
            dbase.session.commit()
        return "Sukses"
    else:
        return redirect(url_for('main.install'))

@main.route("/feb2022")
def feb2022():
    isi=current_app.config['DIREKTORI']
    if Path(isi+'/install.txt').is_file():
        start_date = datetime(2023, 10, 27, 0, 0)
        end_date = datetime(2023, 10, 29, 23, 55)
        time_series = generate_time_series(start_date, end_date)

        for entry in time_series:
            random_value = round(generate_random_value(5.9, 6.8), 2)
            
            if entry[0].hour >= 5 and entry[0].hour < 9:
                value = generate_random_value(28.0, 31.8)
                tds = generate_random_value(142, 212)
                air = generate_random_value(1412, 2012)
                lembab = generate_random_value(1122, 2211)
                hum = generate_random_value(55.2, 78.2)
            elif entry[0].hour >= 9 and entry[0].hour < 13:
                value = generate_random_value(31.1, 37.1)
                tds = generate_random_value(212, 312)
                air = generate_random_value(2112, 2113)
                lembab = generate_random_value(2211, 3210)
                hum = generate_random_value(76.2, 56.2)
            elif entry[0].hour >= 13 and entry[0].hour < 18:
                value = generate_random_value(37.1, 30.0)
                tds = generate_random_value(313, 201)
                air = generate_random_value(2114, 2010)
                lembab = generate_random_value(3211, 2878)
                hum = generate_random_value(56.2, 45.1)
            elif entry[0].hour >= 18 and entry[0].hour < 20:
                value = generate_random_value(30.1, 29.0)
                tds = generate_random_value(202, 151)
                air = generate_random_value(2010, 1879)
                lembab = generate_random_value(2778, 1299)
                hum = generate_random_value(45.1, 42.1)
            elif entry[0].hour >= 20 or entry[0].hour < 3:
                value = generate_random_value(29.1, 28.0)
                tds = generate_random_value(152, 121)
                air = generate_random_value(1879, 1567)
                lembab = generate_random_value(1299, 1223)
                hum = generate_random_value(42.0, 39.2)
            else:
                value = generate_random_value(27.1, 29.0)
                tds = generate_random_value(122, 151)
                air = generate_random_value(1657, 1423)
                lembab = generate_random_value(1223, 1120)
                hum = generate_random_value(39.2, 37.2)
            
            comment = Mesin3(ads=round(tds), ph=random_value, air=round(air), lembab=round(lembab), hum=round(hum),temp=round(value, 2),hujan='0',tgl=entry[0].strftime('%d-%m-%Y'),jam=entry[0].strftime('%H-%M-%S'))
            dbase.session.add(comment)
            dbase.session.commit()
        return "Sukses"
    else:
        return redirect(url_for('main.install'))

