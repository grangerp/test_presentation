# -*- coding: utf-8 -*-

import os

from version import get_version

from django.conf import settings


def version(request):
    """
    release number +  #commit if exists
    """
    version = get_version('normal')
    commit_file = os.path.join(settings.STATIC_ROOT, 'commit.txt')
    if os.path.exists(commit_file):
        commit = open(commit_file, 'r').read()
        version = '%s #%s' % (version, commit)
    return {'version': version}