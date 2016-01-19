from __future__ import absolute_import

import subprocess
import os
import re
from tests.test_utils import check_tests_run_from_base_dir, \
    run, run_galahad, run_arthur, setup, complete
from distutils.version import LooseVersion

@setup
def test_start():
    """
    Check that the student is in the base directory.
    """
    assert check_tests_run_from_base_dir()

@setup
def test_virtualbox_version():
    """
    Shell out to vboxmanage to get the version of virtualbox currently installed.

    TODO: Check to see if this works on windows.
    TODO: Make this less brittle with respect to versions of virtualbox.
    """
    correct_version = LooseVersion('5.0.6')
    try:
        version = LooseVersion(run(['vboxmanage','--version']))
    except FileNotFoundError:
        assert False, "Virtualbox is not yet installed."
    assert correct_version <= version, "Your version of virtualbox is {}.\n \
        This may not work with the rest of the tutorial,\n \
        which is written for Virtualbox {}.".format(version, correct_version)

@setup
def test_vagrant_version():
    correct_version = LooseVersion('1.7.4')
    try:
        version = LooseVersion(run(['vagrant','--version']))
    except FileNotFoundError:
        assert False, "Vagrant is not yet installed."
    assert correct_version in version, "Your version of vagrant is {}.\n \
        This may not work with the rest of the tutorial,\n \
        which is written for vagrant {}.".format(version, correct_version)

@setup
def test_vagrantfile_exists():
    assert os.path.exists('Vagrantfile'), \
        "You must create a vagrantfile at {}".format(os.path.abspath('Vagrantfile'))

@setup
def test_double_boxes_running():
    check_tests_run_from_base_dir()
    global_status = run(['vagrant', 'global-status'])
    arthur_running = re.compile("[0-9a-fA-F]{7}\s*arthur\s*virtualbox\s*running\s"+"{}".format(os.getcwd()))
    galahad_running = re.compile("[0-9a-fA-F]{7}\s*galahad\s*virtualbox\s*running\s"+"{}".format(os.getcwd()))
    assert arthur_running.search(global_status)
    assert galahad_running.search(global_status)

@setup
def test_hostmanager_installed():
    plugins = run(['vagrant', 'plugin', 'list'])
    assert 'vagrant-hostmanager' in plugins

@setup
def test_galahad_can_ping_arthur():
    ping_results = run_galahad('ping -c 1 arthur')
    assert 'unknown host' not in ping_results, \
        "galahad does not know arthur's IP address"
    assert 'Unreachable' not in ping_results, \
        "arthur is not responding to ping"
    assert '1 packets transmitted' in ping_results
