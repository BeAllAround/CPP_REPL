# NOTE: UNUSED CODE BUT COULD BE MADE USE OF DOWN THE LINE FOR MORE CUSTOMIZED UTILITIES


class Transform:
    def __init__(self):
        self.ref_ids = dict()

        # If we have origin, we will have dest_stack
        self.dest_stack = list()
        self.ptr_decl_stack = list()

        self.decl_name = ''

    def get_decl_name(self):
        decl_name = self.decl_name
        self.decl_name = ''
        return decl_name

    def clear_stack(self):
        self.dest_stack.clear()
        self.ptr_decl_stack.clear()

    # extracting type that is essentially a cast in plain source
    # backtracking
    def extract_cast(self, node, origin = c_ast.Decl, s_build = ''):
        _type = type(node)

        if(_type == c_ast.Decl):
            return self.extract_cast(node.type, origin, s_build)

        if(_type == c_ast.FuncDecl):
            l = list()

            for param in node.args.params:
                l.append(self.extract_cast(param, None, ''))
            
            __args_build = '(' + ', '.join(l) + ')'
            

            __build = ''

            if(origin == c_ast.PtrDecl):
                __build = '(' + s_build
            else:
                __build = s_build
            
            __build += __args_build

            signature = self.extract_cast(node.type, c_ast.FuncDecl, '')

            if(origin == c_ast.PtrDecl):
                __build += signature + ')'
            else:
                __build += signature


            # if(origin == c_ast.PtrDecl):
            # else:
                #__build = signature


            # __build += __args_build

            print('signature:', [ __build, signature, s_build ])
            print("__args_build:", __args_build)

            # if(isinstance(signature, tuple)):
            #    return (signature[0] + __build + signature[1], __args_build)
            # else:
            return __build



        elif(_type == c_ast.PtrDecl):
            __build = self.extract_cast(node.type, c_ast.PtrDecl, '*' + s_build)

            return __build

        elif(_type == c_ast.TypeDecl):
            # First TypeDecl in the node tree represents the declaration name
            if(len(self.decl_name) == 0 and node.declname != None):
                self.decl_name = node.declname

            s_build = self.extract_cast(node.type, origin, node.declname)

        elif(_type == c_ast.IdentifierType):
            id_types = list()
            # while(len(self.ptr_decl_stack) != 0):
            #    id_type += self.ptr_decl_stack.pop()

            
            for name in node.names:
                id_types.append(name)

            return ' '.join(id_types)

        elif(_type == c_ast.Typename):
            return self.extract_cast(node.type, origin, s_build)
        else:
            pass


        return s_build


def _extract_cast(node):
    _t = type(node)

    if(_t == c_ast.Decl):
        pass

    s_t = ''
    s = ''
    prev = node
    while node != None:
        _t = type(node)
        
        if(_t == c_ast.FuncDecl):
            if(type(prev) == c_ast.PtrDecl):
                s = '(' + s + ')'
            params = node.args.params
            _s = ', '.join([ _extract_cast(param) for param in params ])
            s += '(' + _s + ')'
        elif(_t == c_ast.PtrDecl):
            s = '*' + s
        elif(_t == c_ast.IdentifierType):
            id_types = list()

            for name in node.names:
                id_types.append(name)

            s = ' '.join(id_types) + s

        prev = node
        print(node)
        node = getattr(node, "type", None) # if node.type != None
    return s


# if __name__ == '__main__':
#     decl_to_cast = [
#             (
#                 '''int (*(*f13(void))(void *))(int);''',
#                 ''' int(*(*)(void)(void*))(int) ''',
#                 'f13'
#             ),
#             (
#                 '''int v0;''', 
#                 ''' int ''',
#                 'v0'
#            ),
#             (
#                 '''int (*v1);''',
#                 ''' int* ''',
#                 'v1'
#             ),
#             (
#                 '''int (**v2);''',
#                 ''' int** ''',
#                 'v2'
#             ),
#             (
#                 '''int _num;''',
#                 ''' int ''',
#                 '_num'
#             ),
# 
# 
# 
#     ]

    '''
    trans = Transform()

    for decl, cast, rdecl_name in decl_to_cast:
        cast = cast.strip()

        node_ast = parser.parse(decl, filename='<none>', debug=False) # debug=True
        d = difflib.Differ()

        for ext in node_ast.ext:
            t = type(ext)
            # print(t, ext)
            if(t == c_ast.Decl):
                extracted_cast = _extract_cast(ext)
                decl_name = trans.get_decl_name()

                try:
                    # print(extracted_cast)
                    # ext.show()
                    print(ext)
                    print(generator.visit(ext))
                    assert cast == extracted_cast
                except AssertionError as excpt:
                    print([ cast, extracted_cast ])
                    # pprint.pprint(list(d.compare(cast, extracted_cast)))
                    raise excpt

                assert decl_name == rdecl_name
                assert len(trans.ptr_decl_stack) == 0
                assert len(trans.dest_stack) == 0
                # print(generator.visit(ext))

    '''

    # print(ext)
    # print('c_source:', generator.visit(ext) + ';')

    # node_ast.show()
    # print(node_ast)

