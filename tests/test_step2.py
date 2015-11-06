import subprocess
import os
import re

PROJECT_NAME = 'saltmarsh'

def run(command):
    try:
        return subprocess.check_output(command, universal_newlines=True)
    except subprocess.CalledProcessError as err:
        return err.output

def run_remote(boxname, command):
    if not isinstance(command, str):
        command = ' '.join(command)
    return run(['vagrant','ssh', boxname, '--command', "{}".format(command)])

def run_frodo(command):
    return run_remote('frodo', command)

def run_samwise(command):
    return run_remote('samwise', command)


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

def test_single_box_not_running():
    global_status = run(['vagrant', 'global-status'])
    assert 'default virtualbox' not in global_status, "the single box created in step 1 is still runnning. remove it with the `vagrant destroy` command."

def test_double_boxes_running():
    check_tests_run_from_base_dir()
    global_status = run(['vagrant', 'global-status'])
    assert "samwise virtualbox running {}".format(os.getcwd()) in global_status
    assert "frodo   virtualbox running {}".format(os.getcwd()) in global_status
    assert os.path.exists('frodo_vagrant')
    assert os.path.exists('samwise_vagrant')

def test_hostmanager_installed():
    plugins = run(['vagrant', 'plugin', 'list'])
    assert 'vagrant-hostmanager' in plugins

def test_samwise_can_ping_frodo():
    assert 'unknown host' not in run_samwise('ping -c 1 frodo'), \
        "samwise cannot ping frodo"
