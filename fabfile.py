from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['jerickson.me']
env.user = 'ubuntu'

webapp_path = '/var/www/django/sancho'

def test():
    local('./bin/test', capture=False)

def pack():
    local('git archive --format zip master --output=sancho.zip', capture=False)

def prepare_deploy():
    pack()

def deploy_prod_code():
    prepare_deploy()
    
    put('sancho.zip', '/home/ubuntu/')
    run('unzip -o /home/ubuntu/sancho.zip -d %s' % webapp_path)
    
    with cd(webapp_path):
        run('touch bin/django.wsgi')
        run('apache2/bin/restart')
    
    run('rm /ubuntu/sancho.zip')

def deploy_prod():
    prepare_deploy()
    
    put('sancho.zip', '/home/ubuntu/')
    run('unzip -o /home/ubuntu/sancho.zip -d %s' % webapp_path)
    
    with cd(webapp_path):
        run('cp sanchoapp/prod_settings.py sanchoapp/settings.py')
        run('python /var/www/django/sancho/manage.py syncdb --noinput')
        run('python /var/www/django/sancho/manage.py migrate')
        run('touch /var/www/django/sancho/apache/django.wsgi')
        run('sudo service apache2 reload')
    
    run('rm /home/ubuntu/sancho.zip')
