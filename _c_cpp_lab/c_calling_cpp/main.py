import ctypes

from ctypes import cdll



# valgrind -s python3 main.py


# See: https://docs.python.org/3/library/ctypes.html#fundamental-data-types
def py_str_to_c_str(s):
    # create a buffer containing a NUL terminated string
    c_char = ctypes.create_string_buffer(bytes(s, 'utf-8'))

    print(ctypes.sizeof(c_char), c_char.raw, c_char.value, len(c_char.value))

    # c_str = ctypes.cast(c_char, ctypes.c_char_p) # char* (NUL terminated)

    # print(c_str)

    return c_char


if __name__ == '__main__':
    # print(cdll)

    # See: https://docs.python.org/3/library/ctypes.html
    eval_app = cdll.LoadLibrary('./libfunc_dynamic.so')

    print(eval_app, dir(eval_app))

    eval_app.my_init()

    eval_app.my_handle()

    eval_app.method_string(py_str_to_c_str("AAA!!!"));

    eval_app.my_clean_up()

