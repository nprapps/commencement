#!/usr/bin/env python

"""
A very thin client wrapper for Google Analytics.
"""

import argparse
import httplib2
import os
import sys

from apiclient import discovery
from oauth2client import client
from oauth2client.clientsecrets import InvalidClientSecretsError
from oauth2client.file import Storage
from oauth2client import tools

CLIENT_SECRETS = os.path.expanduser('~/.google_analytics_secrets.json')
DAT = os.path.expanduser('~/.google_analytics_auth.dat')

SERVICE_NAME = 'analytics'
SERVICE_VERSION = 'v3'
SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'
NPR_ORG_LIVE_ID = '53470309'

class GoogleAnalytics(object):
    def __init__(self, property_id=NPR_ORG_LIVE_ID):
        self.property_id = property_id

        self.storage = Storage(DAT)
        self.credentials = self.storage.get()
        
        if not self.credentials or self.credentials.invalid:
            self.credentials = self._authorize()
            
        http = self.credentials.authorize(http=httplib2.Http())

        self.service = discovery.build(SERVICE_NAME, SERVICE_VERSION, http=http)

    def _authorize(self):
        """
        Authorize with OAuth2.
        """
        parent_parsers = [tools.argparser]
        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=parent_parsers)

        flags = parser.parse_args(sys.argv[1:])

        try:
            flow = client.flow_from_clientsecrets(
                CLIENT_SECRETS,
                scope=SCOPE
            )
        except InvalidClientSecretsError:
            print 'Client secrets not found at %s' % CLIENT_SECRETS
        
        return tools.run_flow(flow, self.storage, flags)

    def query(self, start_date=None, end_date=None, metrics=None, dimensions=None, filters=None, sort=None, start_index=None, max_results=None):
        """
        Execute a query
        """
        if start_date:
            start_date = start_date.strftime('%Y-%m-%d')

        if end_date:
            end_date = end_date.strftime('%Y-%m-%d')

        return self.service.data().ga().get(
            ids='ga:' + self.property_id,
            start_date=start_date,
            end_date=end_date,
            metrics=metrics,
            dimensions=dimensions,
            filters=filters,
            sort=sort,
            start_index=start_index,
            max_results=max_results
        ).execute()
