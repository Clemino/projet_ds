from .token import TokenType, Token
from .ast import (Program, VarDeclaration, ArrayDeclaration, Instruction, 
                 Operation, Operand, Number, Variable, Register, ArrayAccess)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None

    def error(self, message):
        raise Exception(f'Erreur de syntaxe à la ligne {self.current_token.line}: {message}')

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def match(self, token_type):
        if self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        self.error(f'Attendu {token_type.name}, trouvé {self.current_token.type.name}')

    def parse(self):
        declarations = self.parse_declarations()
        instructions = self.parse_instructions()
        return Program(declarations, instructions)

    def parse_declarations(self):
        declarations = []
        self.match(TokenType.VAR)
        
        while self.current_token.type != TokenType.INSTRUCTIONS:
            if self.current_token.type == TokenType.IDENTIFIER:
                decl = self.parse_declaration()
                declarations.append(decl)
                if self.current_token.type == TokenType.COMMA:
                    self.advance()
            else:
                self.advance()
                
        return declarations

    def parse_declaration(self):
        name = self.match(TokenType.IDENTIFIER).value
        self.match(TokenType.COLON)
        
        if self.current_token.type == TokenType.BYTE:
            self.advance()
            return VarDeclaration(name, "byte")
        elif self.current_token.type == TokenType.ARRAY:
            self.advance()
            self.match(TokenType.LBRACKET)
            size = int(self.match(TokenType.NUMBER).value)
            self.match(TokenType.RBRACKET)
            return ArrayDeclaration(name, size)
        else:
            self.error("Type de variable attendu (byte ou Array)")

    def parse_instructions(self):
        instructions = []
        self.match(TokenType.INSTRUCTIONS)
        
        while self.current_token and self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.NUMBER:
                instr = self.parse_instruction()
                if instr:
                    instructions.append(instr)
            else:
                self.advance()
                
        return instructions

    def parse_instruction(self):
        line_num = int(self.match(TokenType.NUMBER).value)
        self.match(TokenType.COLON)
        operation = self.parse_operation()
        self.match(TokenType.SEMICOLON)
        return Instruction(line_num, operation)

    def parse_operation(self):
        if self.current_token.type == TokenType.HASH:
            self.advance()
            return None
            
        op_type = self.current_token.type
        self.advance()
        
        if op_type in [TokenType.HALT, TokenType.IS_FULL]:
            return Operation(op_type)
            
        if op_type in [TokenType.NOT, TokenType.INPUT, TokenType.PRINT, 
                      TokenType.PUSH, TokenType.POP, TokenType.CALL]:
            operand = self.parse_operand()
            return Operation(op_type, operand)
            
        if op_type in [TokenType.JMP, TokenType.JZ, TokenType.JS, TokenType.JO]:
            target = int(self.match(TokenType.NUMBER).value)
            return Operation(op_type, Number(target))
            
        operand1 = self.parse_operand()
        self.match(TokenType.COMMA)
        operand2 = self.parse_operand()
        return Operation(op_type, operand1, operand2)

    def parse_operand(self):
        if self.current_token.type == TokenType.NUMBER:
            value = int(self.match(TokenType.NUMBER).value)
            return Number(value)
            
        elif self.current_token.type == TokenType.REGISTER:
            reg = self.match(TokenType.REGISTER).value
            return Register(reg)
            
        elif self.current_token.type == TokenType.IDENTIFIER:
            var_name = self.match(TokenType.IDENTIFIER).value
            if self.current_token.type == TokenType.LBRACKET:
                self.advance()
                index = self.parse_array_index()
                self.match(TokenType.RBRACKET)
                return ArrayAccess(var_name, index)
            return Variable(var_name)
            
        self.error("Opérande invalide")

    def parse_array_index(self):
        if self.current_token.type == TokenType.NUMBER:
            return Number(int(self.match(TokenType.NUMBER).value))
        elif self.current_token.type == TokenType.IDENTIFIER:
            return Variable(self.match(TokenType.IDENTIFIER).value)
        self.error("Index de tableau invalide") 