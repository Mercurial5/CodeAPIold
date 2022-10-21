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
