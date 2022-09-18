# pylint: disable=invalid-name
"""Parsing rules and globals used by the parser"""

precedence = (
    ("left", "PLUS", "MINUS"),
    ("left", "MUL", "DIV"),
    ("right", "UMINUS"),
)


names = {}

reserved_words = {}

start = "start"
