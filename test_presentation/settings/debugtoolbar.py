# -*- coding: utf-8 -*-

try:
    import debug_toolbar  # NOQA
    djdt = True
except:  # pragma: no cover
    djdt = False


if djdt:  # pragma: no cover
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    INTERNAL_IPS = ('127.0.0.1', )

    middlewares = list(MIDDLEWARE_CLASSES)  # NOQA
    middlewares.insert(
        0,
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    MIDDLEWARE_CLASSES = middlewares

    INSTALLED_APPS += (  # NOQA
        'debug_toolbar',
    )

    CONFIG_DEFAULTS = {
        'INTERCEPT_REDIRECTS': False,
    }