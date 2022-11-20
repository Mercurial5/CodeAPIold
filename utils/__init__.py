from utils.Docker import Docker
from utils.Executor import Executor


def check(code: str, lang: str, input: str, output: str, io_count: str, io_tuple_count: str):
    try:
        io_count = int(io_count)
        io_tuple_count = int(io_tuple_count)
    except ValueError:
        return dict(status=False, reason='ValueError', description='->' + io_count + ' ' + io_tuple_count + '<- is not an integer value!')

    executor = Executor(lang, code, 100, io_count)

    i, o = executor.parse_io(input, output)

    stdout, stderr, command = executor.run(i)

    if stderr == 1:
        return dict(status=False, reason='Input timeout')

    if None in [stdout]:
        return dict(status=False, reason='IOError')
    if None in [i, o]:
        return dict(status=False, reason='Server IOError')

    if stderr:
        if command is not None:
            return dict(status=False, reason='Docker error', description=stderr, command=command)
        stdout = stdout.split('TestCase\n')
        stdout.pop(-1)
        return dict(status=False, reason='Runtime error', description=stderr, case=len(stdout))

    stdout = {idx: ele for idx, ele in
           enumerate(stdout.split('TestCase\n'))}

    for j in range(len(o)):
        if j >= len(o):
            return dict(status=False, reason='Few outputs', case=j + 1)
        if stdout.get(j) != o[j]:
            return dict(status=False, reason='Wrong answer', case=j + 1)

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
