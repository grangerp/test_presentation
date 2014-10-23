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

    class MyModel(Model):
        def complicated_method(self):
            # ... pleins de code compliqué
            self.save()


Remplacer par::

    def complicated_method(obj):
        # ... pleins de code compliqué
        return obj

    class MyModel(Model):
        def complicated_method(self):
            complicated_method(self)
            self.save()


`django.test.Testcase`
----------------------

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

    ::
    
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


    Example d'utilisation::
        
        # not created on db
        user = UserFactory.build(username='my_username')
        print user.group.name
        # >>> 'group'
        
        # another user with same group
        user2 = UserFactory.build(group=user.group)
        
        # create multiple users with groups
        users = UserFactory.create_batch(size=50)


* Facile à maintenir.  Si on ajoute un champ obligatoire on met la valeure par défaut et les
  tests déjà codé ne seront pas affecté.
* Uniquement créer en db nos besoins.
* Identifier clairement ce que l'on veut tester.

    ::

        class MyTests(TestCase):
            def my_test():
                user1 = UserFactory()
    
                # specified group name because that is what we want to test
                user2 = UserFactory(email='email@example.com', group__name='group2')
    
                user1.do_something()
                user2.do_something()
    
                self.assertEqual(user2.group.name, 'group2')
                self.assertEqual(user2.email, 'email@example.com')

* Ne pas créer en db si pas besoin.


Tester `views`
--------------

* Django a des outils pour faire des test unitaire sur les views.

    ::
    
        def test_post_form(self):
            request = RequestFactory().post(
                '/user/add/', {'first_name': 'first', 'last_name': 'last'}
            )
            response = add_user(request)
            
            self.assertIn('new_user', response.context)
            
* Essayer de limiter les test unitaire sur les views.
* Limiter le code dans les views et les tester avec des test fonctionnel. 

    ::
    
        def test_post_form(self):
            response = self.client.post(
                '/user/add/', {'first_name': 'first', 'last_name': 'last'}
            )
            
            self.assertIn('new_user', response.context)
            
* Problèmes ossible avec cette approche.
    * Il manque le champ first_name dnas le template, le test va quand même passer.
    * Un intégrateur a supprimé le tag {% csrf_token %} par erreur, le test passe quand même car django ne le vérifi pas dans les tests.
    * Les templates peuvent être brisé, il faut les tester.
* Solution, `WebTest`

    ::
    
        class AddUserViewTests(WebTest):
            def test_post_form(self):
                response = self.app.get('/user/add/')
                self.assertEqual(response.status_code, 200)
                
                form = response.forms['user-add-form']
                form['first_name'] = 'first'
                form['last_name'] = 'last'
                
                response = form.submit().follow()
                
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json, {'status': 1, 'message': 'success'})
                self.assertEqual(response.html.find('a', title='login').href, '/login/')
            

Tester l'envoie de email
------------------------

    ::
        from django.core import mail
        
        def test_send_email(self):
            
            