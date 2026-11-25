

class Logger:
    enabled = True
    _print_enabled = True
    @staticmethod
    def debug(*args):
        Logger.enabled and print(*args)
    @staticmethod
    def info(*args):
        print(*args)

    # NOTE: THAT THESE CALLS IN THE C_Interpreter CODE HAPPEN AT RUNTIME DUE TO THE ENABLED FLAG CHECK SO IT TAKES A HIT AT THE RUNTIME PERFORMANCE. UNFORTENTLY, THERE ARE NO MACROS IN PYTHON THAT WOULD RESOLVE THIS ISSUE.
    # TODO: RESEARCH MORE ON THIS
    @staticmethod
    def _print(*args): # NOTE FOR C_Interpreter DEBUGGING
        Logger._print_enabled and print(*args)

Logger.enabled = False

Logger._print_enabled = False

debug = Logger.debug
info = Logger.info
_print = Logger._print
