

from flask import Flask, render_template


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
    return render_template('gallery.html')


@app.route('/barley-break/')
def bb():
    return render_template('barley-break.html')


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