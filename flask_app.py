#!/usr/bin/python3

from flask import Flask, render_template, request, make_response
from os import walk


app = Flask(__name__)

unique_visitors = set()

#hashlib.sha256(str(time.gmtime()[0:]).encode()).hexdigest()

@app.route('/')
@app.route('/index/')
@app.route('/home/')
def home():
    unique_visitors.add(request.remote_addr)
    return render_template('home.html', visitors=len(unique_visitors))


@app.route('/about/')
def about():
    unique_visitors.add(request.remote_addr)
    return render_template('about.html', visitors=len(unique_visitors))


@app.route('/gallery/')
def gallery():
    unique_visitors.add(request.remote_addr)
    gallery = []
    query = request.args.get('current')
    bg = request.cookies.get('bgimage')
    images = get_all_imgs('static/images')
    for image in images:
        gallery.append(tuple(['images/'+image, 'thumbnails/'+image[:-4]+'_thumb'+image[-4:]]))
    gallery = [('images/pic7.jpg', 'thumbnails/pic7_thumb.jpg'), ('images/pic0.jpg', 'thumbnails/pic0_thumb.jpg'), ('images/pic2.jpg', 'thumbnails/pic2_thumb.jpg'), ('images/pic6.jpg', 'thumbnails/pic6_thumb.jpg'), ('images/pic4.jpg', 'thumbnails/pic4_thumb.jpg'), ('images/pic1.jpg', 'thumbnails/pic1_thumb.jpg'), ('images/pic8.jpg', 'thumbnails/pic8_thumb.jpg'), ('images/pic5.jpg', 'thumbnails/pic5_thumb.jpg'), ('images/pic3.jpg', 'thumbnails/pic3_thumb.jpg')]
    response = make_response(render_template('gallery.html', gallery=gallery, query=query, bg=bg, visitors=len(unique_visitors)))
    return response

@app.route('/barley-break/')
def bb():
    unique_visitors.add(request.remote_addr)
    return render_template('barley-break.html', visitors=len(unique_visitors))

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
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(410)
def gone(e):
    return render_template('410.html'), 410

@app.context_processor
def get_all_menu_items():
    items = [
        ('/',           'Home'),
        ('/gallery/',   'Gallery'),
        ('/about/',     'About')
    ]
    return dict(menu_items=items)
"""
@app.context_processor
def get_all_pages():
    result = set()
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods:
            url = rule.rule
            result.add(url)
    return dict(pages=result)
"""
