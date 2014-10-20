# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

import factory


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = get_user_model()

    username = factory.Sequence(lambda n: u'user_%s' % n)
    password = '123qwe'

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:  # pragma: no cover
            user.set_password(password)
            user._password = password  # keep non encoded password for login
            if create:  # pragma: no cover
                user.save()
        return user