from .token import TokenType
from .ast import (Variable, Number, ArrayAccess, AST, Program, 
                 VarDeclaration, ArrayDeclaration, Instruction, 
                 Operation, Operand, Register)

class Symbol:
    def __init__(self, name, type_, size=None):
        self.name = name
        self.type = type_
        self.size = size

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.instruction_labels = set()

    def define(self, name, type_, size=None):
        if name in self.symbols:
            raise Exception(f"Erreur sémantique: Variable '{name}' déjà déclarée")
        self.symbols[name] = Symbol(name, type_, size)

    def lookup(self, name):
        return self.symbols.get(name)

    def add_instruction(self, label):
        self.instruction_labels.add(label)

    def has_instruction(self, label):
        return label in self.instruction_labels

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.current_instruction = None

    def visit_Program(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        for instruction in node.instructions:
            self.visit(instruction)
        self.verify_jump_labels()

    def visit_VarDeclaration(self, node):
        self.symbol_table.define(node.name, 'byte')

    def visit_ArrayDeclaration(self, node):
        if node.size <= 0:
            raise Exception(f"Erreur sémantique: Taille de tableau invalide pour '{node.name}'")
        self.symbol_table.define(node.name, 'array', node.size)

    def visit_Instruction(self, node):
        self.current_instruction = node.number
        self.symbol_table.add_instruction(node.number)
        if node.operation:
            self.visit(node.operation)

    def visit_Operation(self, node):
        if node.type in ['JMP', 'JZ', 'JS', 'JO']:
            self.check_jump_target(node.operand1.value)
        elif node.type in ['INPUT', 'PRINT', 'PUSH', 'POP']:
            self.check_operand(node.operand1)
        elif node.type == 'NOT':
            self.check_operand(node.operand1)
        elif node.type == 'CALL':
            self.check_procedure_call(node.operand1)
        else:
            self.check_binary_operation(node)

    def check_binary_operation(self, node):
        self.check_operand(node.operand1)
        self.check_operand(node.operand2)
        if node.type in ['DIV', 'MOD']:
            if hasattr(node.operand2, 'value') and node.operand2.value == 0:
                raise Exception("Erreur sémantique: Division par zéro")

    def check_operand(self, operand):
        if isinstance(operand, Variable):
            symbol = self.symbol_table.lookup(operand.name)
            if not symbol:
                raise Exception(f"Erreur sémantique: Variable '{operand.name}' non déclarée")
        elif isinstance(operand, ArrayAccess):
            symbol = self.symbol_table.lookup(operand.name)
            if not symbol:
                raise Exception(f"Erreur sémantique: Tableau '{operand.name}' non déclaré")
            if symbol.type != 'array':
                raise Exception(f"Erreur sémantique: '{operand.name}' n'est pas un tableau")
            self.check_array_index(operand.index, symbol)

    def check_array_index(self, index, array_symbol):
        if isinstance(index, Number):
            if index.value < 0 or index.value >= array_symbol.size:
                raise Exception(f"Erreur sémantique: Index hors limites pour le tableau '{array_symbol.name}'")
        elif isinstance(index, Variable):
            if not self.symbol_table.lookup(index.name):
                raise Exception(f"Erreur sémantique: Variable d'index '{index.name}' non déclarée")

    def check_jump_target(self, target):
        if not isinstance(target, int):
            raise Exception("Erreur sémantique: La cible du saut doit être un nombre")

    def check_procedure_call(self, procedure):
        if not isinstance(procedure, Variable):
            raise Exception("Erreur sémantique: L'argument de CALL doit être un identifiant")
        if not self.symbol_table.lookup(procedure.name):
            raise Exception(f"Erreur sémantique: Procédure '{procedure.name}' non déclarée")

    def verify_jump_labels(self):
        for instruction in self.symbol_table.instruction_labels:
            if not self.symbol_table.has_instruction(instruction):
                raise Exception(f"Erreur sémantique: Label d'instruction {instruction} non défini")

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'Pas de méthode visit_{type(node).__name__}') 