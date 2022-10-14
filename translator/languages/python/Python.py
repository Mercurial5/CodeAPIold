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

    def run(self) -> Popen:
        commands = [sys.executable, self.path_to_file]
        process = Popen(commands, stderr=PIPE, stdin=PIPE, stdout=PIPE)

        return process
