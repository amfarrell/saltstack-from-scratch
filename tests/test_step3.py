import subprocess
import os
import re
from test_utils import run, run_arthur, run_galahad

PROJECT_NAME = 'saltmarsh'

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

def test_double_boxes_running():
    check_tests_from_base_dir()
    global_status = run(['vagrant', 'global-status'])
    arthur_running = re.compile("[0-9a-fA-F]{7}\s*arthur\s*virtualbox\s*running\s"+"{}".format(os.getcwd()))
    galahad_running = re.compile("[0-9a-fA-F]{7}\s*galahad\s*virtualbox\s*running\s"+"{}".format(os.getcwd()))
    assert arthur_running.search(global_status)
    assert galahad_running.search(global_status)

def test_hostmanager_installed():
    plugins = run(['vagrant', 'plugin', 'list'])
    assert 'vagrant-hostmanager' in plugins

def test_salt_installed_running_on_galahad():
    assert 'saltstack' in run_galahad('grep saltstack /etc/apt/sources.list /etc/apt/sources.list.d/*'), \
        "You must add the saltstack ppa to galahad"
    assert 'ok installed' in run_galahad('dpkg -s salt-minion | grep Status'), \
        "You must install the salt-minion service on galahad"
    assert 'salt-minion start/running' in run_galahad('sudo service salt-minion status'), \
        "The salt-minion is not running on galahad."


def test_galahad_can_ping_arthur():
    assert 'unknown host' not in run_galahad('ping -c 1 arthur'), \
        "galahad cannot ping arthur"

def test_arthur_accepted_minions():
    keys = run_arthur('sudo salt-key -L')
    accepted = keys.split('Denied Keys:')[0].split('Accepted Keys')[1]
    unaccepted = keys.split('Rejected Keys:')[0].split('Unaccepted Keys')[1]
    up_minions = run_arthur('sudo salt-run manage.status').split('up:')[1]
    if 'galahad' not in accepted:
        if 'galahad' not in unaccepted:
            if 'master: arthur' not in run_galahad("grep 'master: arthur' /etc/salt/minion"):
                raise AssertionError("salt-minion on galahad is not configured to point to look for salt-master on the same machine")
            else:
                raise AssertionError("salt-minion on galahad needs a `service salt-minions restart`")
        else:
            raise AssertionError("salt-master on arthur needs to accept the key from salt-minon on galahad")
    assert 'galahad' in up_minions, \
        "The salt-master on arthur does not know that the salt-minion on galahad is up"

    assert 'master: arthur' in run_arthur("grep 'master: arthur' /etc/salt/minion"), \
        "salt-minion on arthur is not configured to point to look for salt-master on the same machine"
    if 'arthur' not in accepted:
        if 'arthur' not in unaccepted:
            if 'master: arthur' not in run_arthur("grep 'master: arthur' /etc/salt/minion"):
                raise AssertionError("salt-minion on arthur is not configured to point to look for salt-master on the same machine")
            else:
                raise AssertionError("salt-minion on arthur needs a `service salt-minions restart`")
        else:
            raise AssertionError("salt-master on arthur needs to accept the key from salt-minon on arthur")
    assert 'arthur' in up_minions, \
        "The salt-master on arthur does not know that the salt-minion on arthur is up"

def test_log_files_copied():
    assert os.path.exists('galahad_vagrant/galahad-minion-log'), \
        "use `salt '*' cmd.run` to copy /var/log/salt/minion into /vagrant on both arthur and galahad."
    assert os.path.exists('arthur_vagrant/arthur-minion-log'), \
        "use `salt '*' cmd.run` to copy /var/log/salt/minion into /vagrant on both arthur and galahad."
