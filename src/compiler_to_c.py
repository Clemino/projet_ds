import subprocess
import os
from .token import TokenType
from .ast import Number, Variable, Register, ArrayAccess

class CCompiler:
    def __init__(self, ast, symbol_table):
        self.ast = ast
        self.symbol_table = symbol_table
        self.c_code = []
        self.indent = 0

    def generate_c_code(self):
        code = [
            "#include <stdio.h>",
            "#include <stdint.h>",
            "#include <stdlib.h>",
            "",
            "#define STACK_SIZE 1024",
            "",
            "int16_t AX = 0, BX = 0, CX = 0, DX = 0;",
            "int16_t stack[STACK_SIZE];",
            "int stack_ptr = 0;",
            ""
        ]

        for name, symbol in self.symbol_table.symbols.items():
            if symbol.type == 'byte':
                code.append(f"int16_t {name} = 0;")
            elif symbol.type == 'array':
                code.append(f"int16_t {name}[{symbol.size}];")
        code.append("")

        code.extend([
            "void push(int16_t value) {",
            "    if (stack_ptr < STACK_SIZE) {",
            "        stack[stack_ptr++] = value;",
            "    }",
            "}",
            "",
            "int16_t pop(void) {",
            "    if (stack_ptr > 0) {",
            "        return stack[--stack_ptr];",
            "    }",
            "    return 0;",
            "}",
            ""
        ])

        code.append("int main(void) {")
        
        for instr in self.ast.instructions:
            if instr.operation:
                code.append(self.compile_instruction(instr))
        
        code.extend([
            "    return 0;",
            "}"
        ])

        return "\n".join(code)

    def compile_instruction(self, instruction):
        if not instruction.operation:
            return ""

        op = instruction.operation
        code = [f"L{instruction.number}:"]

        if op.type == TokenType.MOV:
            dest = self.compile_operand(op.operand1)
            src = self.compile_operand(op.operand2)
            code.append(f"    {dest} = {src};")

        elif op.type == TokenType.ADD:
            dest = self.compile_operand(op.operand1)
            src = self.compile_operand(op.operand2)
            code.append(f"    {dest} += {src};")

        elif op.type == TokenType.SUB:
            dest = self.compile_operand(op.operand1)
            src = self.compile_operand(op.operand2)
            code.append(f"    {dest} -= {src};")

        elif op.type == TokenType.INPUT:
            dest = self.compile_operand(op.operand1)
            code.append(f"    printf(\"Input: \");")
            code.append(f"    scanf(\"%hd\", &{dest});")

        elif op.type == TokenType.PRINT:
            src = self.compile_operand(op.operand1)
            code.append(f"    printf(\"%hd\\n\", {src});")

        elif op.type == TokenType.JMP:
            code.append(f"    goto L{op.operand1.value};")

        elif op.type == TokenType.JZ:
            code.append(f"    if (AX == 0) goto L{op.operand1.value};")

        return "\n".join(code)

    def compile_operand(self, operand):
        if isinstance(operand, Number):
            return str(operand.value)
        elif isinstance(operand, Variable):
            return operand.name
        elif isinstance(operand, Register):
            return operand.name
        elif isinstance(operand, ArrayAccess):
            index = self.compile_operand(operand.index)
            return f"{operand.name}[{index}]"
        return ""

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            f.write(self.generate_c_code())

