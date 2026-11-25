from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.lexers import PygmentsLexer

from pygments.lexers.c_cpp import CLexer

from prompt_toolkit.key_binding import KeyBindings

from prompt_toolkit.application import run_in_terminal

bindings = KeyBindings()

@bindings.add("enter")
def _(event):
    b = event.current_buffer
    # print('current_buffer:', b)

    # See: https://github.com/ipython/ipython/blob/79f313ab453f82d231ba7ac2c1e5211e71d612ce/IPython/terminal/shortcuts/__init__.py#L408
    indent = '  '

    b.insert_text("\n" + indent)

    # b.validate_and_handle()

    return


def prompt_continuation(width, line_number, is_soft_wrap):
    # print('prompt_continuation:', width, line_number, is_soft_wrap)
    # print(line_number)
    return "." * width
    # Or: return [("", "


# TODO: Custom CLexer if needed
# See and re-implement: https://github.com/pygments/pygments/blob/0328cfaf1d953b3a0c7eb0ec0efd363deb2f9d51/pygments/lexers/c_cpp.py#L270
def my_input(message):
    return prompt(message,
                  multiline=True,
                  lexer=PygmentsLexer(CLexer),
                  key_bindings=bindings,
                  prompt_continuation=prompt_continuation)

if __name__ == '__main__':

    print(CLexer)
    
    _out = my_input('> ')

    print('_out:', _out)
