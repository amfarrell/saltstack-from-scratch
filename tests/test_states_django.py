from __future__ import absolute_import

import os.path
import shutil
import subprocess
import unittest
import requests
import re
import yaml
from tests.test_utils import run, run_galahad, run_arthur, \
    SaltStateTestCase, setup, complete

@setup
class TestGalahadDjangoExample(SaltStateTestCase):

    def debian_package_installed(self, packagename):
        return not 'no packages found matching {}'.format(packagename) in \
                run_galahad("dpkg-query -l '{}'".format(packagename))

    def test_virtualenv_exists(self):
        if self.debian_package_installed('python-virtualenv'):
            run_galahad('sudo apt-get remove python-virtualenv')
        if os.path.exists('galahad_vagrant/example-venv/bin/'):
            run_galahad('rm -rf /vagrant/example-venv')
            #remove directory from guest because
            #removing from host triggers a virtualbox bug
        state_response_data = self.run_state(state_file='django', target='galahad')
        assert self.debian_package_installed('python-virtualenv')
        assert os.path.exists('galahad_vagrant/example-venv/bin/')
        assert os.path.exists('galahad_vagrant/example-venv/bin/django-admin.py')
        assert os.path.exists('galahad_vagrant/example-venv/bin/gunicorn')

    def test_git_repo_exists(self):
        if os.path.exists('galahad_vagrant/django-example'):
            run_galahad('rm -rf /vagrant/django-example')
            #remove directory from guest because
            #removing from host triggers a virtualbox bug
        if self.debian_package_installed('git'):
            run_galahad('sudo apt-get remove git')
        state_response_data = self.run_state(state_file='django', target='galahad')
        assert self.debian_package_installed('git')
        assert os.path.exists('galahad_vagrant/django-example/manage.py'), \
            "The app's git repository has not been cloned."

    def test_gunicorn(self):
        run_galahad('sudo service django-example stop')
        run_galahad('sudo rm -f /etc/init/django-example.conf')
        state_response_data = self.run_state(state_file='django', target='galahad')
        # You can run individual states and their dependencies from a file
        # using `salt '*' state.sls_id gunicorn-upstart-file django`. But, one
        # word of warning, this will break if you try to run a state such as
        # git.latest and git is not already installed.
        assert 'django-example.conf' in run_galahad('sudo ls /etc/init/django-example.conf')
        assert 'syntax ok' in run_galahad('sudo init-checkconf /etc/init/django-example.conf')
        assert 'django-example.log' in run_galahad('sudo ls /var/log/upstart/django-example.log')
        assert 'django-example start/running' in run_galahad('sudo service django-example status')
        assert 'Django' in requests.get('http://0.0.0.0:8082').text

    def test_nginx_running(self):
        if self.debian_package_installed('nginx'):
            run_galahad('sudo apt-get remove nginx --purge')
        state_response_data = self.run_state(state_file = 'nginx', target='galahad')
        assert 'master process' in run_galahad('sudo ps aux | grep nginx')

    def test_nginx_restarts_on_conf_change(self):
        self.run_state(state_file = 'nginx', target='galahad')
        run_arthur("echo '  ' >> {}".format(self.state_path("nginx-default.conf")))
        state_response_data = self.run_state(state_file = 'nginx', target='galahad')
        assert 'restarted' in state_response_data['galahad']['service_|-nginx-running_|-nginx_|-running']['comment']
        run_arthur("sed -i '$ d' {}".format(self.state_path("nginx-default.conf")))

    def test_nginx_proxying_port_8080(self):
        if self.debian_package_installed('nginx'):
            run_galahad('sudo apt-get remove nginx --purge')
        state_response_data = self.run_state(state_file = 'django', target='galahad')
        state_response_data = self.run_state(state_file = 'nginx', target='galahad')
        assert '8080' in run_galahad('cat /etc/nginx/sites-enabled/default')
        assert 'Django' in requests.get('http://0.0.0.0:8002').text
        #TODO
        pass
