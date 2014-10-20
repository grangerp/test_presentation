# -*- coding: utf-8 -*-

apps = list(INSTALLED_APPS)  # NOQA
apps.insert(
    apps.index('django.contrib.admin'),
    'suit'
)
INSTALLED_APPS = apps


assert 'django.core.context_processors.request' \
    in TEMPLATE_CONTEXT_PROCESSORS  # NOQA