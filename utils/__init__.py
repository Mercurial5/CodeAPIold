from utils.exceptions import SecurityError
from utils.Executor import Executor


def check(code: str, lang: str, io: list):
    try:
        executor = Executor(lang, code)
    except SecurityError as e:
        return dict(status=False, reason=str(e))

    for index, io_item in enumerate(io, 1):
        response = executor.run(io_item.get('input', ''))
        if not response['status']:
            return response.update(case=index)

        if response['result'].strip() != io_item['output']:
            return dict(status=False, reason='Wrong answer', case=index)

    return dict(status=True)
