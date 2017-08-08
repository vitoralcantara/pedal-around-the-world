# -*- coding: utf-8 -*-

import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__)) + '/'
PROJECT_NAME = PROJECT_ROOT.split('/')[-2]

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = '' # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = PROJECT_NAME
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'America/Recife'
LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

MEDIA_ROOT = PROJECT_ROOT + 'media/'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin-media/'
DJTOOLS_MEDIA_URL = '/djtools_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'cp6ec19(#d0d#27x7zk9^o9qmf+qdi184%cit^-(ld=1=e2_s)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    PROJECT_NAME + '.djtools.middleware.threadlocals.ThreadLocals',
    'djtools.middleware.exception.UserBasedExceptionMiddleware'
)

ROOT_URLCONF = '%s.urls' % (PROJECT_NAME)

TEMPLATE_DIRS = (
    PROJECT_ROOT,
    os.path.join(PROJECT_ROOT, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'djtools',
    'django_extensions',
)
