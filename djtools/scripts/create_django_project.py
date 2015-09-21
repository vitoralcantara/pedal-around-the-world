#!/usr/bin/env python2.5

import os, sys

def create_django_project():
    filename, project_name = sys.argv
    
    # Creating project
    os.system('django-admin.py startproject %s' % project_name)
    os.system('chmod +x %s/manage.py' % project_name)
    
    # Configuring djtools
    os.system('svn co https://suapsvn.ifrn.edu.br/djtools/trunk %s/djtools' % project_name)
    os.system('cp %s/djtools/samples/sample_settings.py %s/settings.py' \
        % (project_name, project_name))
    os.system('cp %s/djtools/samples/sample_urls.py %s/urls.py' \
        % (project_name, project_name))
    os.system('mkdir %s/media' % project_name)
    os.system('mkdir %s/media/js' % project_name)
    os.system('cp %s/djtools/media/js/*.js %s/media/js' % (project_name, project_name))
    
    # Checking out django_extensions
    os.system('svn co http://django-command-extensions.googlecode.com/svn/trunk/django_extensions %s/django_extensions' % project_name)

if __name__ == '__main__':
    create_django_project()
