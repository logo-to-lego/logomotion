"""Main module for the compiler.
"""
from lexer.lexer import Lexer

# from parser.parser import parser

lexer = Lexer()
lexer.build(debug=True)
lexer.get_lexer().input('foo 4 + 2 - 1 for make "foo 5 [ ] { } :test % make forward if')

for token in lexer.get_lexer():
    print(token)

# parser.parse(code, lexer=lexer)
