# -*- coding: utf-8 -*-

SECRET_KEY = 'type random secret_key'

SUIT_CONFIG = {
    'ADMIN_NAME': u'test_presentation',
}

# Make  '' first app to overload templates
apps = list(INSTALLED_APPS)  # NOQA
apps.insert(
    0,
    'test_presentation',
)
INSTALLED_APPS = apps


INSTALLED_APPS += (  # NOQA
)

TEMPLATE_CONTEXT_PROCESSORS += (  # NOQA
    'test_presentation.context_processors.version',
)

MIDDLEWARE_CLASSES += (  # NOQA
    'test_presentation.middleware.GoogleAnalyticsMiddleware',
)

GOOGLE_ANALYTICS_TOKEN = ''