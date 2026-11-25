import unittest

from pycparser import c_lexer

from pycparser import c_parser, c_generator, c_ast

from pycparser import yacctab

CLexer = c_lexer.CLexer


from c_repl.utility.logger import info, debug

# from c_repl.core import s2s
from c_repl.core.s2s import _GCC_Utility, CParser_Utility, comment_remover, add_semi, compare_source, r_ws

# alias
STR_EMPTY = ''
_gccu = _GCC_Utility


class Test_Id_Replace(unittest.TestCase):
    # Note that
    # The setUp() and tearDown() methods allow you to define instructions that will be executed before and after each test method.
    # See https://docs.python.org/3/library/unittest.html for more
    def setUp(self):

        self.init()

        self._refs = self.mock_up_ids()
    
    def tearDown(self):
        pass

    def init(self):
        self.generator = c_generator.CGenerator(False, self.visit_id_func_wrapper)
        self.parser = c_parser.CParser(yacctab=yacctab)

    def mock_up_ids(self):
        refs = dict()
        refs['v1'] = 'deref_var(int*, 0, vars)'
        
        return refs

    def visit_id_func_wrapper(self, c_gen_ref, node_id):

        inside_of_func_def_body = c_gen_ref.inside_of_func_def_body

        _refs = self._refs
        # print(self, node_id)
        # print(c_gen_ref.inside_of_func_def_body, node_id)

        if inside_of_func_def_body:
            return node_id.name

        look_up = _refs.get(node_id.name)

        if(look_up != None):
            return look_up
        
        return node_id.name

    def parse(self, source):
        # TODO: Remove comments and possibly use '-E' for GCC preprocessor output
        source = comment_remover(source)

        node_ast = self.parser.parse(source, filename='<none>', debug=False) # debug=True
        return node_ast

    def test_0(self):
        generator = self.generator
        parser = self.parser
        parse = self.parse
        visit = self.generator.visit

        c_parser_utility = CParser_Utility(generator)

        source_get_decl_from_def = c_parser_utility.source_get_decl_from_def

        source_code = '''
            // Assignment Expression
            v = 1;

            v1 = 2;

            int v2 = 1 ? v1 : v;

            ({v1; v1;});

            void func(int v1) {
                printf("%d\\n", v1);
            }

            // Declaration
            int v3 = v1;

            // Unary operator
            !v1;

            // Logical Operator
            v1 || v1 && v1;

            // Ternary Operator
            1 ? v1 : v1;
        '''

        out_asserts = [
            (
                '''
                v = 1;
                ''',
            ),
            (
                '''
                deref_var(int*, 0, vars) = 2;
                ''',
            ),
            (
                '''
                int v2 = (1) ? (deref_var(int*, 0, vars)) : (v);
                ''',
            ),
            (
                '''
                {
                    deref_var(int*, 0, vars);
                    deref_var(int*, 0, vars);
                }
                ''',
            ),
            (
                # Unchanged essentially.
                # TODO: Make a refactor for unchanged output source
                '''
                void func(int v1) {
                    printf("%d\\n", v1);
                }
                ''',
            ),

            (
                '''
                int v3 = deref_var(int*, 0, vars);
                ''',
            ),

            (
                '''
                !deref_var(int*, 0, vars);
                ''',
            ),

            (
                '''
                deref_var(int*, 0, vars) || (deref_var(int*, 0, vars) && deref_var(int*, 0, vars));
                ''',
            ),

            (
                '''
                (1) ? (deref_var(int*, 0, vars)) : (deref_var(int*, 0, vars));
                ''',
            ),

        ]


        node_ast = parse(source_code)

        assert len(node_ast.ext) == len(out_asserts)

        i = 0
        for ext in node_ast.ext:
            tmp_ext = str(ext)

            # print(ext)
            c_source_out = visit(ext) + add_semi(ext)

            (assert_source,) = out_asserts[i]

            debug("Asserting", c_source_out, assert_source)

            compare_source(self, c_source_out, assert_source)

            assert str(ext) == tmp_ext

            i += 1
    
    def test_1(self):
        generator = self.generator
        parser = self.parser
        parse = self.parse
        visit = self.generator.visit

        c_parser_utility = CParser_Utility(generator)

        source_get_decl_from_def = c_parser_utility.source_get_decl_from_def

        source_code = '''

        // Variable Declarations
        int n = 1;
        const char* _string = "AAA";

        // Function Declarations
        void f();

        void f1(int);

        void f2(int a);

        void f3(int a, int b);

        // Function Definitions
        void f4() {
            printf();
        }

        void f5(int a) {
            printf("%d\\n", a);
        }

        void f6(int a, int b) {
            printf("%d %d\\n", a, b);
        }

        '''

        out_asserts = [
            (
                "int n;",
            ),

            (
                "const char *_string;",
            ),

            (
                "void f();",
            ),

            (
                "void f1(int);",
            ),

            (
                "void f2(int a);",
            ),

            (
                "void f3(int a, int b);",
            ),

            (
                "void f4();",
            ),

            (
                "void f5(int a);",
            ),

            (
                "void f6(int a, int b);",
            ),


        ]

        node_ast = parse(source_code)

        i = 0

        for ext in node_ast.ext:
            tmp_ext = str(ext)

            # print(ext)

            # NOTE: Being the array, node_ast.ext is joint by ';'. However, with individual nodes - NO SEMI-COLON!
            c_source_out = source_get_decl_from_def(ext) + ';' # + add_semi(ext) is only used with immutable node before "visit"

            (assert_source,) = out_asserts[i]
            # print(tmp_ext)

            debug("Asserting", c_source_out, assert_source)

            compare_source(self, c_source_out, assert_source)

            assert str(ext) == tmp_ext

            i += 1



# TODO: https://docs.python.org/3/library/unittest.html
class Test(unittest.TestCase):
    def setUp(self):
        self.init()

    def init(self):
        self.generator = c_generator.CGenerator()
        self.parser = c_parser.CParser(yacctab=yacctab)


    def parse(self, source):
        node_ast = self.parser.parse(source, filename='<none>', debug=False) # debug=True
        return node_ast

    def test_0(self):
        generator = self.generator
        parser = self.parser
        parse = self.parse

        source_code = comment_remover('''
            // DECLARATIONS AND DEFINITIONS
            int i = 1;
            char c = 'a';
            void* d;

            int* pi = &i;

            const int* c_pi = &i;

            const char* cc_1 = "AAA";

            int** ppi = &pi;

            int*** pppi = &ppi;

            // NOTE: FUNCTION DECLARATION - NOT A FUNCTION POINTER!!! BUT STILL TREATED AS (*) by GCC. See the very next case
            // THUS: error: function 'f13' is initialized like a variable
            int (*(*f13(void))(void*))(int);

            // SAME AS THE PREVIOUS
            int (*(*(*f13)(void))(void*))(int);


            // FUNCTION DEFINITION
            void f() {
            }

                                      
            void f1(int, char) {
            }

            void f2(int* p) {
            }


        ''')
        # void f1 () {}

        output_casts = [
                '(int *)',
                '(char *)',
                '(void **)',
                '(int **)',
                '(const int **)',
                '(const char **)',
                '(int ***)',
                '(int ****)',

                '(int (* (* (*)(void))(void *))(int))',
                '(int (* (* (**)(void))(void *))(int))',

                '(void (*)())',
                '(void (*)(int, char))',
                '(void (*)(int*))',
        ]

        node_ast = parse(source_code)
        # print(node_ast)

        assert len(node_ast.ext) == len(output_casts)

        i = 0
        # Quote: FileAST: 'Its children are "external declarations"'
        for ext in node_ast.ext:
            tmp_ext = str(ext) # Must not be mutated so dump as a string and compare

            _typeof = _gccu.get_type_as_ptr('', ext)
            _cast = '(' + _typeof + ')'


            debug("Asserting", _cast, output_casts[i])

            # print(_cast, output_casts[i])

            assert r_ws(_cast) == r_ws(output_casts[i])

            assert tmp_ext == str(ext)

            i += 1
