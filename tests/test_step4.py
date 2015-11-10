import subprocess
import os
import re
import yaml
from test_utils import run, run_frodo, run_samwise

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
    check_tests_run_from_base_dir()
    global_status = run(['vagrant', 'global-status'])
    frodo_running = re.compile("[0-9a-fA-F]{7}\s*frodo\s*virtualbox\s*running\s"+"{}".format(os.getcwd()))
    samwise_running = re.compile("[0-9a-fA-F]{7}\s*samwise\s*virtualbox\s*running\s"+"{}".format(os.getcwd()))
    assert frodo_running.search(global_status)
    assert samwise_running.search(global_status)

def test_hostmanager_installed():
    plugins = run(['vagrant', 'plugin', 'list'])
    assert 'vagrant-hostmanager' in plugins

def test_salt_installed_running_on_samwise():
    assert 'saltstack' in run_samwise('grep saltstack /etc/apt/sources.list /etc/apt/sources.list.d/*'), \
        "You must add the saltstack ppa to samwise"
    assert 'ok installed' in run_samwise('dpkg -s salt-minion | grep Status'), \
        "You must install the salt-minion service on samwise"
    assert 'salt-minion start/running' in run_samwise('sudo service salt-minion status'), \
        "The salt-minion is not running on samwise."


def test_samwise_can_ping_frodo():
    assert 'unknown host' not in run_samwise('ping -c 1 frodo'), \
        "samwise cannot ping frodo"

def test_frodo_accepted_minions():
    keys = run_frodo('sudo salt-key -L')
    accepted = keys.split('Denied Keys:')[0].split('Accepted Keys')[1]
    unaccepted = keys.split('Rejected Keys:')[0].split('Unaccepted Keys')[1]
    up_minions = run_frodo('sudo salt-run manage.status').split('up:')[1]
    if 'samwise' not in accepted:
        if 'samwise' not in unaccepted:
            if 'master: frodo' not in run_samwise("grep 'master: frodo' /etc/salt/minion"):
                raise AssertionError("salt-minion on samwise is not configured to point to look for salt-master on the same machine")
            else:
                raise AssertionError("salt-minion on samwise needs a `service salt-minions restart`")
        else:
            raise AssertionError("salt-master on frodo needs to accept the key from salt-minon on samwise")
    assert 'samwise' in up_minions, \
        "The salt-master on frodo does not know that the salt-minion on samwise is up"

    assert 'master: frodo' in run_frodo("grep 'master: frodo' /etc/salt/minion"), \
        "salt-minion on frodo is not configured to point to look for salt-master on the same machine"
    if 'frodo' not in accepted:
        if 'frodo' not in unaccepted:
            if 'master: frodo' not in run_frodo("grep 'master: frodo' /etc/salt/minion"):
                raise AssertionError("salt-minion on frodo is not configured to point to look for salt-master on the same machine")
            else:
                raise AssertionError("salt-minion on frodo needs a `service salt-minions restart`")
        else:
            raise AssertionError("salt-master on frodo needs to accept the key from salt-minon on frodo")
    assert 'frodo' in up_minions, \
        "The salt-master on frodo does not know that the salt-minion on frodo is up"

def test_samwise_loglevel_set():
    assert "info" in run_samwise('grep ^log_level_logfile /etc/salt/minion'), \
        "You must set log_level_logfile to 'info' in /etc/salt/minion on samwise"
    assert 'INFO' in run_samwise("sudo grep '\[INFO *\]' /var/log/salt/minion"), \
        "You must reset the salt-minion on samwise after setting the value of log_level_logfile"

def test_ag_installed():
    assert 'ok installed' in run_samwise('dpkg -s silversearcher-ag | grep Status'), \
        "You must ensure that silversearcher-ag is installed on samwise."

def test_salt_states_in_vagrant():
    assert '/vagrant/salt' in run_frodo('grep ^file_roots -A 2 /etc/salt/master'), \
        "You must set the file_roots:\nbase: to '/vagrant/salt' in /etc/salt/master."
    assert os.path.exists('frodo_vagrant/salt/ag.sls'), \
        "You must put an sls file named ag.sls for silversearcher-ag in {}".format(os.path.abspath('./salt/ag.sls'))

def test_sls_written():
    with open('frodo_vagrant/salt/ag.sls') as f:
        data = yaml.load(f)
        correct_data = {'install-silversearcher': {'pkg.installed': [{'name': 'silversearcher-ag'}]}}
        assert data == correct_data, \
            "The data in ag.sls must match \n{}. It is currently\n{}".format(
                    yaml.dump(correct_data), yaml.dump(data)
            )
