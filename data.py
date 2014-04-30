#!/usr/bin/env python

import csv
import datetime
import json
import math

import requests

import app_config

def download():
    """
    Downloads the speeches CSV from google docs.
    """
    csv_url = 'https://docs.google.com/spreadsheets/d/%s/export?format=csv&id=%s&gid=0' % (
        app_config.DATA_GOOGLE_DOC_KEY,
        app_config.DATA_GOOGLE_DOC_KEY)
    r = requests.get(csv_url)

    with open('data/data.csv', 'wb') as writefile:
        writefile.write(r.content)

def slugify(row):
    slug = '%(name)s-%(school)s-%(year)s' % row

    return slug.lower().replace(' ', '-')

def parse():
    """
    Parses the data CSV to JSON.
    """
    with open('data/data.csv', 'rb') as readfile:
        rows = list(csv.DictReader(readfile))

    print "Start parse(): %i rows." % len(rows)

    speeches = []
    tags = {}

    for row in rows:
        for k, v in row.items():
            row[k] = v.strip()

        row['year'] = None
        row['decade'] = None

        if row['date']: 
            try:
                month, day, year = map(int, row['date'].split('/'))
                row['year'] = year
                row['decade'] = math.floor(year / 10) * 10

                d = datetime.date(year, month, day)

                row['date'] = '%s %i %i' % (d.strftime('%B'), day, year) 
            except ValueError:
                print 'Invalid date for %(name)s at %(school)s' % row
        else:
            print 'No date for %(name)s at %(school)s' % row 
            row['date'] = None

        row['tags'] = [t.strip().lower() for t in row['tags'].split(';')]
        
        for tag in row['tags']:
            if tag not in tags:
                tags[tag] = 0

            tags[tag] += 1

        row['slug'] = slugify(row)

        speeches.append(row)

    # print tags
    #for t in ['%s: %i' % (k, v) for k, v in tags.items()]:
    #    print t

    # Render complete data
    with open('www/static-data/data.json', 'w') as f:
        f.write(json.dumps(speeches))

    thin_speeches = []

    for speech in speeches:
        thin_speeches.append({
            'slug': speech['slug'],
            'name': speech['name'],
            'profession': speech['profession'],
            'school': speech['school'],
            'tags': speech['tags'],
            'year': speech['year'],
            'decade': speech['decade']
        })

    del row['money_quote']
    del row['money_quote2']
    del row['still_image_url']
    del row['source_url']

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
