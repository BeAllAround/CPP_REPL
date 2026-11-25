from ctypes import cdll



if __name__ == '__main__':
    print(cdll)

    # See: https://docs.python.org/3/library/ctypes.html
    eval_app = cdll.LoadLibrary('./eval_app.so')

    print(dir(eval_app))

    assert(eval_app.get_context() == 0) # context == NULL # unset
    eval_app.init()
    assert(eval_app.get_context() != 0)

    for i in range(0, 2): # Make sure that all persistance tests pass in a loop (more than one execution)
        print(eval_app.get_context())
        r = eval_app._eval()
        print('returned', r)


    clean_up_success = eval_app.clean_up()

    print('clean_up_success', clean_up_success)


