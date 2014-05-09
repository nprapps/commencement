#!/usr/bin/env python

from datetime import date
import json

from apiclient.errors import HttpError
from oauth2client import client

from etc.ga import GoogleAnalytics

path = '/playgrounds/playground'

def query_results():
    """
    Query some things.
    """
    ga = GoogleAnalytics()

    try:
        results = ga.query(
            start_date=date(2014, 4, 1),
            end_date=date(2014, 4, 28),
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

    for url, count in results.get('rows', []):
        payload['results'].append({'slug': url.replace(path, '').replace('.html', '').replace('/', ''), 'count': count })

    with open('www/live-data/most-viewed.json', 'wb') as writefile:
        writefile.write(json.dumps(payload))

if __name__ == '__main__':
    query_results()
