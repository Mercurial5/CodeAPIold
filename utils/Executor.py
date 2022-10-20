from translator import Python

from utils import Docker


class Executor:

    def __init__(self, lang: str, code: str, timeout: int = 2):
        self.lang = lang
        self.code = code
        self.timeout = timeout

        if lang == 'py':
            self.translator = Python(code)
        else:
            raise ValueError(f'Language {lang} not found')

        self.translator.save()

    def run(self, input_data: list) -> tuple:
        docker = Docker(self.lang)
        docker.start_container()
        input_data = '\n'.join(input_data).encode('utf-8')
        response = docker.run(self.translator.filename + '.py', input_data)

        return response

    def __del__(self):
        self.translator.delete()
