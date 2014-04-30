#!/usr/bin/env python

import csv
import json

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
        row['tags'] = [t.strip().lower() for t in row['tags'].split(';')]
        
        for tag in row['tags']:
            if tag not in tags:
                tags[tag] = 0

            tags[tag] += 1

        speeches.append(row)

    with open('www/static-data/data.json', 'wb') as writefile:
        writefile.write(json.dumps(speeches))

    print "Finished."

def load():
    """
    Load the parsed JSON.
    """
    with open('www/static-data/data.json') as f:
        data = json.load(f)

    return data 
