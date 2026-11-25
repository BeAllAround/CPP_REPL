import ctypes
import os

from ctypes import cdll



# cmake . && make && python3 verify_main.py
# valgrind -s python3 main.py


# See: https://docs.python.org/3/library/ctypes.html#fundamental-data-types
def py_str_to_c_str(s):
    # create a buffer containing a NUL terminated string
    c_char = ctypes.create_string_buffer(bytes(s, 'utf-8'))

    # print(ctypes.sizeof(c_char), c_char.raw, c_char.value, len(c_char.value))

    # c_str = ctypes.cast(c_char, ctypes.c_char_p) # char* (NUL terminated)

    # print(c_str)

    return c_char


if __name__ == '__main__':
    # print(cdll)

    # See: https://docs.python.org/3/library/ctypes.html
    # eval_app = cdll.LoadLibrary('./libfunc_dynamic.so', mode=os.RTLD_GLOBAL)
    eval_app = ctypes.CDLL('./libfunc_dynamic.so', mode=os.RTLD_GLOBAL)

    print(eval_app, dir(eval_app))

    setup_ok = eval_app.setUp()

    assert setup_ok == 0


    cpp_source = "int i = 1020; std::cout << i << std::endl;"
    # cpp_source = "int i = 1;"

    output = eval_app.parseAndExecute(py_str_to_c_str(cpp_source))

    print('output:', output)

    # eval_app.cleanUp()

