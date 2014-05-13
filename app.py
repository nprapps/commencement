#!/usr/bin/env python

import argparse
from flask import Flask, Markup, render_template
import random
from urlparse import urlparse

from typogrify.templatetags import jinja_filters

import app_config
import data
from render_utils import make_context, urlencode_filter
import static

app = Flask(app_config.PROJECT_SLUG)

app.jinja_env.filters['urlencode'] = urlencode_filter
jinja_filters.register(app.jinja_env)

@app.route('/')
def index():
    """
    Example view demonstrating rendering a simple HTML page.
    """
    context = make_context()

    speeches = []
    for speech in data.load():
        if speech.get('full_text_link', None):
            url = speech['full_text']
        else:
            url = speech['source_url']

        speech['web_source_credit'] = urlparse(url).netloc.replace('www.', '')
        speeches.append(speech)

        if speech['slug'] == app_config.INITIAL_SPEECH_SLUG:
            context['featured'] = speech

    context['speeches'] = sorted(speeches, key=lambda x: x['name'])

    with open('www/static-data/data.json') as f:
        context['speeches_json'] = Markup(f.read())

    return render_template('index.html', **context)

@app.route('/speech/<string:slug>/')
def _speech(slug):
    """
    Example view demonstrating rendering a simple HTML page.
    """
    context = make_context()

    context['speeches'] = data.load()
    context['speech'] = next(s for s in context['speeches'] if s['slug'] == slug)

    context['share_url'] = 'http://%s/%s/speech/%s/' % (app_config.PRODUCTION_S3_BUCKETS[0], app_config.PROJECT_SLUG, slug)
    context['money_quote_image'] = '%s/quote-images/%s.png' % (app_config.S3_BASE_URL, slug)
    context['share_text'] = '%(name)s\'s commencement address at %(school)s in %(year)s.' % context['speech']

    with open('www/static-data/data-thin.json') as f:
        context['speeches_json'] = Markup(f.read())

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
