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
