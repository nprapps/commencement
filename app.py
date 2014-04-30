#!/usr/bin/env python

import argparse
from flask import Flask, render_template

import app_config
import data
from render_utils import make_context, urlencode_filter
import static

app = Flask(app_config.PROJECT_NAME)

app.jinja_env.filters['urlencode'] = urlencode_filter

@app.route('/')
def index():
    """
    Example view demonstrating rendering a simple HTML page.
    """
    context = make_context()

    context['speeches'] = data.load() 

    return render_template('index.html', **context)

@app.route('/speech/<string:slug>/')
def speech(slug):
    """
    Example view demonstrating rendering a simple HTML page.
    """
    context = make_context()

    context['speeches'] = data.load() 
    context['speech'] = next(s for s in context['speeches'] if s['slug'] == slug)

    return render_template('speech.html', **context)

app.register_blueprint(static.static)

# Boilerplate
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port')
    args = parser.parse_args()
    server_port = 8000

    if args.port:
        server_port = int(args.port)

    app.run(host='0.0.0.0', port=server_port, debug=app_config.DEBUG)
