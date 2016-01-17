from __future__ import absolute_import

import subprocess
import os
import re
from tests.test_utils import run, run_galahad, run_arthur, setup, complete

@complete
def test_salt_installed_running_on_galahad():
    assert 'saltstack' in run_galahad('grep saltstack /etc/apt/sources.list /etc/apt/sources.list.d/*'), \
        "You must add the saltstack ppa to galahad"
    assert 'ok installed' in run_galahad('dpkg -s salt-minion | grep Status'), \
        "You must install the salt-minion service on galahad"
    assert 'salt-minion start/running' in run_galahad('sudo service salt-minion status'), \
        "The salt-minion is not running on galahad."

@complete
def test_arthur_accepted_minions():
    keys = run_arthur('sudo salt-key -L')
    if not keys:
        raise AssertionError("No keys accepted by salt-master.")
    try:
        accepted = keys.split('Denied Keys:')[0].split('Accepted Keys')[1]
        unaccepted = keys.split('Rejected Keys:')[0].split('Unaccepted Keys')[1]
        up_minions = run_arthur('sudo salt-run manage.status').split('up:')[1]
    except IndexError:
        raise AssertionError("Listing keys on the salt-master shows {}".format(keys))
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

@complete
def test_log_files_copied():
    assert os.path.exists('galahad_vagrant/galahad-minion-log'), \
        "use `salt '*' cmd.run` to copy /var/log/salt/minion into /vagrant on both arthur and galahad."
    assert os.path.exists('arthur_vagrant/arthur-minion-log'), \
        "use `salt '*' cmd.run` to copy /var/log/salt/minion into /vagrant on both arthur and galahad."
