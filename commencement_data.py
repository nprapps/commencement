#!/usr/bin/env python

import codecs
import csv
import datetime
import json
import re

from oauth import get_credentials
from typogrify.filters import smartypants
from urlparse import urlparse, parse_qs

import requests

import app_config

SPREADSHEET_URL_TEMPLATE = 'https://docs.google.com/feeds/download/spreadsheets/Export?exportFormat=csv&key=%s&gid=0'

def download():
    """
    Downloads the speeches CSV from google docs.
    """
    credentials = get_credentials()
    url = SPREADSHEET_URL_TEMPLATE % app_config.DATA_GOOGLE_DOC_KEY
    print url
    response = app_config.authomatic.access(credentials, url)

    with codecs.open('data/data.csv', 'wb', 'utf-8') as writefile:
        writefile.write(response.content)

def slugify(row):
    bits = []

    for field in ('name', 'school', 'year'):
        d = row[field]

        if d:
            d = str(d)
            d = d.lower()
            d = re.sub(r"[^\w\s]", '', d)
            d = re.sub(r"\s+", '-', d)

            bits.append(d)

    slug = '-'.join(bits) 

    return slug

def parse():
    """
    Parses the data CSV to JSON.
    """
    with open('data/data.csv', 'rb') as readfile:
        rows = list(csv.DictReader(readfile))

    print "Start parse(): %i rows." % len(rows)

    speeches = []
    speeches_by_tag = {}

    for row in rows:
        for k, v in row.items():
            row[k] = v.strip()

        row['year'] = None
        row['youtube_id'] = None
        row['vimeo_id'] = None

        if not row['name']:
            #print 'Skipping row without name'
            continue

        if row['date']: 
            if re.match('\d{1,2}/\d{1,2}/\d{4}', row['date']):
                try:
                    month, day, year = map(int, row['date'].split('/'))
                except:
                    print 'Unrecognized date format: "%s"' % row['date']
                    row['date'] = None

                row['year'] = year

                # NOTE: nonsense so month will format correctly
                # (strftime doens't work on dates before 1900)
                d = datetime.date(2000, month, day)

                row['date'] = '%s %i, %i' % (d.strftime('%B'), day, year) 
            elif re.match('\d{4}', row['date']):
                year = int(row['date'])

                row['year'] = year
                row['date'] = '%i' % year
            else:
                print 'Unrecognized date format: "%s"' % row['date']
                row['date'] = None
        else:
            print 'No date for %(name)s at %(school)s' % row 
            row['date'] = None

        if row['video_url']:
            o = urlparse(row['video_url'])

            if o.netloc.find('youtu') >= 0:
                if parse_qs(o.query):
                    row['youtube_id'] = parse_qs(o.query)['v'][0]
                else:
                    row['youtube_id'] = o.path.split('/')[-1]
            elif o.netloc.find('vimeo') >= 0:
                row['vimeo_id'] = o.path.split('/')[-1]

        if row['money_quote']:
            row['money_quote'] = smartypants(row['money_quote'].strip('"'))

        tags = [t.strip().lower().replace(' ', '-').replace('\'', '')
                for t in row['take_homes'].replace(',', ';').split(';')]
        row['tags'] = []

        for tag in tags:
            if not tag:
                continue

            if tag not in app_config.TAGS:
                print 'Unrecognized tag: "%s" (%s)' % (tag, row['name']) 
                continue

            row['tags'].append(tag)

            if tag not in speeches_by_tag:
                speeches_by_tag[tag] = [] 

            speeches_by_tag[tag].append(row)

        row['slug'] = slugify(row)
        row['name'] = smartypants(row['name'])
        row['school'] = smartypants(row['school'])

        speeches.append(row)

    # Generate related speeches
    for speech in speeches:
        speech['related'] = {}

        for tag in speech['tags']:
            speech['related'][tag] = []
            next_speech = None

            for index, tag_speech in enumerate(speeches_by_tag[tag]):
                if tag_speech['slug'] == speech['slug']:
                    if index + 1 < len(speeches_by_tag[tag]):
                        next_speech = index + 1
                    else:
                        next_speech = 0

            speech['related'][tag].append({
                'slug': speeches_by_tag[tag][next_speech]['slug'],
                'name': speeches_by_tag[tag][next_speech]['name'],
                'school': speeches_by_tag[tag][next_speech]['school'],
                'year': speeches_by_tag[tag][next_speech]['year'],
                'img': speeches_by_tag[tag][next_speech]['img']
            })


    # Strip unused fields to keep filesize down
    del row['take_homes']

    # Render complete data
    with open('www/static-data/data.json', 'w') as f:
        f.write(json.dumps(speeches))

    for tag, speeches in speeches_by_tag.items():
        print '%s: %i' % (tag, len(speeches))

    thin_speeches = []

    for speech in speeches:
        thin_speeches.append({
            'slug': speech['slug'],
            'name': speech['name'],
            'school': speech['school'],
            'tags': speech['tags'],
            'year': speech['year']
        })

    # Render thin data for index
    with open('www/static-data/data-thin.json', 'w') as f:
        f.write(json.dumps(thin_speeches))

    print "Finished."

def load():
    """
    Load the parsed JSON.
    """
    with open('www/static-data/data.json') as f:
        data = json.load(f)

    return data 
