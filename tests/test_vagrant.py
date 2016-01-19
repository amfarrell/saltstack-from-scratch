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

@complete
def test_vagrantfile_exists():
    assert os.path.exists('Vagrantfile'), \
        "You must create a vagrantfile at {}".format(os.path.abspath('Vagrantfile'))

@complete
def test_single_box_running():
    check_tests_run_from_base_dir()
    global_status = run(['vagrant', 'global-status'])
    assert "default virtualbox running {}".format(os.getcwd()) in global_status

@complete
def test_file_created_through_synced_folders():
    assert os.path.exists('synced-file'), "Log in to the vagrant box and create a directory named 'synced-file within /vagrant"
