#!/usr/bin/python3

from flask import Flask, render_template, request
from os import walk


app = Flask(__name__)


@app.route('/')
@app.route('/index/')
@app.route('/home/')
def home():
    return render_template('home.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/gallery/')
def gallery():
    gallery = []
    query = request.args.get('current')
    images = get_all_imgs('static/images')
    for image in images:
        gallery.append(tuple(['images/'+image, 'thumbnails/'+image[:-4]+'_thumb'+image[-4:]]))
    gallery = [('images/pic7.jpg', 'thumbnails/pic7_thumb.jpg'), ('images/pic0.jpg', 'thumbnails/pic0_thumb.jpg'), ('images/pic2.jpg', 'thumbnails/pic2_thumb.jpg'), ('images/pic6.jpg', 'thumbnails/pic6_thumb.jpg'), ('images/pic4.jpg', 'thumbnails/pic4_thumb.jpg'), ('images/pic1.jpg', 'thumbnails/pic1_thumb.jpg'), ('images/pic8.jpg', 'thumbnails/pic8_thumb.jpg'), ('images/pic5.jpg', 'thumbnails/pic5_thumb.jpg'), ('images/pic3.jpg', 'thumbnails/pic3_thumb.jpg')]
    return render_template('gallery.html', gallery=gallery, query=query)


@app.route('/barley-break/')
def bb():
    return render_template('barley-break.html')

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
