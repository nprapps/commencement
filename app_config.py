#!/usr/bin/env python

"""
Project-wide application configuration.

DO NOT STORE SECRETS, PASSWORDS, ETC. IN THIS FILE.
They will be exposed to users. Use environment variables instead.
See get_secrets() below for a fast way to access them.
"""

import os

"""
NAMES
"""
# Project name to be used in urls
# Use dashes, not underscores!
PROJECT_SLUG = 'commencement'

# The name of the repository containing the source
REPOSITORY_NAME = 'commencement'
REPOSITORY_URL = 'git@github.com:nprapps/%s.git' % REPOSITORY_NAME
REPOSITORY_ALT_URL = None # 'git@bitbucket.org:nprapps/%s.git' % REPOSITORY_NAME'

# Project name used for assets rig
# Should stay the same, even if PROJECT_SLUG changes
ASSETS_SLUG = 'commencement'

# Project name to be used in file paths
PROJECT_FILENAME = 'commencement'

"""
DEPLOYMENT
"""
PRODUCTION_S3_BUCKETS = ['apps.npr.org', 'apps2.npr.org']
STAGING_S3_BUCKETS = ['stage-apps.npr.org']
ASSETS_S3_BUCKET = 'assets.apps.npr.org'

PRODUCTION_SERVERS = ['cron.nprapps.org']
STAGING_SERVERS = ['50.112.92.131']

# Should code be deployed to the web/cron servers?
DEPLOY_TO_SERVERS = False

SERVER_USER = 'ubuntu'
SERVER_PYTHON = 'python2.7'
SERVER_PROJECT_PATH = '/home/%s/apps/%s' % (SERVER_USER, PROJECT_FILENAME)
SERVER_REPOSITORY_PATH = '%s/repository' % SERVER_PROJECT_PATH
SERVER_VIRTUALENV_PATH = '%s/virtualenv' % SERVER_PROJECT_PATH

# Should the crontab file be installed on the servers?
# If True, DEPLOY_TO_SERVERS must also be True
DEPLOY_CRONTAB = False

# Should the service configurations be installed on the servers?
# If True, DEPLOY_TO_SERVERS must also be True
DEPLOY_SERVICES = False

UWSGI_SOCKET_PATH = '/tmp/%s.uwsgi.sock' % PROJECT_FILENAME
UWSGI_LOG_PATH = '/var/log/%s.uwsgi.log' % PROJECT_FILENAME
APP_LOG_PATH = '/var/log/%s.app.log' % PROJECT_FILENAME

# Services are the server-side services we want to enable and configure.
# A three-tuple following this format:
# (service name, service deployment path, service config file extension)
SERVER_SERVICES = [
    ('app', SERVER_REPOSITORY_PATH, 'ini'),
    ('uwsgi', '/etc/init', 'conf'),
    ('nginx', '/etc/nginx/locations-enabled', 'conf'),
]

# These variables will be set at runtime. See configure_targets() below
S3_BUCKETS = []
S3_BASE_URL = ''
SERVERS = []
SERVER_BASE_URL = ''
DEBUG = True

"""
COPY EDITING
"""
COPY_GOOGLE_DOC_KEY = '0AlXMOHKxzQVRdFM0eHpucEdWRzRiMVFDdkY4amx6QkE'
COPY_PATH = 'data/copy.xlsx'

DATA_GOOGLE_DOC_KEY = '1a1SZvyycLpv4w8iyq-wvmT-eUERRGfzVkfliFkaQVnE'
#DATA_GOOGLE_DOC_KEY = '1YJ0oc85wMuL9twZk1o3n8Qpz58lFTlyBpnOpBwlBe70'

"""
SHARING
"""
SHARE_URL = 'http://%s/%s/' % (PRODUCTION_S3_BUCKETS[0], PROJECT_SLUG)

# Will be resized to 120x120, can't be larger than 1MB
TWITTER_IMAGE_URL = '%squote-images/john-f-kennedy-yale-university-1962.png' % SHARE_URL
TWITTER_HANDLE = '@nprviz'
TWITTER_SHARE_TEXT = ''

# 16:9 ("wide") image. FB uses 16:9 in the newsfeed and crops to square in timelines.
# No documented restrictions on size
FACEBOOK_IMAGE_URL = TWITTER_IMAGE_URL
FACEBOOK_APP_ID = '138837436154588'
FACEBOOK_SHARE_TEXT = ''

# Thumbnail image for Google News / Search.
# No documented restrictions on resolution or size
GOOGLE_IMAGE_URL = TWITTER_IMAGE_URL

NPR_DFP = {
    'STORY_ID': '1013',
    'TARGET': 'News_U_S__Education',
    'ENVIRONMENT': 'NPR',
    'TESTSERVER': 'false'
}

"""
SERVICES
"""
GOOGLE_ANALYTICS = {
    'ACCOUNT_ID': 'UA-5828686-4',
    'DOMAIN': PRODUCTION_S3_BUCKETS[0],
    'TOPICS': '[1003,1013]' # e.g. '[1014,3,1003,1002,1001]'
}

COMMENT_PROMPT = 'Leave a comment'
DISQUS_UUID = '$NEW_DISQUS_UUID'

"""
APP-SPECIFIC
"""
TAGS = {
    'balance': 'Balance',
    'be-kind': 'Be kind',
    'change-the-world': 'Change the world',
    'dont-give-up': 'Don\'t give up',
    'dream': 'Dream',
    'embrace-failure': 'Embrace failure',
    'face-fear': 'Face fear',
    'inner-voice': 'Inner voice',
    'make-art': 'Make art',
    'play': 'Play',
    'remember-history': 'Remember history',
    'tips': 'Tips',
    'unplug': 'Unplug',
    'work-hard': 'Work hard',
    'yolo': 'YOLO'
}

INITIAL_SPEECH_SLUG = 'john-f-kennedy-american-1963'

"""
Utilities
"""
def get_secrets():
    """
    A method for accessing our secrets.
    """
    secrets = [
        'EXAMPLE_SECRET'
    ]

    secrets_dict = {}

    for secret in secrets:
        name = '%s_%s' % (PROJECT_FILENAME, secret)
        secrets_dict[secret] = os.environ.get(name, None)

    return secrets_dict

def configure_targets(deployment_target):
    """
    Configure deployment targets. Abstracted so this can be
    overriden for rendering before deployment.
    """
    global S3_BUCKETS
    global S3_BASE_URL
    global SERVERS
    global SERVER_BASE_URL
    global DEBUG
    global DEPLOYMENT_TARGET
    global APP_LOG_PATH
    global DISQUS_SHORTNAME

    if deployment_target == 'production':
        S3_BUCKETS = PRODUCTION_S3_BUCKETS
        S3_BASE_URL = 'http://%s/%s' % (S3_BUCKETS[0], PROJECT_SLUG)
        SERVERS = PRODUCTION_SERVERS
        SERVER_BASE_URL = 'http://%s/%s' % (SERVERS[0], PROJECT_SLUG)
        DISQUS_SHORTNAME = 'npr-news'
        DEBUG = False
    elif deployment_target == 'staging':
        S3_BUCKETS = STAGING_S3_BUCKETS
        S3_BASE_URL = 'http://%s/%s' % (S3_BUCKETS[0], PROJECT_SLUG)
        SERVERS = STAGING_SERVERS
        SERVER_BASE_URL = 'http://%s/%s' % (SERVERS[0], PROJECT_SLUG)
        DISQUS_SHORTNAME = 'nprviz-test'
        DEBUG = True
    else:
        S3_BUCKETS = []
        S3_BASE_URL = 'http://127.0.0.1:8000'
        SERVERS = []
        SERVER_BASE_URL = 'http://127.0.0.1:8001/%s' % PROJECT_SLUG
        DISQUS_SHORTNAME = 'nprviz-test'
        DEBUG = True
        APP_LOG_PATH = '/tmp/%s.app.log' % PROJECT_SLUG

    DEPLOYMENT_TARGET = deployment_target

"""
Run automated configuration
"""
DEPLOYMENT_TARGET = os.environ.get('DEPLOYMENT_TARGET', None)

configure_targets(DEPLOYMENT_TARGET)

