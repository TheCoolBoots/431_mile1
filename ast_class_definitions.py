

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


# declaration → type id list ;
class m_declaration:
    def __init__(self, type:m_type, id:m_id):
        self.type = type
        self.id = id
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.type == __o.type and self.id == __o.id


# type declaration → struct id { nested decl } ;
class m_type_declaration:
    def __init__(self, id:m_id, nested_declarations:list[m_declaration]):
        self.id = id
        self.nested_declarations = nested_declarations
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.id == __o.id and listsEqual(self.nested_declarations, __o.nested_declarations)


# function → fun id parameters return type { declarations statement list }
class m_function:
    def __init__(self, id:m_id, param_declarations:list[m_declaration], return_type:m_type, body_declarations:list[m_declaration], statements:list):
        self.id = id
        self.param_declarations = param_declarations
        self.return_type = return_type
        self.body_declarations = body_declarations
        self.statements = statements
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False

        bools = [self.id == __o.id, 
            self.return_type == __o.return_type, 
            listsEqual(self.statements, __o.statements),
            listsEqual(self.body_declarations, __o.body_declarations),
            listsEqual(self.param_declarations, __o.param_declarations)]

        equal = all(bools)
        # print(f'function equal? {equal}')
        return equal


# program → types declarations functions
class m_prog:
    def __init__(self, type_declarations:list[m_type_declaration], global_declarations:list[m_declaration], functions:list[m_function]):
        self.types = type_declarations
        self.global_declarations = global_declarations
        self.functions = functions
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False

        return listsEqual(self.types, __o.types) and listsEqual(self.global_declarations, __o.global_declarations) and listsEqual(self.functions, __o.functions)
    

# assignment → lvalue = { expression | read } ;
class m_assignment:
    def __init__(self, target_ids:list[m_id], source_expression):
        self.target_ids = target_ids
        self.source_expression = source_expression
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.source_expression == __o.source_expression and listsEqual(self.target_ids, __o.target_ids)


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
class m_conditional:
    def __init__(self, guard_expression, if_statements:list, else_statements:list = [None]):
        self.guard_expression = guard_expression
        self.if_statements = if_statements
        self.else_statements = else_statements
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        equal = self.guard_expression == __o.guard_expression and listsEqual(self.if_statements, __o.if_statements) and listsEqual(self.else_statements, __o.else_statements)
        # print(f'conditional is equal? {equal}')
        return equal


# loop → while ( expression ) block
class m_loop:
    def __init__(self, guard_expression, body_statements:list):
        self.guard_expression = guard_expression
        self.body_statements = body_statements
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        equal = self.guard_expression == __o.guard_expression and listsEqual(self.body_statements, __o.body_statements)
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


class m_binop:
    def __init__(self, operator:str, left_expression, right_expression):
        self.operator = operator
        self.left_expression = left_expression
        self.right_expression = right_expression
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.operator == __o.operator and self.left_expression == __o.left_expression and self.right_expression == __o.right_expression


# invocation → id arguments ;
class m_invocation:
    # not yet sure what type arguments will be
    # but I think they will be expressions
    def __init__(self, id:m_id, args_expressions:list):
        self.id = id
        self.args_expressions = args_expressions
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.id == __o.id and listsEqual(self.args_expressions, __o.args_expressions)


# needed whenever using new [struct_id];
class m_new_struct:
    def __init__(self, struct_id:m_id):
        self.struct_id = struct_id
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.struct_id == __o.struct_id


# unary → {! | −}∗selector
class m_unary:
    def __init__(self, operator:str, operand_expression):
        self.operator = operator
        self.operand_expression = operand_expression
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.operator == __o.operator and self.operand_expression == __o.operand_expression

