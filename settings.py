# -*- coding: utf-8 -*-
# Django settings for stunat project.
from os.path import abspath, dirname

PROJECT_PATH = abspath(dirname(__file__))
PROJECT_NAME = PROJECT_PATH.split('/')[-1]
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'stunat'                        # Or path to database file if using sqlite3.
DATABASE_USER = 'postgres'                      # Not used with sqlite3.
DATABASE_PASSWORD = 'postgres'                  # Not used with sqlite3.
DATABASE_HOST = 'localhost'                     # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '5432'                          # Set to empty string for default. Not used with sqlite3.'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Recife'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

MEDIA_ROOT = PROJECT_PATH + '/media/'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin-media/'
# Djtools Media e JQuery
DJTOOLS_MEDIA_URL = '/djtools-media/'
DJTOOLS_JQUERY_IN_SUPER_TEMPLATE = True

USE_L10N = False
DATE_FORMAT = 'd/m/Y'
DATE_INPUT_FORMATS = (
    '%d/%m/%Y',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '_)32c$uo491b-g2+c*rigu(wefewk7a799fb-^#22e0jix+-yq'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'stunat.djtools.middleware.threadlocals.ThreadLocals',
)

ROOT_URLCONF = 'stunat.urls'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

TEMPLATE_DIRS = (
    '%s/templates' %(PROJECT_PATH),
    PROJECT_PATH
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.auth',
    'comum.utils.stunat_context_processor',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
#    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'djtools',
    'geraldo',
    'comum',
    'gratuidade',
    # EM PRODUÇÃO
    'inventario',    
)

# Nome de referencia para os modulos
APP_CONTENT_TYPES = [
    ['gratuidade', u'Gratuidade'],
    ['inventario', u'Inventário'],
]
# Sessão expira se o navegador for fechado
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
