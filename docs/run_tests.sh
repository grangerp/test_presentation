BUILD_PATH='dummy'

rm -Rf $BUILD_PATH
django-admin.py startproject --template=. --extension=py,ini,md,rst $BUILD_PATH
cp $BUILD_PATH/dummy/settings/local_settings.py.sample $BUILD_PATH/dummy/settings/local_settings.py
cd $BUILD_PATH
tox 
tox -e reports
tox -e docs