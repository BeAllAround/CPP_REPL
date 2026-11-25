import ctypes
import os


# See: https://docs.python.org/3/library/ctypes.html#fundamental-data-types
def py_str_to_c_str(s):
    # create a buffer containing a NUL terminated string
    c_char = ctypes.create_string_buffer(bytes(s, 'utf-8'))

    # print(ctypes.sizeof(c_char), c_char.raw, c_char.value, len(c_char.value))

    # c_str = ctypes.cast(c_char, ctypes.c_char_p) # char* (NUL terminated)

    # print(c_str)

    return c_char


class CppInterpreter:
    def __init__(self):
        self.eval_app = ctypes.CDLL('./libfunc_dynamic.so', mode=os.RTLD_GLOBAL)

    def setUp(self):
        setup_ok = self.eval_app.setUp()

        assert setup_ok == 0
    
    def interpret(self, input_str):
        output = self.eval_app.parseAndExecute(py_str_to_c_str(input_str))

        return output

    # TODO: IMPLEMENT
    def cleanUp():
        pass
