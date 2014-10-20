# -*- coding: utf-8 -*-

INSTALLED_APPS += (  # NOQA
    'raven.contrib.django',
)

RAVEN_CONFIG = {
    'dsn': 'http://5dd0bfcc13b04da8aeba27e309714589:c5643b8aca874bad8ec5a1b1f8fbfa49@sentry.williamdev.com/32',  # NOQA
}