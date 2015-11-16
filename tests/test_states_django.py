from test_utils import run_frodo, run_samwise, SaltStateTestCase
import shutil
import os.path
import unittest
import requests
import yaml

class TestSamwiseRepoCloned(SaltStateTestCase):

    def debian_package_installed(self, packagename):
        return not 'no packages found matching {}'.format(packagename) in \
                run_samwise("dpkg-query -l '{}'".format(packagename))

    def test_virtualenv_exists(self):
        if self.debian_package_installed('python-virtualenv'):
            run_samwise('sudo apt-get remove python-virtualenv')
        if os.path.exists('samwise_vagrant/example-venv/bin/'):
            run_samwise('rm -rf /vagrant/example-venv')
            #remove directory from guest because 
            #removing from host triggers a virtualbox bug
        state_response_data = self.run_state(state_file='django', target='samwise')
        assert self.debian_package_installed('python-virtualenv')
        assert os.path.exists('samwise_vagrant/example-venv/bin/')
        assert os.path.exists('samwise_vagrant/example-venv/bin/django-admin.py')
        assert os.path.exists('samwise_vagrant/example-venv/bin/gunicorn')

    def test_git_repo_exists(self):
        if os.path.exists('samwise_vagrant/django-example'):
            run_samwise('rm -rf /vagrant/django-example')
            #remove directory from guest because 
            #removing from host triggers a virtualbox bug
        if self.debian_package_installed('git'):
            run_samwise('sudo apt-get remove git')
        state_response_data = self.run_state(state_file='django', target='samwise')
        assert self.debian_package_installed('git')
        assert os.path.exists('samwise_vagrant/django-example/manage.py'), \
            "The app's git repository has not been cloned."

    def test_gunicorn(self):
        run_samwise('sudo service django-example stop')
        run_samwise('sudo rm -f /etc/init/django-example.conf')
        state_response_data = self.run_state(state_file='django', target='samwise')
        # You can run individual states and their dependencies from a file
        # using `salt '*' state.sls_id gunicorn-upstart-file django`. But, one
        # word of warning, this will break if you try to run a state such as
        # git.latest and git is not already installed.
        assert 'django-example.conf' in run_samwise('sudo ls /etc/init/django-example.conf')
        assert 'syntax ok' in run_samwise('sudo init-checkconf /etc/init/django-example.conf')
        assert 'django-example.log' in run_samwise('sudo ls /var/log/upstart/django-example.log')
        assert 'django-example start/running' in run_samwise('sudo service django-example status')
        assert 'Django' in requests.get('http://0.0.0.0:8082').text
