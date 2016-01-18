from __future__ import absolute_import

import subprocess
import os
import re
from tests.test_utils import run, run_galahad, run_arthur, setup, complete

@complete
def test_ag_installed_on_galahad():
    assert 'ok installed' in run_galahad('dpkg -s silversearcher-ag | grep Status'), \
        "You must ensure that silversearcher-ag is installed on galahad."

@complete
def test_ag_installed_on_arthur():
    assert 'ok installed' in run_arthur('dpkg -s silversearcher-ag | grep Status'), \
        "You must ensure that silversearcher-ag is installed on arthur."

@complete
def test_salt_states_in_vagrant():
    assert '/vagrant/salt' in run_arthur('grep ^file_roots -A 2 /etc/salt/master'), \
        "You must set the file_roots:\nbase: to '/vagrant/salt' in /etc/salt/master."
    assert os.path.exists('arthur_vagrant/salt/ag.sls'), \
        "You must put an sls file named ag.sls for silversearcher-ag in {}".format(os.path.abspath('./salt/ag.sls'))

@complete
def test_sls_written():
    with open('arthur_vagrant/salt/ag.sls') as f:
        data = yaml.load(f)
        correct_data = {'install-silversearcher': {'pkg.installed': [{'name': 'silversearcher-ag'}]}}
        assert data == correct_data, \
            "The data in ag.sls must match \n{}. It is currently\n{}".format(
                    yaml.dump(correct_data), yaml.dump(data)
            )
