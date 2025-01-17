
from .token import Token, TokenType, KEYWORDS, REGISTERS

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None
        self.line = 1
        self.column = 1

    def error(self):
        raise Exception(f'Caractère invalide à la ligne {self.line}, colonne {self.column}: {self.current_char}')

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        self.pos += 1
        self.column += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char and self.current_char != '\n':
            self.advance()

    def get_number(self):
        result = ''
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_identifier(self):
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def tokenize(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '#':
                self.advance()
                self.skip_comment()
                continue

            if self.current_char.isdigit():
                tokens.append(Token(TokenType.NUMBER, str(self.get_number()), self.line, self.column))
                continue

            if self.current_char.isalpha():
                identifier = self.get_identifier()
                if identifier in KEYWORDS:
                    token_type = KEYWORDS[identifier]
                elif identifier in REGISTERS:
                    token_type = TokenType.REGISTER
                else:
                    token_type = TokenType.IDENTIFIER
                tokens.append(Token(token_type, identifier, self.line, self.column))
                continue

            if self.current_char == '[':
                tokens.append(Token(TokenType.LBRACKET, '[', self.line, self.column))
                self.advance()
                continue

            if self.current_char == ']':
                tokens.append(Token(TokenType.RBRACKET, ']', self.line, self.column))
                self.advance()
                continue

            if self.current_char == ':':
                tokens.append(Token(TokenType.COLON, ':', self.line, self.column))
                self.advance()
                continue

            if self.current_char == ',':
                tokens.append(Token(TokenType.COMMA, ',', self.line, self.column))
                self.advance()
                continue

            if self.current_char == ';':
                tokens.append(Token(TokenType.SEMICOLON, ';', self.line, self.column))
                self.advance()
                continue

            if self.current_char == '+':
                tokens.append(Token(TokenType.PLUS, '+', self.line, self.column))
                self.advance()
                continue

            if self.current_char == '-':
                tokens.append(Token(TokenType.MINUS, '-', self.line, self.column))
                self.advance()
                continue

            if self.current_char == '*':
                tokens.append(Token(TokenType.MULTIPLY, '*', self.line, self.column))
                self.advance()
                continue

            if self.current_char == '/':
                tokens.append(Token(TokenType.DIVIDE, '/', self.line, self.column))
                self.advance()
                continue

            self.error()

        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens 