# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, patterns, url

try:
    import debug_toolbar
    djdt = True
except:  # pragma: no cover
    djdt = False

if settings.DEBUG and djdt:
    urlpatterns += patterns(  # NOQA
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )