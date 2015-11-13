import subprocess
import unittest
import yaml

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

class SaltStateTestCase(unittest.TestCase):
    def run_state(self, state_file, target='*', state_id=None):
        if state_id:
            response = run_frodo("sudo salt '{}' state.sls_id {} {} --output=yaml".format(target, state_id, state_file))
        else:
            response = run_frodo("sudo salt '{}' state.sls {} --output=yaml".format(target, state_file))
        response_data = yaml.load(response)
        tracebacks = []
        failures = []
        for minion, state_results in response_data.items():
            if isinstance(state_results, str):
                tracebacks.append((minion, state_results))
                continue
            if isinstance(state_results, list):
                failures.append((minion, "", state_results))
                continue
            for state_id, results in state_results.items():
                if results['result'] is not True:
                    failures.append((minion, state_id, yaml.results))
        if tracebacks:
            message = "The following minions had tracebacks:\n"
            for traceback in tracebacks:
                message += "{}:\n{}\n\n".format(*traceback)
            raise AssertionError(message)
        if failures:
            message = "The following salt states failed:\n"
            for failure in failures:
                message += "On {}, the state {} failed with\n {}\n".format(*failure)
            raise AssertionError(message)
        return response_data
