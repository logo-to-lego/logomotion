"""Main module for the compiler.
"""
from lexer.lexer import Lexer

# from parser.parser import parser

PROG = """foo 4 + 2 - 1 for make "foo 5 [ ] { } :test %
make forward if show
; foo show
oikealle 4 / 2"""

lexer = Lexer()
lexer.build(debug=True)
lexer.get_lexer().input(PROG)

for token in lexer.get_lexer():
    print(token)

# parser.parse(code, lexer=lexer)
