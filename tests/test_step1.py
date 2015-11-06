import subprocess
import os

PROJECT_NAME = 'saltmarsh'

def run(command):
    return subprocess.check_output(command, universal_newlines=True)


def check_tests_run_from_base_dir():
    wd = os.getcwd()
    if os.path.basename(wd) == PROJECT_NAME:
        return True
    elif PROJECT_NAME in wd:
        while not os.path.basename(wd) == 'saltmarsh':
            wd = os.path.dirname(wd)
        raise AssertionError("the SaltStack From Scratch tests must be run from {}".format(os.path.abspath(wd)))
    else:
         for node, subdirs, files in os.walk('.'):
             if os.path.basename(node) == 'saltmarsh':
                 raise AssertionError("the SaltStack From Scratch tests must be run from {}".format(os.path.abspath(node)))
    raise AssertionError("the SaltStack From Scratch tests must be run from the base directory of their git repository.")

def test_virtualbox_version():
    """
    Shell out to vboxmanage to get the version of virtualbox currently installed.

    TODO: Check to see if this works on windows.
    TODO: Make this less brittle with respect to versions of virtualbox.
    """
    correct_version = '5.0.6'
    try:
        version = run(['vboxmanage','--version'])
    except FileNotFoundError:
        assert False, "Virtualbox is not yet installed."
    assert correct_version in version, "Your version of virtualbox is {}.\n \
        This may not work with the rest of the tutorial,\n \
        which is written for Virtualbox {}.".format(version, correct_version)

def test_vagrant_version():
    correct_version = '1.7.4'
    try:
        version = run(['vagrant','--version'])
    except FileNotFoundError:
        assert False, "Vagrant is not yet installed."
    assert correct_version in version, "Your version of vagrant is {}.\n \
        This may not work with the rest of the tutorial,\n \
        which is written for vagrant {}.".format(version, correct_version)

def test_vagrantfile_exists():
    assert os.path.exists('Vagrantfile'), \
        "You must create a vagrantfile at {}".format(os.path.abspath('Vagrantfile'))

def test_single_box_running():
    check_tests_run_from_base_dir()
    global_status = run(['vagrant', 'global-status'])
    assert "default virtualbox running {}".format(os.getcwd()) in global_status


def test_file_created_through_synced_folders():
    assert os.path.exists('synced-file'), "Log in to the vagrant box and create a directory named 'synced-file within /vagrant"
