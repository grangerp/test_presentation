# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, url

if 'rosetta' in settings.INSTALLED_APPS and settings.DEBUG:
    urlpatterns += patterns('',  # NOQA
        url(r'^rosetta/', include('rosetta.urls')),
    )