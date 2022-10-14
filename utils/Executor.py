from subprocess import TimeoutExpired

from translator import Python


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

    def run(self, input_data: str):
        process = self.translator.run()

        try:
            response = process.communicate(input_data.encode('utf-8'), self.timeout)
        except TimeoutExpired:
            return dict(status=False, reason='Timeout')

        stdout, stderr = response[0].decode('utf-8'), response[1].decode('utf-8')

        if stderr:
            return dict(status=False, reason='Runtime Error', log=stderr)

        return dict(status=True, result=stdout)

    def __del__(self):
        self.translator.delete()


