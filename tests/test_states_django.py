from __future__ import absolute_import

import os.path
import shutil
import subprocess
import unittest
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
