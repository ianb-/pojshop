from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'poj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('shop.urls', namespace="shop")),
    url(r'^shop/', include('shop.urls', namespace="shop")),
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cp/', include('cpanel.urls', namespace="cpanel")),
    url(r'^contact/', include('helpdesk.urls', namespace="helpdesk")),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )