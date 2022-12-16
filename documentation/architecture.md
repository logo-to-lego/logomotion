# Architecture

This file is a work in progress. Headings follow the folder structure of the project. The aim of this document is to describe the architecture of Logo-To-Lego project in detail so that it is easier to keep developing the project to a capable compiler for the Logo programming language.

## Class Diagram
![Class Diagram](https://github.com/logo-to-lego/logomotion/blob/main/documentation/pictures/logomotion_architecture.png)

## Lexer

### Token_types.py
Define token types here.

### Lexer.py
Contains `class Lexer`
Define word representations for lex tokens. Forbidden characters also defined here. 

## Parser

### Command.py
Parsing rules for function calls, command structures, logo specific commands.

### Expression.py
Parsing rules for expressions: binop, relop, uminus, numbers, bools, references (derefs), things that reduce to expressions.  

### Globals.py
Contains:
- Precedence rules for operations. 
- `class Position` which is used for error highlighting.
- Shared wrapper for exposing lexer, console_io, symbol tables, and error_handler to parser functions.

### Parser.py
Contains the parser class, which uses the PLY parser.
Contains rules for start, statement_list, empty and error.

### Preparser.py
Provides preparsing of functions, which are then given to parser.py.

## Ply

### lex.py

### yacc.py

## Tests

### Unit testing

### End-to-End testing
End-to-End tests are done with Robot Framework. They are used for compiling the generated java. I.e. they compile a logo file and check that the generated java code compiles.

The tests are located in [src/tests/e2e](https://github.com/logo-to-lego/logomotion/tree/main/src/tests/e2e) and [AppLibrary.py](https://github.com/logo-to-lego/logomotion/blob/main/src/AppLibrary.py) handles the Robot Framework function calls.

## Utils
Contains logger, error_handler and lowercase_converter.

## Logo

## Other architectural comments
