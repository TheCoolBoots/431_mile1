

"""
TASK 1: create python class for each format as described in overview.pdf
    name class m_[name of thing]
    ex def m_program(types declarations functions)
    NOTE maybe this isn't required? can do all semantic checks just on json?
"""

# from msilib.schema import Error
from typing import Tuple


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
        return 


class m_num:
    def __init__(self, val:int):
        self.val = val
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.val == __o.val


class m_id:
    def __init__(self, lineNum:int, identifier:str):
        self.identifier = identifier
        self.lineNum = lineNum
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.identifier == __o.identifier
    def __str__(self):
        return self.identifier


# type → int | bool | struct id
class m_type:
    def __init__(self, typeID:str):
        self.typeID = typeID
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.typeID == __o.typeID
    def __str__(self):
        return self.typeID


# declaration → type id list ;
class m_declaration:
    def __init__(self, lineNum:int, type:m_type, id:m_id):
        self.type = type
        self.id = id
        self.lineNum = lineNum
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.type == __o.type and self.id == __o.id and self.lineNum == __o.lineNum

    # NOTE: type_env structure = {str : {str : (int, m_type)}}
    def getLLVM(self, lastRegUsed:int, type_sizes:dict):
        match self.type.typeID:
            case 'int'|'bool':
                return [f'%{self.id.identifier} = alloca i32']    # TODO check if can use i8 instead
            case structID:
                return [f'%{lastRegUsed + 1} = call i8* @malloc({type_sizes[structID]})',
                f'%{self.id.identifier} = bitcast i8* %{lastRegUsed + 1} to %struct.{structID}*']

    def getSSAGlobals(self) -> list[str]:
        if self.type.typeID == 'int' or self.type.typeID == 'bool':
            return f'@{self.id.identifier} = common dso_local global i32 0'
        else:
            return f'@{self.id.identifier} = common dso_local global %struct.{self.type.typeID}* null'

    def getSSALocals(self) -> list[str]:
        if self.type.typeID == 'int' or self.type.typeID == 'bool':
            return f'%{self.id.identifier} = alloca i32'
        else:
            return f'%{self.id.identifier} = alloca %struct.A*'


# type declaration → struct id { nested decl } ;
class m_type_declaration:
    def __init__(self, lineNum:int, id:m_id, nested_declarations:list[m_declaration]):
        self.id = id
        self.nested_declarations = nested_declarations
        self.lineNum = lineNum
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.id == __o.id and self.nested_declaration == __o.nested_declarations and self.lineNum == __o.lineNum
    def getLLVM(self):
            # %struct.foo = type {i32, i32, %struct.simple*}
            # %struct.simple = type {i32}
            types = []
            for decl in self.nested_declarations:
                if decl.type == m_type('int') or decl.type == m_type('bool'):
                    types.append('i32')
                else:
                    types.append(f'%struct.{decl.type.typeID}*')
            types = '{' + (', '.join(types)) + '}'
            return f'%struct.{self.id.identifier} = type {types}'


# function → fun id parameters return type { declarations statement list }
class m_function:
    def __init__(self, lineNum:int, id:m_id, param_declarations:list[m_declaration], return_type:m_type, body_declarations:list[m_declaration], statements:list):
        self.id = id
        self.param_declarations = param_declarations
        self.return_type = return_type
        self.body_declarations = body_declarations
        self.statements = statements
        self.lineNum = lineNum
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False

        bools = [self.id == __o.id, 
            self.return_type == __o.return_type, 
            self.statements == __o.statements,
            self.body_declarations == __o.body_declarations,
            self.param_declarations == __o.param_declarations,
            self.lineNum == __o.lineNum]

        equal = all(bools)
        # print(f'function equal? {equal}')
        return equal


# program → types declarations functions
class m_prog:
    def __init__(self, type_declarations:list[m_type_declaration], global_declarations:list[m_declaration], functions:list[m_function]):
        self.types = type_declarations
        self.global_declarations = global_declarations
        self.functions = functions

    # returns {str : {str : (int, m_type)}}
    def getTopTypeEnv(self):
        env = {}
        for type_declaration in self.types:
            decls = {decl.id.identifier:(decl.lineNum, decl.type) for decl in type_declaration.nested_declarations}
            env[type_declaration.id.identifier] = decls
        return env

    # for use in generateLLVM
    # maps struct IDs to a list of nested m_declarations
    # returns {str: list[m_declaration]}
    def getTypes(self):
        return {typeDecl.id.identifier:typeDecl.nested_declarations for typeDecl in self.types}

    def getTypeSizes(self):
        return {typeDecl.id.identifier:len(typeDecl.nested_declarations) * 4 for typeDecl in self.types}

    # returns {str : m_type}
    def getTopEnv(self, includeLineNum = True):
        if includeLineNum:
            return {decl.id.identifier:(decl.lineNum, decl.type) for decl in self.global_declarations}
        else:
            return {decl.id.identifier:(True, decl.type) for decl in self.global_declarations}

    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False

        return self.types == __o.types and self.global_declarations == __o.global_declarations and self.functions == __o.functions
    

# assignment → lvalue = { expression | read } ;
class m_assignment:
    def __init__(self, lineNum:int, target_ids:list[m_id], source_expression):
        self.target_ids = target_ids
        self.source_expression = source_expression
        self.lineNum = lineNum
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.source_expression == __o.source_expression and self.target_ids == __o.target_ids and self.lineNum == __o.lineNum


# print → print expression {endl}opt;
class m_print:
    def __init__(self, lineNum:int, expression, endl:bool = False):
        self.expression = expression
        self.endl = endl
        self.lineNum = lineNum
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.expression == __o.expression and self.endl == __o.endl and self.lineNum == __o.lineNum


# conditional → if ( expression ) block {else block}opt
class m_conditional:
    def __init__(self, lineNum:int, guard_expression, if_statements:list, else_statements:list = [None]):
        self.guard_expression = guard_expression
        self.if_statements = if_statements
        self.else_statements = else_statements
        self.lineNum = lineNum
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        equal = self.guard_expression == __o.guard_expression and self.if_statements == __o.if_statements and self.else_statements == __o.else_statements
        # print(f'conditional is equal? {equal}')
        return equal and self.lineNum == __o.lineNum


# loop → while ( expression ) block
class m_loop:
    def __init__(self, lineNum:int, guard_expression, body_statements:list):
        self.guard_expression = guard_expression
        self.body_statements = body_statements
        self.lineNum = lineNum
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        equal = self.guard_expression == __o.guard_expression and self.body_statements == __o.body_statements
        # print(f'm_loops equal? {equal}')
        # print(type(self.block), type(__o.block))
        return equal and self.lineNum == __o.lineNum


# delete → delete expression ;
class m_delete:
    def __init__(self, lineNum:int, expression):
        self.expression = expression
        self.lineNum = lineNum
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.expression == __o.expression and self.lineNum == __o.lineNum


class m_read:
    def __init__(self, lineNum):
        self.lineNum = lineNum
    def __eq__(self, __o):
        if type(__o) != type(self):
            return False
        return self.lineNum == __o.lineNum    


# ret → return {expression}opt;
class m_ret:
    def __init__(self, lineNum:int, expression = None):
        self.expression = expression
        self.lineNum = lineNum
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.expression == __o.expression and self.lineNum == __o.lineNum


# == != <= < > >= - + * / || &&
class m_binop:
    def __init__(self, lineNum:int, operator:str, left_expression, right_expression):
        self.operator = operator
        self.left_expression = left_expression
        self.right_expression = right_expression
        self.lineNum = lineNum
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.operator == __o.operator and self.left_expression == __o.left_expression and self.right_expression == __o.right_expression and self.lineNum == __o.lineNum
            

# invocation → id arguments ;
class m_invocation:
    # not yet sure what type arguments will be
    # but I think they will be expressions
    def __init__(self, lineNum:int, id:m_id, args_expressions:list):
        self.id = id
        self.args_expressions = args_expressions
        self.lineNum = lineNum
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.id == __o.id and self.args_expressions == __o.args_expressions and self.lineNum == __o.lineNum


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
    def __init__(self, lineNum:int, operator:str, operand_expression):
        self.operator = operator
        self.operand_expression = operand_expression
        self.lineNum = lineNum
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.operator == __o.operator and self.operand_expression == __o.operand_expression and self.lineNum == __o.lineNum


class m_dot:
    def __init__(self, lineNum:int, ids:list[m_id]):
        self.lineNum = lineNum
        self.ids = ids
    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        return self.lineNum == __o.lineNum and self.ids == __o.ids


class CFG_Node():
    None


class CFG_Node():
    def __init__(self, id:int, label:str, sealed = True, guardExpression = None) -> None:
        self.id = id
        self.label = label
        self.ast_statements = []
        self.guardExpression = guardExpression
        self.prevNodes = []
        self.nextNodes = []
        self.sealed = sealed
        self.mappings = {}
        self.visited = False

    def addPrevNode(self, node:CFG_Node):
        self.prevNodes.append(node)

    def addNextNode(self, node:CFG_Node):
        self.nextNodes.append(node)

    def extendStatements(self, statements:list):
        self.ast_statements.extend(statements)


class Function_CFG():
    def __init__(self, rootNode:CFG_Node, exitNode:CFG_Node, returnNode:CFG_Node, ast:m_function):
        self.rootNode = rootNode
        self.exitNode = exitNode
        self.returnNode = returnNode
        self.ast = ast

    def serialize(self):
        output = ['digraph "cfg" {']
        nodeReferences = {}
        queue = []
        queue.append(self.rootNode)

        while queue != []:
            currNode = queue.pop(0)

            if currNode.id in nodeReferences:
                continue
            else:
                nodeReferences[currNode.id] = True
            for node in currNode.nextNodes:
                output.append("  " + str(currNode.id) + " -> " + str(node.id) + ";")
                queue.append(node)
        
        output.append('}')
        return output

    def getAllNodes(self, dictionary = False) -> list:
        nodeReferences = {}
        queue = []
        queue.append(self.rootNode)
        while queue != []:
            currNode = queue.pop(0)
            if currNode.id in nodeReferences:
                continue
            else:
                nodeReferences[currNode.id] = currNode
            for node in currNode.nextNodes:
                queue.append(node)
        if dictionary:
            return nodeReferences
        return list(nodeReferences.values())

    def getUnsealedNodes(self) -> dict:
        unsealedNodes = {}
        nodeReferences = {}
        queue = []
        queue.append(self.rootNode)
        while queue != []:
            currNode = queue.pop(0)
            if currNode.id in nodeReferences:
                continue
            else:
                nodeReferences[currNode.id] = currNode
                if not currNode.sealed:
                    unsealedNodes[currNode.id] = currNode
            for node in currNode.nextNodes:
                queue.append(node)
        return unsealedNodes