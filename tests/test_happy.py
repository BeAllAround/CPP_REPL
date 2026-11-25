
import inspect

import unittest


from pycparser import c_parser, c_generator, c_ast

from pycparser import yacctab

# from c_repl.core.s2s import comment_remover


STR_EMPTY = ''
# import c_repl.core

# print(c_repl.core)
# c_repl.core.module1.from_module_func()


# TestCase.assertEqual, TestCase.assertTrue, TestCase.assertFalse

def create_node_from_source(_code):
    parser = c_parser.CParser(yacctab=yacctab)
    node_ast = parser.parse(_code, filename='<none>', debug=False) # debug=True

    return node_ast.ext

class VerifyPyCParserFork(unittest.TestCase):
    def test_happy(self):
        # NOTE: the happy test for the proper yacctab being used in order to parse Statement Expression at the external decl level
        # Make sure there are no exceptions raised during the happy test with a few assertions
        # See: https://github.com/BeAllAround/pycparser/blob/main/pycparser/c_parser.py#L559

        # Top Level External Declaration Statements includes the following parsing checks/passes:
        # These should generate the valid AST Nodes with no exceptions raised or conflicts with the grammar
        # STRUCT DECLARATION OK
        # TYPEDEF STRUCT DECLARATION OK
        # BINARY EXPRESSION OK
        # UNARY CAST OK
        # FUNCTION DECLARATION OK
        # DECLARATION OK
        # ASSIGNMENT EXPRESSION OK
        # FUNCTION DEFINITION OK
        # FUNC CALL OK

        _code = '''

        struct _struct {
        };

        typedef struct _struct my_struct;

        1;
        1+1;

        (int*)(d1 + 1);

        ((void*)d1 * 1);

        int* (*dd)(void, void);


        int d;

        d;

        d = 44;

        void func_d() { aaaaa; printf("AA", a); }

        func_d();


        '''

        # _code = comment_remover(_code)

        # void main() {}
        # int d1 = 1;

        generator = c_generator.CGenerator()

        sig = inspect.signature(c_generator.CGenerator.__init__)

        # NOTE: Ensure it is 3 parameters due to the addition of the optional visit_id_func_wrapper parameter
        self.assertTrue(len(sig.parameters) == 3)
        # print(len(sig.parameters), str(sig))

        parser = c_parser.CParser(yacctab=yacctab)
        node_ast = parser.parse(_code, filename='<none>', debug=False) # debug=True

        # NOTE: external_decl: statement check
        # Make sure that it can be turned into a valid node
        self.assertTrue(node_ast != None)
        # Make sure that the C Generation passses
        self.assertTrue(generator.visit(node_ast) != None)

    def test_try_run_01(self):

        _code = '''
            void _func_01() {}
            void _func_02(int*a) {}
        '''

        print('')

        generator = c_generator.CGenerator()

        parser = c_parser.CParser(yacctab=yacctab)
        node_ast = parser.parse(_code, filename='<none>', debug=False) # debug=True

        # TODO: Cloning a node
        # At the moment, we could combine visit:->str and parse
        for _node in node_ast.ext:
            # It actually works: https://github.com/BeAllAround/pycparser/blob/15ff29786e22a335eae69277bf747ada63f8e7bd/examples/cdecl.py#L133
            # __node = copy.deepcopy(_node)
            # print(create_node_from_source("int *b; ")[0])
            # print(_node_.decl.type)
            _args = _node.decl.type.args
            if(_args != None):
                _params = _args.params # Note: Python list
                assert type(_params) == list
                new_param = create_node_from_source("int* b;")[0]
                _params.append(new_param)

            print(generator.visit(_node))


# if __name__ == '__main__':
#     unittest.main()
