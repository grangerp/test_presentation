# -*- coding: utf-8 -*-

from django.conf import settings
from django.test import TestCase
from django.core import mail

from django_webtest import WebTest
from webtest import AppError
from version import get_version

from .factories import UserFactory


class AdminRouteTest(WebTest):
    """
    Test Django admin is plugged at '/admin' with django-suit.
    """
    def test_admin_index(self):
        """
        Test /admin URL with appended or not '/'
        """
        response = self.app.get('/admin')
        self.assertEqual(response.status_int, 302)

        # add prefix language
        response = response.follow()
        self.assertEqual(response.status_int, 301)

        # add prefix language and append slash
        response = response.follow()
        self.assertEqual(response.status_int, 200)

        response.mustcontain('username', 'password')

    def test_admin_i18n_index(self):
        """
        Test Django admin response with each language prefix of settings.
        """
        for language, name in settings.LANGUAGES:
            response = self.app.get('/%s/admin/' % language)
            self.assertEqual(response.status_int, 200)
            response.mustcontain('username', 'password')

    def test_django_suit(self):
        """
        Test if django suit is plugged and respond with custom settings.
        """
        for language, name in settings.LANGUAGES:
            response = self.app.get('/%s/admin/' % language)
            self.assertEqual(response.status_int, 200)
            response.mustcontain(get_version('normal'), 'w.illi.am')


class MailTest(TestCase):
    """
    Test that mails are not really sent by default settings.
    """
    def test_send_mail(self):
        """
        In test mode, locmem backend is used as mailbackend.
        (Check the var where it stores the original one.)
        """
        self.assertEqual(mail._original_email_backend,
                         'django.core.mail.backends.console.EmailBackend')


class DebugTest(WebTest):
    """
    Ensure tools are not loaded in production mode.
    """

    def test_no_rosetta(self):
        admin = UserFactory.create(is_staff=True, is_superuser=True)
        self.assertRaises(AppError, self.app.get, '/rosetta/', user=admin)

    def test_no_debugtoolbar(self):
        response = self.app.get('/admin/').follow()
        self.assertEqual(response.status_int, 200)
        response.mustcontain(no='djDebugToolbar')