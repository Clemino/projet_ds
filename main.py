from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.compiler_to_c import CCompiler
import subprocess

def main():
    print("Compilateur Assembleur - Exécution du fichier source:")
    try:
        with open('examples/test.projet', 'r') as file:
            source_code = file.read()
        
        print("\nCode source:")
        print(source_code)
        
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(ast)
        
        compiler = CCompiler(ast, semantic_analyzer.symbol_table)
        compiler.save_to_file("output.c")
        
        print("\nCode C généré dans 'output.c'")
    except Exception as e:
        print(f'Erreur: {e}')

if __name__ == "__main__":
    main()
