import subprocess

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
