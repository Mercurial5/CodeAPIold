from utils.Docker import Docker
from utils.Executor import Executor


def check(code: str, lang: str, inputs: list, outputs: list):
    executor = Executor(lang, code, 100, len(inputs))

    stdout, stderr, command = executor.run(inputs)

    if stderr == 1:
        return dict(status=False, reason='Input timeout')

    if None in [stdout]:
        return dict(status=False, reason='IOError')
    if None in [inputs, outputs]:
        return dict(status=False, reason='Server IOError')

    if stderr:
        if command is not None:
            return dict(status=False, reason='Docker error', description=stderr, command=command)
        stdout = stdout.split('TestCase\n')
        stdout.pop(-1)
        return dict(status=False, reason='Runtime error', description=stderr, case=len(stdout))

    stdout = [output.strip() for output in stdout.split('TestCase\n')][:-1]

    for index, output in enumerate(outputs):
        if stdout[index] != output:
            return dict(status=False, reason='Wrong answer', case=index + 1)

    return dict(status=True, reason='Accepted')
