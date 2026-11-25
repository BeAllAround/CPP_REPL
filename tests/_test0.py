import os

from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.lexers import PygmentsLexer


from prompt_toolkit.styles import BaseStyle, DynamicStyle

from pygments.lexers.c_cpp import CppLexer

from prompt_toolkit.key_binding import KeyBindings

from prompt_toolkit.application import run_in_terminal


import pygments.styles
from pygments.styles import get_style_by_name
from pygments import highlight
from pygments.formatters import Terminal256Formatter, TerminalTrueColorFormatter
from pygments.formatters import TerminalFormatter

# print(list(pygments.styles.get_all_styles()))


# print(list(pygments.formatters.get_all_formatters()))


bindings = KeyBindings()

indent_sep = '  '

def get_intentation(current_buffer):
    bracket_c = 0

    for c in current_buffer.text:
        if(c == '{'):
            bracket_c += 1
        elif(c == '}'):
            bracket_c -= 1


    if(bracket_c == 0 or bracket_c < 0):
        current_buffer.validate_and_handle()
        return None

    
    indent = (indent_sep * bracket_c)

    return indent

@bindings.add("escape", "enter")  # Alt+Enter
def _(event):
    current_buffer = event.current_buffer

    current_buffer.insert_text("\n" + indent_sep)

@bindings.add("enter")
def _(event):
    current_buffer = event.current_buffer
    # print('current_buffer:', current_buffer)
    # print('current_buffer text:', current_buffer.text)

    # See: https://github.com/ipython/ipython/blob/79f313ab453f82d231ba7ac2c1e5211e71d612ce/IPython/terminal/shortcuts/__init__.py#L408


    indent = get_intentation(current_buffer)

    if(indent == None):
        return

    current_buffer.insert_text("\n" + indent)

    # TODO LOGIC: IF CODE CLOSED BRACKETS

    return


def prompt_continuation(width, line_number, is_soft_wrap):
    # print('prompt_continuation:', width, line_number, is_soft_wrap)
    # print(line_number)
    return "." * width
    # Or: return [("", "


# TODO: Custom CLexer if needed
# See and re-implement: https://github.com/pygments/pygments/blob/0328cfaf1d953b3a0c7eb0ec0efd363deb2f9d51/pygments/lexers/c_cpp.py#L270


'''
# TODO Proper Prompt Session
# 3.5.2 The PromptSession object

session = PromptSession(
    lexer=PygmentsLexer(CLexer),
    style=get_style_by_name('monokai') # Or any other Pygments style
)
'''

from prompt_toolkit.styles.pygments import style_from_pygments_cls



def my_input(message):
    return prompt(message,
                  lexer=PygmentsLexer(CppLexer),
                  multiline=True,
                  # style=DynamicStyle(),
                  # vi_mode = True,
                  style = style_from_pygments_cls(get_style_by_name('vim')),
                  key_bindings=bindings,
                  prompt_continuation=prompt_continuation)


def print_Formatted_C_Code(_code):

    # _code = '''
    # void d() {};
    # struct {};
    # '''

    # NOTE: Seems like the only the TruColorFormatter is accurate to the default input formatting of the prompt function
    result = highlight(_code, CppLexer(), TerminalTrueColorFormatter(style="monokai"))

    print(result)


from prompt_toolkit import PromptSession
from prompt_toolkit.styles import AdjustBrightnessStyleTransformation


from cpp_repl.core.interpret import CppInterpreter


import subprocess

import shutil

from datetime import datetime

def get_clang_version():
    clang = shutil.which("clang") or shutil.which("clang++")
    if not clang:
        return None

    try:
        out = subprocess.check_output(
            [clang, "--version"],
            text=True,
            stderr=subprocess.STDOUT,
        )
        # First line is usually enough, e.g. "Ubuntu clang version 18.1.3 ..."
        return out.splitlines()[0]
    except subprocess.CalledProcessError:
        return None


def get_llvm_package_version():
    try:
        out = subprocess.check_output(
            ["dpkg", "-l", "clang"], text=True
        )
        for line in out.splitlines():
            if line.startswith("ii"):
                return line.split()[2]   # package version
    except subprocess.CalledProcessError:
        return None


def get_timestamp():
    return datetime.now().strftime("%b %d %Y, %H:%M:%S")



if __name__ == '__main__':
    print(get_timestamp(), 'LLVM[' + get_llvm_package_version() + ']', '[Clang' + get_clang_version() + ']')
    print('Current Working Directory:', os.getcwd())

    print_Formatted_C_Code('''
// Welcome to BeAllAround/CPP_REPL !

void code_CPlusPlus_at_runtime() { std::cout << "NOW!" << std::endl; }
''')

    session = PromptSession(
        lexer=PygmentsLexer(CppLexer),
        multiline=True,
        style = style_from_pygments_cls(get_style_by_name('vim')),
        style_transformation=AdjustBrightnessStyleTransformation(
            min_brightness=0.5,  # Ensures dark text is raised to at least 50% brightness
            max_brightness=1.0),
        key_bindings=bindings,
        prompt_continuation=prompt_continuation
    )
    # print(CLexer)

    cpp_interpreter = CppInterpreter()

    cpp_interpreter.setUp()

    while True:
        cpp_source = session.prompt("> ")

        # print('cpp_source', cpp_source)

        cpp_interpreter.interpret(cpp_source)


        # print(eval_app, dir(eval_app))


        # c_source = my_input('> ')
        # cpp_interpreter.interpret(c_source)

    # print('_out:', [_out])

    # print_Formatted_C_Code(_out)
