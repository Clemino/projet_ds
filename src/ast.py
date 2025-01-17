
class AST:
    pass

class Program(AST):
    def __init__(self, declarations, instructions):
        self.declarations = declarations
        self.instructions = instructions

class VarDeclaration(AST):
    def __init__(self, name, type_):
        self.name = name
        self.type = type_

class ArrayDeclaration(AST):
    def __init__(self, name, size):
        self.name = name
        self.size = size

class Instruction(AST):
    def __init__(self, number, operation):
        self.number = number
        self.operation = operation

class Operation(AST):
    def __init__(self, type_, operand1=None, operand2=None):
        self.type = type_
        self.operand1 = operand1
        self.operand2 = operand2

class Operand(AST):
    pass

class Number(Operand):
    def __init__(self, value):
        self.value = value

class Variable(Operand):
    def __init__(self, name):
        self.name = name

class Register(Operand):
    def __init__(self, name):
        self.name = name

class ArrayAccess(Operand):
    def __init__(self, name, index):
        self.name = name
        self.index = index # type: ignore