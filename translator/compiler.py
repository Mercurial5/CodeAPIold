from translator import Translator

from abc import abstractmethod


class Compiler(Translator):
    """
    Compiler - class which is derived from Translator. All languages
    which need to compile before run should be inherited from this class.
    """

    @abstractmethod
    def compile(self):
        pass
