from translator import Interpreter

from subprocess import Popen, PIPE
import sys


class Python(Interpreter):

    def __init__(self, code: str):
        """
        Calls Translator constructor, which is creating all needed directories.

        :param code: str
        """
        super().__init__('python', 'py', code)

    def check_security(self) -> dict:
        if 'import' in self.code:
            return dict(status=False, reason='Used banned keyword "import".')

        self.is_secure = True
        return dict(status=True)

    def run(self) -> dict:
        commands = [sys.executable, self.path_to_file]
        program = Popen(commands, stderr=PIPE, stdin=PIPE, stdout=PIPE)
        program.stdin.flush()

        stdout = program.stdout.read().decode('utf-8')
        stderr = program.stderr.read().decode('utf-8')

        if stderr:
            return dict(status=False, error=stderr)

        return dict(status=True, output=stdout)
