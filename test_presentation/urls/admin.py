# -*- coding: utf-8 -*-

from django.contrib import admin

from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns

admin.autodiscover()

urlpatterns += i18n_patterns(  # NOQA
    '',
    url(r'^admin/', include(admin.site.urls)),
)