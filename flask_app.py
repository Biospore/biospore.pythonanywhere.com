#!/usr/bin/python3

from flask import Flask, render_template, request, make_response
from os import walk
import bleach

from marshaller import Storage, Storage2, Storage3
import jinja2


app = Flask(__name__)


unique_visitors = Storage()
comments2 = Storage2()
imgs = Storage3()

def get_all_imgs(folder):
    files = []
    for (dirpath, dirnames, filenames) in walk(folder):
        files.extend(filenames)
    return files

try:
    unique_visitors.unmarshal('marshalled.xml')
    comments2.unmarshal('comments.xml')
    images = get_all_imgs('static/images')
    imgs.unmarshal('images.xml')
except Exception as e:
    print(e)
    pass


def _add_comm():
    try:
        ufile = open('marshalled.xml', 'w+')
        ufile.write(unique_visitors.marshal())
        ufile.close()
    except Exception as e:
        pass
    name = request.args.get('uname')
    email = request.args.get('uemail')
    text = request.args.get('umessage')
    name = bleach.clean(name, tags=['b', 'i', 'img'], attributes=['src', 'name', 'type'])
    email = bleach.clean(email, tags=['b', 'i', 'img'], attributes=['src', 'name', 'type'])
    text = bleach.clean(text, tags=['b', 'i', 'img'], attributes=['src', 'name', 'type'])
    if name and email and text:
        comments2.add_comment(name, email, text)
    marsh = comments2.marshal()
    mfile = open('comments.xml', 'w+')
    mfile.write(marsh)
    mfile.close()

def liked():
    rit = request.args.get('i')
    who = str(request.headers.get('X-Real-IP'))
    if i and who:
        imgs.liked(rit, who)
        stt = imgs.marshal()
        fh = open('images.xml', 'w+')
        fh.write(stt)
        fh.close()
#hashlib.sha256(str(time.gmtime()[0:]).encode()).hexdigest()

@app.route('/')
@app.route('/index/')
@app.route('/home/')
def home():
    _add_comm()
    unique_visitors.add_ip(request.headers.get('X-Real-IP'))
    return render_template('home.html', visitors=unique_visitors.get_counter())

@app.route('/comments/')
def comments():
    _add_comm()
    all_comments = comments2.get_comments()
    cleared_comments = []
    for comm in all_comments:
        name, email, text = comm
        name = bleach.clean(name, tags=['b', 'i', 'img'], attributes=['src', 'name', 'type'])
        email = bleach.clean(email, tags=['b', 'i', 'img'], attributes=['src', 'name', 'type'])
        text = bleach.clean(text, tags=['b', 'i', 'img'], attributes=['src', 'name', 'type'])
        cleared_comments.append((name, email, text))
    unique_visitors.add_ip(request.headers.get('X-Real-IP'))
    return render_template('comments.html', visitors=unique_visitors.get_counter(), comments=cleared_comments)

@app.route('/comments/comments.xml')
def get_comments_xml():
    fh = open('comments.xml', 'r')
    data = fh.read()
    fh.close()
    return data

@app.route('/about/')
def about():
    _add_comm()
    unique_visitors.add_ip(request.headers.get('X-Real-IP'))
    return render_template('about.html', visitors=unique_visitors.get_counter())

@app.route('/gallery/images.xml')
def get_images_xml():
    fh = open('images.xml', 'r')
    data = fh.read()
    fh.close()
    return data


@app.route('/gallery/')
def gallery():
    unique_visitors.add_ip(request.headers.get('X-Real-IP'))
    gallery = []
    _add_comm()
    liked()
    query = request.args.get('current')
    bg = request.cookies.get('bgimage')
    gallery = imgs.get_all_images()
    ip = str(request.headers.get('X-Real-IP'))
    response = make_response(render_template('gallery.html', gallery=gallery, query=query, bg=bg, ip=ip, visitors=unique_visitors.get_counter()))
    return response

@app.route('/barley-break/')
def bb():
    _add_comm()
    unique_visitors.add_ip(request.headers.get('X-Real-IP'))
    return render_template('barley-break.html', visitors=unique_visitors.get_counter())



#@app.route('/<page>/')
#def autofind(page='index'):
#    return render_template(page + '.html')


@app.errorhandler(404)
def not_found(e):
    _add_comm()
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    _add_comm()
    return render_template('403.html'), 403


@app.errorhandler(500)
def internal_server_error(e):
    _add_comm()
    return render_template('500.html'), 500

@app.errorhandler(410)
def gone(e):
    _add_comm()
    return render_template('410.html'), 410

@app.context_processor
def get_all_menu_items():
    items = [
        ('/',           'Home'),
        ('/gallery/',   'Gallery'),
        ('/about/',     'About'),
        ('/comments/', 'Comments')
    ]
    return dict(menu_items=items)
"""
@app.context_processor
def get_all_pages():
    result = set()
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods:
            url = rule.rule
            result.add_ip(url)
    return dict(pages=result)
"""
