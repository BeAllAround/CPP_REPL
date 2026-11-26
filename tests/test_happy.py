
import inspect

import unittest


from cpp_repl.core.interpret import CppInterpreter


# TestCase.assertEqual, TestCase.assertTrue, TestCase.assertFalse

def create_node_from_source(_code):
    parser = c_parser.CParser(yacctab=yacctab)
    node_ast = parser.parse(_code, filename='<none>', debug=False) # debug=True

    return node_ast.ext

class VerifyCppInterpreterSetupAndRun(unittest.TestCase):
    def test_happy(self):
        cpp_interpreter = CppInterpreter()

        setup_ok = cpp_interpreter.setUp()

        self.assertTrue(setup_ok == 0)


        cpp_interpreter.interpret("int i = 1; std::cout << i << std::endl;")


        cleanUpOk = cpp_interpreter.cleanUp()

        self.assertTrue(cleanUpOk == 0)


    def test_try_run_01(self):
        pass



# if __name__ == '__main__':
#     unittest.main()
