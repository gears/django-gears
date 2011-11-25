from .base import ExecEngine


class CoffeeScriptEngine(ExecEngine):

    params = ['--print', '--stdio']
    result_mimetype = 'application/javascript'
