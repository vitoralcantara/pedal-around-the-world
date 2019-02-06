
from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from django.conf import settings
from settings import PROJECT_PATH

admin.autodiscover()

handler500 = 'django.views.defaults.server_error'
handler404 = 'django.views.defaults.page_not_found'

urlpatterns = patterns('',
    # Example:
    # (r'^stunat/', include('stunat.foo.urls')),
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.PROJECT_PATH + '/media/'}),

    (r'^admin-media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.PROJECT_PATH + '/admin-media/'}),

    (r'^djtools-media/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.PROJECT_PATH + '/djtools/media/'}),
)

urlpatterns += patterns('stunat.views',
    # Geral
    (r'^$', 'index'),
    (r'^change_app/$', 'change_app_and_get_menu_template'),
)

urlpatterns += patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
     {'template_name': 'templates/login.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
     
    (r'^djtools/', include('djtools.urls')),
    (r'^gratuidade/', include('gratuidade.urls')),
    (r'^inventario/', include('inventario.urls')),
    (r'^admin/', include(admin.site.urls)),
    
#    (r'^$', 'django.views.generic.simple.redirect_to', 
#        {'url': '/admin'}),
)
