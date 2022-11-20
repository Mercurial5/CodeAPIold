from subprocess import Popen, PIPE, TimeoutExpired
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

        command = f'docker run -i --memory 64M --oom-kill-disable -dv {self.path_to_host_volume}:' \
                  f'{self.path_to_container_volume} {image}'

        process = Popen(command, shell=True, stdout=PIPE)
        self.container_id = process.stdout.read().decode('utf-8').strip()

    def run(self, filename: str, input_data: bytes, timeout: int = 2) -> tuple:
        """
        :param filename: str
        :param input_data: str
        :param timeout: int

        :return: str
        """

        if self.lang == 'py':
            execution_command = 'python'
        else:
            raise ValueError

        path_to_code = path.join(self.path_to_container_volume, filename)
        command = f'docker exec -i {self.container_id} {execution_command} {path_to_code}'

        process = Popen(command, shell=True, stderr=PIPE, stdin=PIPE, stdout=PIPE)
        try:
            response = process.communicate(input_data, timeout)
        except TimeoutExpired:
            return '', 'Timeout', None
        print(response)

        stdout, stderr = response[0].decode('utf-8'), response[1].decode('utf-8')

        if 'python' in stderr:
            return stdout, stderr, process.args

        return stdout, stderr, None

    def __del__(self):
        command = f'docker rm -f {self.container_id}'
        # Popen(command, shell=True, stderr=PIPE, stdin=PIPE, stdout=PIPE)
