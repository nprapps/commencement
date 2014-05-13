#!/usr/bin/env python

import argparse
from collections import defaultdict
from flask import Flask, Markup, render_template
import json
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
    context = make_context()

    speeches = []
    for speech in data.load():
        speech['share_url'] = 'http://%s/%s/speech/%s/' % (app_config.PRODUCTION_S3_BUCKETS[0], app_config.PROJECT_SLUG, speech['slug'])
        speech['money_quote_image'] = '%s/quote-images/%s.png' % (app_config.S3_BASE_URL, speech['slug'])
        speech['share_text'] = '%(name)s, %(year)s. From NPR\'s The Best Commencement Speeches, Ever.' % speech
        speeches.append(speech)

        if speech['slug'] == app_config.INITIAL_SPEECH_SLUG:
            context['featured'] = speech

    speeches = sorted(speeches, key=lambda x: x['name'])
    context['speeches'] = speeches
    context['speeches_json'] = json.dumps(speeches)

    return render_template('index.html', **context)

@app.route('/speech/<string:slug>/')
def _speech(slug):
    context = make_context()

    speeches = data.load()

    context['speech'] = next(s for s in speeches if s['slug'] == slug)
    context['share_url'] = 'http://%s/%s/speech/%s/' % (app_config.PRODUCTION_S3_BUCKETS[0], app_config.PROJECT_SLUG, slug)
    context['money_quote_image'] = '%s/quote-images/%s.png' % (app_config.S3_BASE_URL, slug)
    context['share_text'] = '%(name)s, %(year)s. From NPR\'s The Best Commencement Speeches, Ever.' % context['speech']

    # Fancy web source credit line, e.g., See full text at graduationwisdom.com.
    if context['speech'].get('full_text_link', None):
        url = context['speech']['full_text']
    else:
        url = context['speech']['source_url']

    context['speech']['web_source_credit'] = urlparse(url).netloc.replace('www.', '')

    # Horizontal nav.
    context['tags'] = []
    speech_tags = defaultdict(list)

    # Build a dictionary of tags; for each tag, get me a list of the speeches.
    # Loop over all speeches.
    for speech in speeches:

        # Loop over the tags in this speech.
        for tag in speech['tags']:

            # If this speech shares a tag with the page we're on, append it to the list.
            if tag in context['speech']['tags']:
                speech_tags[tag].append(speech)

    # Get the list of speeches that share tags with this speech on a tag-by-tag basis.
    # Sort the list by name. Find the speech that follows this one in the list.
    for tag in context['speech']['tags']:
        speech_tags[tag] = sorted(speech_tags[tag], key=lambda x: x['name'])

        for index, speech in enumerate(speech_tags[tag]):

            if speech['slug'] == context['speech']['slug']:
                # The next speech should just be the one following this one in the list.
                next_speech = speech_tags[tag][index + 1]

                # There is one exception to this rule.
                # Loop over the speeches we've already grabbed using this logic
                # and make sure we don't have the same speech showing up twice.
                # Duplicates are evil.
                for obj in context['tags']:

                    if obj['speech']['slug'] == next_speech['slug']:
                        next_speech = speech_tags[tag][index + 2]

                context['tags'].append({ 'tag': tag.replace('-', ' ').title(), 'speech': next_speech })
                break

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
