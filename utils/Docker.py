from subprocess import Popen, PIPE
from ast import literal_eval
from os import getenv, path


class Docker:

    def __init__(self, lang: str):
        """
        lang - programming language

        :param lang: str
        """
        self.container_id = None
        self.path_to_host_volume = getenv('path_to_host_volume')
        self.path_to_container_volume = getenv('path_to_container_volume')
        self.images: dict = literal_eval(getenv('images'))
        self.lang = lang

    def start_container(self):
        image = self.images[self.lang]

        command = f'docker run -i -dv {self.path_to_host_volume}:{self.path_to_container_volume}' \
                  f' -m90M --memory-swap=90M --kernel-memory=10M {image}'

        process = Popen(command, shell=True, stdout=PIPE)
        self.container_id = process.stdout.read().decode('utf-8').strip()

    def run(self, filename: str, input_data: bytes, timeout: int = 2) -> tuple:
        """
        :param container_id: str
        :param filename: str
        :param input_data: str

        :return: str
        """

        if self.lang == 'py':
            execution_command = 'python'
        else:
            raise ValueError

        path_to_code = path.join(self.path_to_container_volume, filename)
        command = f'docker exec -i {self.container_id} {execution_command} {path_to_code}'

        process = Popen(command, shell=True, stderr=PIPE, stdin=PIPE, stdout=PIPE)

        response = process.communicate(input_data, timeout)

        stdout, stderr = response[0].decode('utf-8'), response[1].decode('utf-8')

        if 'python' in stderr:
            return stdout, stderr, process.args

        return stdout, stderr, None

    def __del__(self):
        command = f'docker rm --force {self.container_id}'
        process = Popen(command, shell=True, stderr=PIPE, stdin=PIPE, stdout=PIPE)
