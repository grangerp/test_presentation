# -*- coding: utf-8 -*-

try:
    finders = STATICFILES_FINDERS
except NameError:
    finders = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

finders += (
    'compressor.finders.CompressorFinder',
)
STATICFILES_FINDERS = finders

INSTALLED_APPS += (  # NOQA
    'compressor',
)

COMPRESS_URL = STATIC_URL  # NOQA

COMPRESS_ROOT = STATIC_ROOT  # NOQA