from os.path import join
import re

from translator import Python
from utils import Docker


class Executor:

    def __init__(self, lang: str, code: str, timeout: int = 2, io_count: int = 0):
        self.lang = lang
        self.code = code
        self.timeout = timeout
        self.io_count = io_count

        if lang == 'py':
            self.translator = Python(code)
        else:
            raise ValueError(f'Language {lang} not found')

        self.translator.save(io_count)

    def run(self, input_data: list) -> tuple:
        docker = Docker(self.lang)
        docker.start_container()
        input_data = '\n'.join(input_data).encode('utf-8')

        code_path = 'python/' + self.translator.filename + '.py'
        response = docker.run(code_path, input_data, self.timeout)
        return response

    def parse_io(self, input: str, output: str) -> tuple:
        i = re.split(r'(TestCase\n)', input)
        i.pop(0)
        i = list(filter(('TestCase\n').__ne__, i))

        o = re.split(r'(TestCase\n)', output)
        o.pop(0)
        o = list(filter(('TestCase\n').__ne__, o))

        return i, o

    def __del__(self):
        self.translator.delete()
