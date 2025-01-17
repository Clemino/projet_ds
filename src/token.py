

from enum import Enum, auto

class TokenType(Enum):
    VAR = auto()
    INSTRUCTIONS = auto()
    BYTE = auto()
    ARRAY = auto()
    MOV = auto()
    ADD = auto()
    SUB = auto()
    MULT = auto()
    DIV = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    JMP = auto()
    JZ = auto()
    JS = auto()
    JO = auto()
    INPUT = auto()
    PRINT = auto()
    HALT = auto()
    PUSH = auto()
    POP = auto()
    IS_FULL = auto()
    CALL = auto()
    REGISTER = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COLON = auto()
    COMMA = auto()
    SEMICOLON = auto()
    HASH = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    COMMENT = auto()
    EOF = auto()

class Token:
    def __init__(self, type_: TokenType, value: str = None, line: int = 0, column: int = 0):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self):
        if self.value:
            return f'Token({self.type.name}, {self.value}, line={self.line}, col={self.column})'
        return f'Token({self.type.name}, line={self.line}, col={self.column})'
    
    def __repr__(self):
        return self.__str__()

KEYWORDS = {
    'Var': TokenType.VAR,
    'Instructions': TokenType.INSTRUCTIONS,
    'byte': TokenType.BYTE,
    'Array': TokenType.ARRAY,
    'mov': TokenType.MOV,
    'add': TokenType.ADD,
    'sub': TokenType.SUB,
    'mult': TokenType.MULT,
    'div': TokenType.DIV,
    'and': TokenType.AND,
    'or': TokenType.OR,
    'not': TokenType.NOT,
    'jmp': TokenType.JMP,
    'jz': TokenType.JZ,
    'js': TokenType.JS,
    'jo': TokenType.JO,
    'input': TokenType.INPUT,
    'print': TokenType.PRINT,
    'halt': TokenType.HALT,
    'push': TokenType.PUSH,
    'pop': TokenType.POP,
    'isFull': TokenType.IS_FULL,
    'call': TokenType.CALL,
}

REGISTERS = {
    'AX': TokenType.REGISTER,
    'BX': TokenType.REGISTER,
    'CX': TokenType.REGISTER,
    'DX': TokenType.REGISTER,
}  # type: ignore