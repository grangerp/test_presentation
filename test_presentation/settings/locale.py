# -*- coding: utf-8 -*-

import os


TIME_ZONE = 'America/Montreal'

LANGUAGE_CODE = 'fr'

USE_I18N = True

LANGUAGES = (
    ('fr', u'Français'),
    ('en', u'English'),
)

middlewares = list(MIDDLEWARE_CLASSES)  # NOQA

idx = middlewares.index('django.middleware.common.CommonMiddleware')
middlewares.insert(
    idx,
    'django.middleware.locale.LocaleMiddleware'
)
MIDDLEWARE_CLASSES = middlewares  # NOQA

LOCALE_PATHS = (
    unicode(os.path.join(BASE_DIR, 'locale', )),  # NOQA
)