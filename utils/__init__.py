from utils.Docker import Docker
from utils.Executor import Executor


def check_weak_samples(code: str, lang: str, inputs: list, outputs: list):
    executor = Executor(lang, code)

    docker = Docker(lang)
    docker.start_container()

    responses = executor.run(docker, inputs)

    for index, response in enumerate(responses, start=1):
        stdout, stderr, command = response

        if stderr == 'Timeout':
            return dict(status=False, reason='Time limit', case=index)

        if stdout is None:
            return dict(status=False, reason='IOError')
        if None in [inputs, outputs]:
            return dict(status=False, reason='Server IOError')

        if stderr:
            if command is not None:
                return dict(status=False, reason='Docker error', description=stderr, command=command)
            stdout = stdout.split('TestCase\n')
            stdout.pop(-1)
            return dict(status=False, reason='Runtime error', description=stderr, case=index)

        if outputs[index] != stdout.strip():
            return dict(status=False, reason='Wrong answer', case=index)

    return dict(status=True, reason='Accepted')


def check_strong_samples(code: str, lang: str, inputs: list, outputs: list, case_shift):
    executor = Executor(lang, code, len(inputs), with_template=True)

    docker = Docker(lang)
    docker.start_container()
    stdout, stderr, command = executor.run(docker, inputs)

    if stderr == 1:
        return dict(status=False, reason='Input timeout')

    if stdout is None:
        return dict(status=False, reason='IOError')
    if None in [inputs, outputs]:
        return dict(status=False, reason='Server IOError')

    if stderr:
        if command is not None:
            return dict(status=False, reason='Docker error', description=stderr, command=command)
        stdout = stdout.split('TestCase\n')
        stdout.pop(-1)
        return dict(status=False, reason='Runtime error', description=stderr, case=len(stdout) + case_shift)

    stdout = [output.strip() for output in stdout.split('TestCase\n')][:-1]

    for index, output in enumerate(outputs, start=1):
        if stdout[index] != output:
            return dict(status=False, reason='Wrong answer', case=index + case_shift)

    return dict(status=True, reason='Accepted')
