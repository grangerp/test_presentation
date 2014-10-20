# -*- coding: utf-8 -*-

from split_settings.tools import include

urlpatterns = []

include(
    'test_presentation.py',
    'admin.py',
    'locale.py',
    'static.py',
    'rosetta.py',
    'debugtoolbar.py',
    scope=locals(),
)