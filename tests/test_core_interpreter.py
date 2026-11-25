import unittest

from pycparser import c_lexer

from pycparser import c_parser, c_generator, c_ast

from pycparser import yacctab

CLexer = c_lexer.CLexer


from c_repl.utility.logger import info, debug

# from c_repl.core import s2s
from c_repl.core.s2s import _GCC_Utility, C_Interpreter, comment_remover, add_semi, compare_source, r_ws

# alias
STR_EMPTY = ''
_gccu = _GCC_Utility


# TODO: https://docs.python.org/3/library/unittest.html
class Test(unittest.TestCase):
    def setUp(self):
        self.init()

    def init(self):
        self.c_interpreter = C_Interpreter()


    def test_0(self):
        c_interpreter = self.c_interpreter


        # TODO: TEST C_Interpreter.compile

        c_interpreter.interpret('''
        int i = 1;
        void f(int i) {
            printf("f() %d\\n", i);
        }
''')
        c_interpreter.interpret('''
        f(10);
        printf("Asserting i == 1 ...");
        assert(i == 1);
''')

       # c_interpreter.interpret('''

       # int a = 1115;

       #  printf("A INITALIZED %d\\n", a);
       # ''')

       # c_interpreter.interpret('''
       # printf("A LOOKUP %d\\n", a);
       # ''')
