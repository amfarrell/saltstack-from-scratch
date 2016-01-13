import subprocess
import unittest
import yaml
import os
import pytest
setup = pytest.mark.setup
complete = pytest.mark.complete

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

def run_arthur(command):
    return run_remote('arthur', command)

def run_galahad(command):
    return run_remote('galahad', command)

def check_tests_run_from_base_dir():
    wd = os.getcwd()
    if os.path.basename(wd) == PROJECT_NAME:
        return True
    elif PROJECT_NAME in wd:
        while not os.path.basename(wd) == PROJECT_NAME:
            wd = os.path.dirname(wd)
        raise AssertionError("the SaltStack From Scratch tests must be run from {}".format(os.path.abspath(wd)))
    else:
         for node, subdirs, files in os.walk('.'):
             if os.path.basename(node) == PROJECT_NAME:
                 raise AssertionError("the SaltStack From Scratch tests must be run from {}".format(os.path.abspath(node)))
    raise AssertionError("the SaltStack From Scratch tests must be run from the base directory of their git repository.")


class SaltStateTestCase(unittest.TestCase):
    def run_state(self, state_file, target='*', state_id=None):
        if state_id:
            command = "sudo salt '{}' state.sls_id {} {} --output=yaml".format(target, state_id, state_file)
        else:
            command = "sudo salt '{}' state.sls {} --output=yaml".format(target, state_file)
        response = run_arthur(command)
        response_data = yaml.load(response)
        tracebacks = []
        failures = []
        if isinstance(response_data, str):
            raise AssertionError("The result of running {} was\n{}.".format(command, response_data))
        for minion, state_results in response_data.items():
            if isinstance(state_results, str):
                tracebacks.append((minion, state_results))
                continue
            if isinstance(state_results, list):
                failures.append((minion, "", state_results))
                continue
            for state_id, results in state_results.items():
                if results['result'] is not True:
                    failures.append((minion, state_id, results))
        if tracebacks:
            message = "The following minions had tracebacks:\n"
            for traceback in tracebacks:
                message += "{}:\n{}\n\n".format(*traceback)
            raise AssertionError(message)
        if failures:
            message = "The following salt states failed:\n"
            for failure in failures:
                message += "On {}, the state {} failed with\n {}\n".format(*failure)
                print(failure[2]['comment'])
            raise AssertionError(message)
        return response_data
