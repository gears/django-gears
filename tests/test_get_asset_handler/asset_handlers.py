from gears.compilers import BaseCompiler


class PythonCompiler(BaseCompiler):

    def __call__(self, asset):
        pass


class CompilerWithOptions(BaseCompiler):

    def __init__(self, level):
        self.level = level

    def __call__(self, asset):
        pass


def simple_compiler(asset):
    pass


incorrect_handler = 'incorrect handler'
