from utils.Docker import Docker
from utils.Executor import Executor


def check(code: str, lang: str, input: list, output: list):
    executor = Executor(lang, code)

    stdout, stderr = executor.run(input)

    if stderr:
        # Need to return the test index
        return dict(status=False, reason='Runtime error', description=stderr) #, case=i)

    # Need to return answers splitter character
    stdout = stdout.split('\n')

    for i in range(len(output)):
        if i >= len(stdout):
            return dict(status=False, reason='Few outputs', case=i + 1)

        if stdout[i] != output[i]:
            print(stdout[i], output[i])
            return dict(status=False, reason='Wrong answer', case=i + 1)

    return dict(status=True, reason='Accepted')


"""
    for index, io_item in enumerate(io, 1):
        response = executor.run(io_item.get('input', ''))
        if not response['status']:
            return response.update(case=index)

        if response['result'].strip() != io_item['output']:
            return dict(status=False, reason='Wrong answer', case=index)
    return dict(status=True)
    """
