# -*- coding: utf-8 -*-

from split_settings.tools import optional, include

include(
    'base.py',
    'south.py',
    'locale.py',
    'nose.py',
    'logger.py',
    'django_suit.py',
    'raven.py',
    'rosetta.py',
    'django_compressor.py',
    'test_presentation.py',
    optional('local_settings.py'),
    'debugtoolbar.py',
    scope=locals()
)