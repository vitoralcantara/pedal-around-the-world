# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import get_commands
from django.template.loader import render_to_string

class Command(BaseCommand):

    def handle(self, *args, **options):
        completion_content = render_to_string(
                'djtools/templates/django_bash_completion', 
                dict(actions=' '.join(get_commands().keys())))
        completion_file = open('django_bash_completion.sh', 'w')
        completion_file.write(completion_content)
        completion_file.close()
        print self.style.SQL_COLTYPE('File django_bash_completion.sh sucessifully created')
        print self.style.SQL_COLTYPE('To use: ". %s/django_bash_completion.sh"' % settings.PROJECT_PATH)
