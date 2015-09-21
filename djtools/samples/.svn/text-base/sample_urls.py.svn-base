# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

handler500 = 'django.views.defaults.server_error'
handler404 = 'django.views.defaults.page_not_found'

# Serving media files
urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^djtools_media/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.PROJECT_ROOT + 'djtools/media/'}),
)

# Authencitation
urlpatterns += patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'djtools/templates/login.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
)

urlpatterns += patterns('django.views.generic.simple',
    ('^accounts/$', 'redirect_to', {'url': '/accounts/login/'}),
)

# Includes
urlpatterns += patterns('',
    # (r'^example/(?P<object_id>\d+)/$', 'views.example')
    (r'^admin/(.*)', admin.site.root),
    (r'^djtools/', include('djtools.urls')),
)
