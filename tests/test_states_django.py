from test_utils import run_arthur, run_galahad, SaltStateTestCase
import shutil
import os.path
import unittest
import yaml

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
