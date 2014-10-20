# -*- coding: utf-8 -*-

import os  # noqa

ALLOWED_HOSTS = ('*', )

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

STATIC_ROOT = os.path.join(CONTAINER_DIR, 'static')  # NOQA
COMPRESS_ROOT = STATIC_ROOT
MEDIA_ROOT = os.path.join(CONTAINER_DIR, 'media')  # NOQA
CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'ckeditor')