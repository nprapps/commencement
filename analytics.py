#!/usr/bin/env python

from datetime import date
import json
import app_config

from apiclient.errors import HttpError
from oauth2client import client

from etc.ga import GoogleAnalytics

path = '/%s/speech' % app_config.PROJECT_SLUG

def query_results():
    """
    Query some things.
    """
    ga = GoogleAnalytics()

    try:
        results = ga.query(
            start_date=date(2014, 5, 12),
            end_date=date(2014, 5, 28),
            metrics='ga:pageviews',
            dimensions='ga:pagePath',
            filters='ga:pagePath=~^%s' % path,
            sort='-ga:pageviews',
            start_index='1',
            max_results='10'
        )
        write_results(results)
    except TypeError, error:
        print ('There was an error in constructing your query : %s' % error)
    except HttpError, error:
        print ('API error : %s : %s' % (error.resp.status, error._get_reason()))
    except client.AccessTokenRefreshError:
        print ('Credentials have been revoked or expired, please re-run the application to re-authorize')

def write_results(results):
    payload = {}
    payload['sampling'] = {}
    payload['sampling']['sampled'] = False
    payload['sampling']['sample_size'] = None


    if results['containsSampledData']:
        payload['sampling']['sampled'] = True
        payload['sampling']['sample_size'] = 'Sampled: %.2f%' % (float(results['sampleSize']) / float(results['sampleSpace']) * 100)

    payload['results'] = []

    with open('www/static-data/data.json') as f:
        data = json.load(f)

    for url, count in results.get('rows', []):
        slug = url.replace(path, '').replace('.html', '').replace('/', '')
        speech_data = {}

        for speech in data:
            print speech['slug']

            if speech['slug'] == slug:
                speech_data = speech

                speech = {
                    'slug': slug,
                    'count': count,
                    'name': speech_data['name'],
                    'school': speech_data['school'],
                    'year': speech_data['year'],
                    'img': '%s/assets/mugs/%s' % (app_config.S3_BASE_URL, speech_data['img'])
                }

                payload['results'].append(speech)

    with open('www/live-data/most-viewed.json', 'wb') as writefile:
        writefile.write(json.dumps(payload))

if __name__ == '__main__':
    query_results()
