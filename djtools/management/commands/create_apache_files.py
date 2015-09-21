#!/usr/bin/env python2.5

from django.contrib import admin
from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        server_name, server_admin = args
        base_server_name = server_name.split('.')[0]
        
        project_root = '/'.join(__file__.split('/')[:-4]) + '/'
        project_name = project_root.split('/')[-2]
        project_parent_root = '/'.join(project_root.split('/')[:-2])
        
        # gerando arquivo wsgi
        os.system('rm -rf %sapache' % project_root)
        os.system('mkdir %sapache' % project_root)
        wsgi_content = render_to_string(
                'djtools/templates/apache_project_wsgi', 
                dict(project_parent_root = project_parent_root,
                     project_root        = project_root,
                     project_name        = project_name))
        wsgi_file = open('%sapache/%s.wsgi' % (project_root, base_server_name), 'w')
        wsgi_file.write(wsgi_content)
        wsgi_file.close()
        
        # gerando arquivo virtualhost
        vh_content = render_to_string(
                'djtools/templates/apache_virtualhost_template', 
                dict(server_name         = server_name,
                     base_server_name    = base_server_name,
                     server_admin        = server_admin,
                     project_root        = project_root[:-1], # without '/'
                     project_name        = project_name))
        vh_file = open('%s%s' % (project_root, base_server_name), 'w')
        vh_file.write(vh_content)
        vh_file.close()
        
        # Symbolic link to admin-media
        admin_media_root = '/'.join(admin.__file__.split('/')[:-1]) + '/media'
        os.system('ln -s %s %sadmin-media' % (admin_media_root, project_root))
