from os.path import join
import re

from translator import Python
from utils import Docker


class Executor:

    def __init__(self, lang: str, code: str, inputs_count: int = 0, with_template: bool = False):
        self.lang = lang
        self.code = code
        self.with_template = with_template

        if lang == 'py':
            self.translator = Python(code)
        else:
            raise ValueError(f'Language {lang} not found')

        self.translator.save(inputs_count, with_template)

    def run(self, docker: Docker, input_data: list) -> list | tuple:
        if self.with_template:
            return self.__run_with_template(docker, input_data)
        else:
            return self.__run(docker, input_data)

    def __run(self, docker: Docker, input_data: list) -> list:
        code_path = 'python/' + self.translator.filename + '.py'
        responses = [docker.run(code_path, data.encode('utf-8')) for data in input_data]

        return responses

    def __run_with_template(self, docker: Docker, input_data: list) -> tuple:
        input_data = '\n'.join(input_data).encode('utf-8')

        code_path = 'python/' + self.translator.filename + '.py'
        response = docker.run(code_path, input_data)
        return response

    def __del__(self):
        self.translator.delete()
