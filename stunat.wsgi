import os, sys
sys.path.append('/var/www/apps_wsgi/trunk/stunat')
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)+'/../'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'stunat.sample_settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
