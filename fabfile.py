# -*- coding: utf-8 -*-


"""

Deployement structure
---------------------

container folder (uat / staging ...)
  |__ env (python virtual env)
  |__ source code (project source code)
  |__ media (uploaded files)
  |__ static (project static resources served by frontal)
  |__ etc (generated service config files)
  |__ logs (services logs)
  |__ tmp (socket files, not in VCS)

"""

import os
import sys

from fabric.api import env, local, run, cd, put, sudo, lcd, get
from fabric.contrib.files import exists, upload_template
from fabric.contrib.console import confirm
from fabric.context_managers import warn_only
from fab_deploy.crontab import crontab_update


env.git_url = "git@github.com:williamdev/test_presentation.git"
env.bin_python = 'python2.7'
env.project_name = 'test_presentation'

env.tmp_folder = '/tmp'
env.dump_file_name = 'db.sql'
env.local_settings = os.path.join(
    env.project_name, 'settings', 'local_settings.py')
env.run = run
env.sudo = sudo
env.cd = cd
env.server_alias = ''  # add more server names to gninx server_name

###############################################################################
# TARGETS
###############################################################################


def _safe_subdomain(name):
    """
    see RFC 952
    """
    return name.replace('_', '-')


def target(fct):
    """
    Plug target as environment variable set from function name
    """
    def wrapped(*args, **kwargs):
        if not hasattr(env, 'target'):
            env.target = fct.__name__
        return fct(*args, **kwargs)
    return wrapped


def secured(fct):
    """
    Decorator to prompt for confirmation
    """
    def wrapped(*args, **kwargs):
        local('git status')
        if not confirm("Are you sure?", default=False):
            print 'Nothing done'
            sys.exit(-1)
        return fct(*args, **kwargs)
    return wrapped


@target
def staging(name=None, domain='staging.williamdev.com'):
    env.domain = domain
    if name is None:
        env.project_fullname = '%(project_name)s' % env
        settings = '%(target)s.py' % env
    else:
        env.project_fullname = '%(project_name)s' % env + '_%s' % name
        settings = '%(target)s' % env + '_%s.py' % name

    if 'settings_file' not in env:
        env.settings_file = os.path.join(
            env.project_name, 'settings', settings)

    env.db_password = env.project_fullname
    env.dns_name = _safe_subdomain(env.project_fullname)
    env.server_name = '%(dns_name)s.%(domain)s' % env
    env.container_path = os.path.join('/var', 'william', env.dns_name)
    env.media = os.path.join(env.container_path, "media")

    env.user = 'teamdev'
    env.hosts = [
        env.domain,
    ]


@secured
@target
def prod():
    domain = 'FILL ME'
    staging(name=None, domain=domain)
    env.server_name = domain


@target
def dev(name=None):
    env.run = local
    env.cd = lcd
    env.settings_file = os.path.join(
        env.project_name, 'settings', 'staging.py')
    domain = '127.0.0.1'
    staging(name=name, domain=domain)
    env.container_path = os.path.dirname(__file__)
    env.media = os.path.join(env.container_path, "media")
    env.server_name = domain
    env.user = os.getenv('USERNAME')


@target
def vagrant():
    staging()
    env.settings_file = os.path.join(
        env.project_name, 'settings', 'vagrant.py')
    env.user = 'vagrant'
    env.password = 'vagrant'
    env.hosts = [
        '127.0.0.1:2222',
    ]


def _dynamic_env():
    """
    Setup env variable for fabric tasks
    """
    if not getattr(env, 'env_path', None):
        env.env_path = os.path.join(env.container_path, 'env')
    if not getattr(env, 'source_path', None):
        env.source_path = os.path.join(env.container_path, env.project_name)
    env.pip = os.path.join(env.env_path, 'bin', 'pip')
    env.python = os.path.join(env.env_path, 'bin', 'python')


###############################################################################
# TASKS
###############################################################################


def dump_db():
    """
    Copy database in env.dump_file_name
    """
    _dynamic_env()
    dump_data = env.run("PGPASSWORD=%(db_password)s pg_dump -U %(project_fullname)s --clean --no-owner --no-privileges %(project_fullname)s" % env)  # NOQA
    f = open(env.dump_file_name, 'w')
    f.write(dump_data)


def dump_files():
    """
    Copy media files in in ./media
    """
    _dynamic_env()
    get(env.media, '%(path)s')


def dump_data():
    """
    Dump database and media
    """
    dump_db()
    dump_files()


def load_db():
    """
    import dumpfile into database target
    """
    _dynamic_env()
    tmp_file = os.path.join(env.tmp_folder, env.project_fullname)
    data = env.copy()
    data.update({
        'tmp_file': tmp_file,
    })
    put(env.dump_file_name, tmp_file)
    env.run("PGPASSWORD=%(db_password)s psql %(project_fullname)s -U %(project_fullname)s < %(tmp_file)s" % data)  # NOQA
    env.run("rm -f %(tmp_file)s" % data)


def load_files():
    """
    Upload media files on target
    """
    _dynamic_env()
    local_media = os.path.basename(env.media)
    put(local_media, os.path.dirname(env.media))


def load_data():
    """
    Load database and media on target
    """
    load_db()
    load_files()


def db():
    """
    create a db/user considering the deploy target (project_fullname)
    """
    _dynamic_env()
    env.run("""psql template1 -c "CREATE USER %(project_fullname)s WITH ENCRYPTED PASSWORD '%(db_password)s';" """ % env)  # NOQA
    env.run("psql template1 -c 'CREATE DATABASE %(project_fullname)s OWNER %(project_fullname)s;'" % env)  # NOQA


def setup():
    """
    Create container structure if not exists
    Create virtual envirionemen if not existst
    Upload configuration files for services
    """
    _dynamic_env()
    with warn_only():
        env.run("mkdir -p %(container_path)s" % env)
        env.run("mkdir -p %(media)s" % env)
        env.run("mkdir -p %(container_path)s/media/ckeditor" % env)
        env.run("mkdir -p %(container_path)s/static" % env)
        env.run("mkdir -p %(container_path)s/logs" % env)
        env.run("mkdir -p %(container_path)s/etc" % env)
        env.run("mkdir -p %(container_path)s/tmp" % env)
        env.run("mkdir -p %(source_path)s" % env)

        clearsessions = "%(python)s %(source_path)s/manage.py clearsessions" \
            % env
        crontab_update("0 0 */1 * * %s > /dev/null 2>&1" % clearsessions,
                       "clearsessions_%(project_fullname)s" % env)

    if not exists(env.env_path):
        env.run("virtualenv %(env_path)s --python=%(bin_python)s" % env)

    etc_out_folder = "%s/etc" % env.container_path
    env.run("mkdir -p %s" % etc_out_folder)
    etc_in_folder = os.path.join(os.path.dirname(__file__), 'etc')

    for filename in os.listdir(etc_in_folder):
        conf_out = os.path.join(etc_out_folder, filename)
        upload_template(filename,
                        conf_out,
                        template_dir=etc_in_folder,
                        context={'env': env},
                        use_jinja=True)


def _stamp_commit(commit):
    """
    Upload commit number of release
    """
    commit_file = 'commit.txt'
    local('git log -n 1 --pretty=format:"%%H" %s > %s' % (commit, commit_file))
    put(commit_file, '%(container_path)s/static' % env)
    local('rm -f %s' % commit_file)


def deploy(commit='HEAD'):
    """
    Setup container and virtualenv if not exists
    Upload configuration files for services
    Reload services
    """
    _dynamic_env()
    setup()
    archive_name = 'build.tar'
    local('git archive %s > %s' % (commit, archive_name))
    remote_archive_path = os.path.join(env.source_path, archive_name)
    env.run('rm -Rf %(source_path)s' % env)
    env.run("mkdir -p %(source_path)s" % env)
    put(archive_name, remote_archive_path)
    local('rm -f %s' % archive_name)
    _stamp_commit(commit)
    with env.cd(env.source_path):
        env.run('tar xf %s' % archive_name)
        env.run('rm -f %s' % archive_name)
        env.run('cp %(settings_file)s %(local_settings)s' % env)
        env.run('%(pip)s install -r requirements.txt' % env)
        env.run('%(python)s manage.py syncdb --noinput' % env)
        env.run('%(python)s manage.py migrate' % env)
        env.run('%(python)s manage.py collectstatic --noinput' % env)
        env.run('%(python)s manage.py compilemessages' % env)
    reload()


def manage(cmd=''):
    """
    Remote plug of django manage.py
    """
    _dynamic_env()
    with env.cd(env.source_path):
        env.run('%s manage.py %s' % (env.python, cmd))


def reload():
    """
    Reload supervisor config
    Restart supervisor website
    Reload nginx config (without restart)
    Start nginx
    """
    _dynamic_env()
    env.sudo('supervisorctl reread', shell=False)
    env.sudo('supervisorctl add %(server_name)s' % env, shell=False)
    env.sudo('supervisorctl restart %(server_name)s' % env, shell=False)
    with warn_only():
        env.sudo('nginx', shell=False)
    env.sudo('nginx -s reload', shell=False)