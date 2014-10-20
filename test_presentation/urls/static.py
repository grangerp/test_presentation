# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, url, patterns


media_pattern = r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/')
static_pattern = r'^%s/(?P<path>.*)$' % settings.STATIC_URL.strip('/')

if settings.DEBUG:
    urlpatterns += patterns(  # NOQA
        '',
        url(media_pattern, 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    )