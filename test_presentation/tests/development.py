# -*- coding: utf-8 -*-

from django_webtest import WebTest
from django.test.utils import override_settings

from .factories import UserFactory


class DebugToolTest(WebTest):
    """
    Ensure tools are loaded in debug mode.
    """
    def test_rosetta(self):
        admin = UserFactory.create(is_staff=True, is_superuser=True)
        response = self.app.get('/rosetta/', user=admin)
        self.assertEqual(response.status_int, 200)
        response.mustcontain('Rosetta')

    @override_settings(DEBUG=True)
    def test_debugtoolbar(self):
        response = self.app.get('/admin/').follow()
        self.assertEqual(response.status_int, 200)
        response.mustcontain('djDebugToolbar')