from abc import ABC, abstractmethod
from uuid import uuid4
import os


class Translator(ABC):
    """
    Translator - base class which represents all the languages.
    Each language can be divided into compiler and interpreter based.

    All languages have their own separate directory, where their code is
    being executed. Those separate directories are stored in `temp` directory.
    """

    def __init__(self, language: str, extension: str, code: str):
        """
        Creates `temp` directory if it does not exist.
        Creates special directory for specific language if it does not exist.
        Generates a random filename for a file where code will be stored.

        :param language: str
        :param extension: str
        :param code: str
        """
        self.language = language
        self.extension = extension
        self.filename = uuid4().hex

        self.code = code

        self.base_directory = os.path.join(os.getcwd(), 'temp')
        if not os.path.exists(self.base_directory):
            os.mkdir(self.base_directory)

        self.language_directory = os.path.join(self.base_directory, language)
        if not os.path.exists(self.language_directory):
            os.mkdir(self.language_directory)

        filename = f'{self.filename}.{self.extension}'
        self.path_to_file = os.path.join(self.language_directory, filename)

    @abstractmethod
    def run(self):
        """
        Runs code and returns process.

        :return: Popen
        """

    def save(self) -> bool:
        """
        Saves code into file.

        This method will create file only if `is_secure` is True.

        Returns `True`, if file was created, and `False`, if file
        was either not secure or was not checked.

        :return: bool
        """

        if not self.is_secure:
            return False

        with open(self.path_to_file, 'w') as file:
            file.write(self.code)

        return True

    def delete(self) -> bool:
        """
        Deletes previously created file.

        Returns `True`, if file was deleted, and `False`, if file
        was not found (means was not created).

        :return: bool
        """
        try:
            os.remove(self.path_to_file)
            return True
        except FileNotFoundError:
            return False
