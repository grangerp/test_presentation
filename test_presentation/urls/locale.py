# -*- coding: utf-8 -*-

from django.conf.urls import include, patterns

urlpatterns += patterns(  # NOQA
    '',
    (r'^i18n/', include('django.conf.urls.i18n')),
)