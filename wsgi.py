# -*- coding: utf-8 -*-

"""
WSGI entry point to load from mod_wsgi of Apache.
It add site-packages of virtualenv to the system python.
(Be careful of the python version support of mod_wsgi)
"""

import os
import sys
import site

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_presentation.settings'


def application(environ, start_response):
    """
    Grap Environement vars and return class Django WSGI application.
    """
    if 'VIRTUALENV_PATH' in environ.keys():
        os.environ['VIRTUALENV_PATH'] = environ['VIRTUALENV_PATH']

    if 'DJANGO_SETTINGS_MODULE' in environ.keys():
        os.environ['DJANGO_SETTINGS_MODULE'] = \
            environ['DJANGO_SETTINGS_MODULE']

    ROOT = os.path.dirname(__file__)
    VIRTUALENV_PATH = os.environ['VIRTUALENV_PATH']

    version = 'python%s' % sys.version[0:3]

    site_packages = os.path.join(
        VIRTUALENV_PATH, 'lib', version, 'site-packages')
    site.addsitedir(site_packages)

    sys.path.append(ROOT)

    activate_this = os.path.join(
        VIRTUALENV_PATH, 'bin', 'activate_this.py')
    activate_env = os.path.expanduser(activate_this)
    execfile(activate_env, dict(__file__=activate_env))

    from django.core.wsgi import get_wsgi_application
    _wsgi_application = get_wsgi_application()
    return _wsgi_application(environ, start_response)