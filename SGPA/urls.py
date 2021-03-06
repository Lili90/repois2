from django.conf.urls import patterns, include, url
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'demo.views.home', name='home'),
    # url(r'^demo/', include('demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^',include('SGPA.apps.home.urls')),
    url(r'^',include('SGPA.apps.usuario.urls')),
    url(r'^',include('SGPA.apps.roles.urls')),
    url(r'^',include('SGPA.apps.flujo.urls')),
    url(r'^',include('SGPA.apps.proyectos.urls')),
    url(r'^',include('SGPA.apps.sprint.urls')),
    url(r'^',include('SGPA.apps.actividades.urls')),
    url(r'^',include('SGPA.apps.userhistory.urls')),
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
)
