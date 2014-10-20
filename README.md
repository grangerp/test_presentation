# test_presentation

w.illi.am amazing project


## Setup developement environement

* mkvirtualenv test_presentation (need virtualenv and virtualenvwrapper)

* pip install tox

* git clone git@github.com:williamdev/test_presentation.git 

* cd test_presentation

* pip install -r requirements/developments.txt

* cp test_presentation/settings/local_settings.py.sample test_presentation/settings/local_settings.py

* Create a new postgres user test_presentation with its database test_presentation
(This new user has to able to CREATE / DROP database for testing)

* python manage.py syncdb --migrate

### Without Grunt

* python manage.py runserver

### With Grunt

* npm install

* grunt serve


* check at: http://127.0.0.1:8000/admin

* tox