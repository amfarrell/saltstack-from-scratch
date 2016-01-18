import subprocess
import os
import re
import yaml
from test_utils import run, run_arthur, run_galahad

def test_aws_plugin_installed():
    assert 'aws' in run(['vagrant', 'plugin', 'list'])
