Tests
=====

Inspiré par http://carljm.github.io/django-testing-slides

Unittest
--------

* test granulaire
* isoler fonctionnalités
* aide à structurer le code

Integration (système)
---------------------

* tester l'assemblage du système
* bon pour la régression
* lent
* moins que unit si possible

Tester models
-------------

* Séparer ce qui utilise la db du reste

Example::
    
.. highlight:: python
    :linenothreshold: 5
    
    class MyModel(Model):
        def complicated_method(self):
            # ... pleins de code compliqué
            self.save()
            
Remplacer par:

.. highlight:: python
    :linenothreshold: 5
    
    def complicated_method(obj):
        # ... pleins de code compliqué
        return obj
    
    class MyModel(Model):
        def complicated_method(self):
            complicated_method(self)
            self.save()
            
            
`django.test.Testcase`
--------------------

* Chaque test est exécuté dans une transaction avec un rollback à la fin.
* Utiliser `django.utils.unittest.case.TestCase`, pas de transaction, plus rapide.


Fixtures
--------

* Très difficile à maintenir.
* Ajoute des dépendances entre les tests.
* Lent, chaque test doit le loader.

Factory boy
-----------

* Model factories.

.. highlight:: python
    :linenothreshold: 5
    
    # models.py
    class Group(Model):
        name = CharField()
    
    class User(Model):
        name = CharField(blank=True, null=True)
        username = Charfield(unique=True)
        email = Charfield()
        group = ForeignKey(Group)
    
    # factories.py
    class GroupFactory(DjangoModelFactory):
        
        class Meta:
            model = Group
            
        name = 'group'
        
    class UserFactory(DjangoModelFactory):
        
        class Meta:
            model = User
            
        username = factory.Sequence(lambda n: 'username_{0}'.format(n))
        email = factory.Sequence(lambda n: 'person{0}@example.com'.format(n))
        group = factory.SubFactory(GroupFactory)


* Facile à maintenir.  Si on ajoute un champ obligatoire on met la valeure par défaut et les
  tests déjà codé ne seront pas affecté.
* Uniquement créer en db nos besoins.
* Identifier clairement ce que l'on veut tester.

.. highlight:: python
    :linenothreshold: 5
    
    class MyTests(TestCase):
        def my_test():
            user1 = UserFactory()
            
            # specified group name because that is what we want to test
            user2 = UserFactory(email='mtemail@example.com', group__name='group2')
            
            user1.do_something()
            user2.do_something()
            
            self.assertEqual(user2.group.name, 'group2')

* Ne pas créer en db si pas besoin.
