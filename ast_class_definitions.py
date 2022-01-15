

"""
TASK 1: create python class for each format as described in overview.pdf
    name class m_[name of thing]
    ex def m_program(types declarations functions)
    NOTE maybe this isn't required? can do all semantic checks just on json?
"""

def listsEqual(listA:list, listB:list):
    if len(listA) != len(listB):
        return False
    for i in range(len(listA)):
        if not (listA[i] == listB[i]):
            return False
    return True

# placeholder classes; will be overwritten at compile time

class m_binop:
    None

class m_bool:
    def __init__(self, val:bool):
        self.val = val
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return not (self.val ^ __o.val)

class m_null:
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False

class m_num:
    def __init__(self, val:int):
        self.val = val
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.val == __o.val

class m_id:
    def __init__(self, identifier:str):
        self.identifier = identifier
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.identifier == __o.identifier


# type → int | bool | struct id
class m_type:
    def __init__(self, typeID:str):
        self.type = typeID
        typeKeywords = ['int', 'bool', 'void']
        if self.type not in typeKeywords:
            print(f'ERROR: invalid type. Expected {typeKeywords} but got {self.type}')
    def __init__(self, typeID:m_id):
        self.type = typeID
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.type == __o.type


# due to id list being obslete, m_decl and m_declaration are the same thing
# decl → type id
# class m_decl:
#     def __init__(self, type:m_type, id:m_id):
#       self.type = type
#       self.id = id

# it appears as though the java miniCompiler parses out declaration id list into individual declarations
# and so this class is obslete
# # id list → id {,id}∗
# class m_id_list:
#     def __init__(self, id_list:list[m_id]):
#         self.id_list = id_list # TODO check id_list len >= 1
#         if len(self.id_list < 1):
#             print("ERROR: according to overview.pdf, an id_list should have 1 or more ids. This condition is not met somewhere")


# declaration → type id list ;
class m_declaration:
    def __init__(self, type:m_type, id:m_id):
        self.type = type
        self.id = id
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.type == __o.type and self.id == __o.id


# # declarations → {declaration}∗
# class m_declarations:
#     def __init__(self, declarations:list[m_declaration]):
#       self.declarations = declarations
#     def __eq__(self, __o: object) -> bool:
#         if type(__o) != type(self):
#             return False
#         if len(self.declarations) != len(__o.declarations):
#             return False
#         for i in range(len(self.declarations)):
#             if not (self.declarations[i] == __o.declarations[i]):
#                 return False
#         return True


# has the same parsing signature of m_declarations, just have to make sure len of declarations is >= 1
# nested decl → decl ; {decl ;}∗
# class m_nested_decl:
#     def __init__(self, declarations:list[m_declaration]):
#         self.declarations = declarations  # TODO check declarations len >= 1
#         if len(self.declarations) < 1:
#             print(f"ERROR: according to overview.pdf, a nested_decl should have 1 or more ids. This condition is not met somewhere")
#     def __eq__(self, __o: object) -> bool:
#         if type(__o != m_types):
#             return False
#         if len(self.declarations) != len(__o.declarations):
#             return False
#         for i in range(len(self.declarations)):
#             if not (self.declarations[i] == __o.declarations[i]):
#                 return False
#         return True


# type declaration → struct id { nested decl } ;
class m_type_declaration:
    def __init__(self, id:m_id, nested_declarations:list[m_declaration]):
        self.id = id
        self.nested_declarations = nested_declarations
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.id == __o.id and listsEqual(self.nested_declarations, __o.nested_declarations)


# # types → {type declaration}∗
# class m_types:
#     def __init__(self, type_declarations:list[m_type_declaration]):
#         self.type_declarations = type_declarations
#     def __eq__(self, __o: object) -> bool:
#         if type(__o) != type(self):
#             return False
#         if len(self.type_declarations) != len(__o.type_declarations):
#             return False
#         for i in range(len(self.type_declarations)):
#             if not (self.type_declarations[i] == __o.type_declarations[i]):
#                 return False
#         return True


# is obslete; has same structure as m_nested_decl
# parameters → ( {decl {,decl}∗}opt)
# class m_parameters:
#     def __init__(self, decls:list[m_declaration] = None):
#         self.decls = decls  # TODO if decls != None, len needs to be >= 1
#         if(self.decls != None and len(decls) < 1):
#             print(f"ERROR: according to overview.pdf, a paramaters should have 1 or more decls. This condition is not met somewhere")


# is obslete; can just be stored as m_type
# return type → type | void
# class m_return_type:
#     def __init__(self, type:str):
#         self.type = type    # TODO check if return val is "void"
#         if(self.type != "void"):
#             print(f'ERROR: the return type should either be a valid type or void.')
#     def __init__(self, type:m_type):
#         self.type = type
#     def __eq__(self, __o: object) -> bool:
#         if type(__o) != type(self):
#             return False
#         return self.type == __o.type


# function → fun id parameters return type { declarations statement list }
class m_function:
    def __init__(self, id:m_id, parameters:list[m_declaration], return_type:m_type, declarations:list[m_declaration], statement_list:list):
        self.id = id
        self.parameters = parameters
        self.return_type = return_type
        self.declarations = declarations
        self.statement_list = statement_list
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False

        bools = [self.id == __o.id, 
            self.return_type == __o.return_type, 
            listsEqual(self.statement_list, __o.statement_list),
            listsEqual(self.declarations, __o.declarations),
            listsEqual(self.parameters, __o.parameters)]

        equal = all(bools)
        # print(f'function equal? {equal}')
        return equal


# # functions → {function}∗
# class m_functions:
#     def __init__(self, functions:list[m_function]):
#       self.functions = functions
#     def __eq__(self, __o: object) -> bool:
#         if type(__o) != type(self):
#             return False
#         if len(self.functions) != len(__o.functions):
#             return False
#         for i in range(len(self.functions)):
#             if not (self.functions[i] == __o.functions[i]):
#                 return False
#         return True


# program → types declarations functions
class m_prog:
    def __init__(self, types:list[m_type_declaration], declarations:list[m_declaration], functions:list[m_function]):
        self.types = types
        self.declarations = declarations
        self.functions = functions
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False

        return listsEqual(self.types, __o.types) and listsEqual(self.declarations, __o.declarations) and listsEqual(self.functions, __o.functions)
    

# assignment → lvalue = { expression | read } ;
class m_assignment:
    def __init__(self, target:list[m_id], assignmentExpression):
        self.target = target
        self.assignmentExpression = assignmentExpression
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.assignmentExpression == __o.assignmentExpression and listsEqual(self.target, __o.target)


# print → print expression {endl}opt;
class m_print:
    def __init__(self, expression, endl:bool = None):
        self.expression = expression
        self.endl = endl
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.expression == __o.expression and self.endl == __o.endl


# conditional → if ( expression ) block {else block}opt
"""

"""
class m_conditional:
    def __init__(self, expression, if_statementList:list, else_statementList:list = None):
        self.expression = expression
        self.if_statementList = if_statementList
        self.else_statementList = else_statementList
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        equal = self.expression == __o.expression and listsEqual(self.if_statementList, __o.if_statementList) and listsEqual(self.else_statementList, __o.else_statementList)
        # print(f'conditional is equal? {equal}')
        return equal


# loop → while ( expression ) block
class m_loop:
    def __init__(self, expression, body_statementList:list):
        self.expression = expression
        self.body_statementList = body_statementList
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        equal = self.expression == __o.expression and listsEqual(self.body_statementList, __o.body_statementList)
        # print(f'm_loops equal? {equal}')
        # print(type(self.block), type(__o.block))
        return equal


# delete → delete expression ;
class m_delete:
    def __init__(self, expression):
        self.expression = expression
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.expression == __o.expression


# ret → return {expression}opt;
class m_ret:
    def __init__(self, expression = None):
        self.expression = expression
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.expression == __o.expression


# invocation → id arguments ;
class m_invocation:
    def __init__(self, id:m_id, arguments):
        self.id = id
        self.arguments = arguments
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.id == __o.id and self.arguments == __o.arguments 


# statement → block | assignment | print | conditional | loop | delete | ret | invocation
# class m_statement:
#     # def __init__(self, contents:m_block):
#     #     self.contents = contents
#     def __init__(self, contents:m_assignment):
#         self.contents = contents
#     def __init__(self, contents:m_print):
#         self.contents = contents
#     def __init__(self, contents:m_conditional):
#         self.contents = contents
#     def __init__(self, contents:m_loop):
#         self.contents = contents
#     def __init__(self, contents:m_delete):
#         self.contents = contents
#     def __init__(self, contents:m_ret):
#         self.contents = contents
#     def __init__(self, contents:m_invocation):
#         self.contents = contents
#     def __eq__(self, __o: object) -> bool:
#         if type(__o) != type(self):
#             return False
#         equal = self.contents == __o.contents
#         # print(f'statement equal? {equal}')
#         return equal


# # statement list → {statement}∗
# class m_statement_list:
#     def __init__(self, statements:list[m_statement]):
#         self.statements = statements
#     def __eq__(self, __o: object) -> bool:
#         if type(__o) != type(self):
#             return False
#         if len(self.statements) != len(__o.statements):
#             return False
#         for i in range(len(self.statements)):
#             if not (self.statements[i] == __o.statements[i]):
#                 return False
#         return True
    

# block → { statement list }
# class m_block:
#     def __init__(self, statement_list:list[m_statement]):
#         self.statement_list = statement_list
#     def __eq__(self, __o: object) -> bool:
#         if type(__o) != type(self):
#             return False
#         if len(self.statement_list) != len(__o.statement_list):
#             return False
#         for i in range(len(self.statement_list)):
#             if not (self.statement_list[i] == __o.statement_list[i]):
#                 return False
#         return True


# # lvalue → id {.id}∗
# class m_lvalue:
#     def __init__(self, m_ids:list[m_id]):
#         self.m_ids = m_ids  # length of m_ids should be >= 1
#         if len(self.m_ids) < 1:
#             print(f"ERROR: according to overview.pdf, a lvalue should have 1 or more ids. This condition is not met somewhere")
#     def __eq__(self, __o: object) -> bool:
#         if type(__o) != type(self):
#             return False
#         if len(self.m_ids) != len(__o.m_ids):
#             return False
#         for i in range(len(self.m_ids)):
#             if not (self.m_ids[i] == __o.m_ids[i]):
#                 return False
#         return True


# ( expression ) | id {arguments}opt| number | true | false | new id | null
class m_factor:
    def __init__(self, contents):
        self.expression = contents
        self.rest = None
    def __init__(self, contents:m_id, arguments = None):
        self.expression = contents
        self.rest = arguments
    def __init__(self, contents:int):
        self.expression = contents
        self.rest = None
    def __init__(self, contents:str):
        self.expression = contents  # TODO contents should either be "true", "false", or "null"
        keywords = ['true', 'false', 'null']
        if self.expression not in keywords:
            print(f'ERROR: invalid keyword in m_factor. Got {self.expression} but expected one of {keywords}.')
        self.rest = None
    def __init__(self, contents:str, id:m_id):  # for the new id case
        self.expression = contents  # TODO contents should be "new"
        if self.expression != "new":
            print(f'ERROR: expected keyword "new" in m_factor but got keyword {self.expression}')
        self.rest = id
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.expression == __o.expression and self.rest == __o.rest
    

# selector → factor {.id}∗
class m_selector:
    def __init__(self, factor:m_factor, identifiers:list[m_id]):
        self.factor = factor
        self.identifiers = identifiers
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        if len(self.identifiers) != len(__o.identifiers):
            return False
        for i in range(len(self.identifiers)):
            if not (self.identifiers[i] == __o.identifiers[i]):
                return False
        return self.factor == __o.factor


# unary → {! | −}∗selector
class m_unary:
    def __init__(self, operators:list[str], selector:m_selector):
        self.operators = operators
        self.selector = selector
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        if len(self.operators) != len(__o.operators):
            return False
        for i in range(len(self.operators)):
            if not (self.operators[i] == __o.operators[i]):
                return False
        return self.selector == __o.selector


# class m_expression:
#     def __init__(self, contents:m_binop) -> None:
#         self.contents = contents
#     def __init__(self, contents:m_num) -> None:
#         self.contents = contents
#     def __init__(self, contents:m_bool) -> None:
#         self.contents = contents
#     def __init__(self, contents:m_null) -> None:
#         self.contents = contents
#     def __eq__(self, __o: object) -> bool:
#         if type(self) != type(__o):
#             return False
#         return self.contents == __o.contents


class m_binop:
    def __init__(self, operator:str, left, right):
        self.operator = operator
        self.left = left
        self.right = right
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.operator == __o.operator and self.left == __o.left and self.right == __o.right

    


# all binary operators are parsed by parser into a single type, so can scratch all that out
# similarly, all "expressions" will be explicitly defined by parser, and thus we won't need to consider them
# # term → unary {{∗ | /} unary}∗
# class m_term:
#     def __init__(self, unarys:list[m_unary], operators:list[str]):
#         self.unarys = unarys
#         self.operators = operators
#     def __eq__(self, __o: object) -> bool:
#         if type(__o) != type(self):
#             return False
#         if len(self.unarys) != len(__o.unarys):
#             return False
#         for i in range(len(self.unarys)):
#             if not (self.unarys[i] == __o.unarys[i]):
#                 return False
#         if len(self.operators) != len(__o.operators):
#             return False
#         for i in range(len(self.operators)):
#             if not (self.operators[i] == __o.operators[i]):
#                 return False
#         return True


# # simple → term {{+ | −} term}∗
# class m_simple:
#     def __init__(self, terms:list[m_term], operators:list[str]):
#         self.terms = terms
#         self.operators = operators
#     def __eq__(self, __o: object) -> bool:
#         if type(__o) != type(self):
#             return False
#         if len(self.terms) != len(__o.terms):
#             return False
#         for i in range(len(self.terms)):
#             if not (self.terms[i] == __o.terms[i]):
#                 return False
#         if len(self.operators) != len(__o.operators):
#             return False
#         for i in range(len(self.operators)):
#             if not (self.operators[i] == __o.operators[i]):
#                 return False
#         return True


# # relterm → simple {{<| >| <= | >=} simple}∗
# class m_relterm:
#     def __init__(self, simples:list[m_simple], operators:list[str]):
#         self.simples = simples
#         self.operators = operators
#     def __eq__(self, __o: object) -> bool:
#         if type(__o) != type(self):
#             return False
#         if len(self.simples) != len(__o.simples):
#             return False
#         for i in range(len(self.simples)):
#             if not (self.simples[i] == __o.simples[i]):
#                 return False
#         if len(self.operators) != len(__o.operators):
#             return False
#         for i in range(len(self.operators)):
#             if not (self.operators[i] == __o.operators[i]):
#                 return False
#         return True


# # eqterm → relterm {{== | ! =} relterm}∗
# class m_eqterm:
#     def __init__(self, relterms:list[m_relterm], operators:list[str]):
#         self.relterms = relterms
#         self.operators = operators
#     def __eq__(self, __o: object) -> bool:
#         if type(__o) != type(self):
#             return False
#         if len(self.relterms) != len(__o.relterms):
#             return False
#         for i in range(len(self.relterms)):
#             if not (self.relterms[i] == __o.relterms[i]):
#                 return False
#         if len(self.operators) != len(__o.operators):
#             return False
#         for i in range(len(self.operators)):
#             if not (self.operators[i] == __o.operators[i]):
#                 return False
#         return True


# # boolterm → eqterm {&& eqterm}∗
# class m_boolterm:
#     def __init__(self, eqterms:list[m_eqterm]):
#         self.eqterms = eqterms
#     def __eq__(self, __o: object) -> bool:
#         if type(__o) != type(self):
#             return False
#         if len(self.eqterms) != len(__o.eqterms):
#             return False
#         for i in range(len(self.eqterms)):
#             if not (self.eqterms[i] == __o.eqterms[i]):
#                 return False
#         return True