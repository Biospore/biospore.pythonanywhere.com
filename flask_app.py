#!/usr/bin/python3

from flask import Flask, render_template, request, make_response
from os import walk
from marshaller import Storage, Storage2
import jinja2


app = Flask(__name__)


unique_visitors = Storage()
comments2 = Storage2()


try:
    ufile = open('marshalled.xml')
    unique_visitors.unmarshal(ufile.read())
    ufile.close()
    mfile = open('comments.xml')
    comments.unmarshal(mfile.read())
    mfile.close()
except:
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
    if name and email and text:
        comments2.add_comment(name, email, text)
    marsh = comments2.marshal()
    mfile = open('comments.xml', 'w+')
    mfile.write(marsh)
    mfile.close()


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
    unique_visitors.add_ip(request.headers.get('X-Real-IP'))
    return render_template('comments.html', visitors=unique_visitors.get_counter(), comments=all_comments)

@app.route('/about/')
def about():
    _add_comm()
    unique_visitors.add_ip(request.headers.get('X-Real-IP'))
    return render_template('about.html', visitors=unique_visitors.get_counter())


@app.route('/gallery/')
def gallery():
    unique_visitors.add_ip(request.headers.get('X-Real-IP'))
    gallery = []
    _add_comm()
    query = request.args.get('current')
    bg = request.cookies.get('bgimage')
    images = get_all_imgs('static/images')
    for image in images:
        gallery.append(tuple(['images/'+image, 'thumbnails/'+image[:-4]+'_thumb'+image[-4:]]))
    gallery = [('images/pic7.jpg', 'thumbnails/pic7_thumb.jpg'), ('images/pic0.jpg', 'thumbnails/pic0_thumb.jpg'), ('images/pic2.jpg', 'thumbnails/pic2_thumb.jpg'), ('images/pic6.jpg', 'thumbnails/pic6_thumb.jpg'), ('images/pic4.jpg', 'thumbnails/pic4_thumb.jpg'), ('images/pic1.jpg', 'thumbnails/pic1_thumb.jpg'), ('images/pic8.jpg', 'thumbnails/pic8_thumb.jpg'), ('images/pic5.jpg', 'thumbnails/pic5_thumb.jpg'), ('images/pic3.jpg', 'thumbnails/pic3_thumb.jpg')]
    response = make_response(render_template('gallery.html', gallery=gallery, query=query, bg=bg, visitors=unique_visitors.get_counter()))
    return response

@app.route('/barley-break/')
def bb():
    _add_comm()
    unique_visitors.add_ip(request.headers.get('X-Real-IP'))
    return render_template('barley-break.html', visitors=unique_visitors.get_counter())

def get_all_imgs(folder):
    files = []
    for (dirpath, dirnames, filenames) in walk(folder):
        files.extend(filenames)
    return files

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
