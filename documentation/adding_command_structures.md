# Command structures

Also known as premade functions. This document will cover how to add new functions/command structures. Regrettably the code is currently fairly spread out so that you'll have to touch the following parts:

- Lexer: lexer.py, token_types.py
- Parser
- preconfigured_functions.py
- preconf_code_generator.py

## Note about structure and a refactoring suggestion

The structure is currently very spread out. Authors suggest that command structures ought to be refactored so that they exists within one file. The suggested method is: a list is created similarly to parser/preparser.py's export_grammar_rules function and it is passed to parser in parse/parser.py's _build function. There the functions can be added to global scope, and ought to work as they do now, just that the structure would be concise.

## How to add new 

### Lexer

Add the relevant token to token_types.py. Then if you want to call it with similar name, add the calls to lexer.py reserved_words dictionary.

### Parser

Currently repeat (and for) exist in parser/command.py, but choose the file according to your needs. You'll need to create a rule so that parser understands you command structure. Create the relevant node, likely ProcCall.

### Preconfigured_functions

1. Create a function
    - Returns a function class instance
    - Has the relevant params as Variable instances, which are given relevant types.
    - Has the correct name
    - Has the correct typeclass
2. Add the just made function to preconfigured_functions.py's initialize_logo_functions functions similarly as is done to for and repeat. 

### Preconf_code_generator.py

Repeat and for will end up as functions within the same class just outside of main. Here you ought to add a function that returns the relevant java code as string. Don't forget to add the created function to get_funcs dictionary.
If you look at the java code, functions added here show up as `func1` and `func2` etc.

## Current command structures

### General

Repeat should work. There have been some issues with for parsing. We think that there should be a new type for the control-list part that is

`for ["i 1 2 3] {...}`

the part that is noted by [...] should be its own type like a control-list.

## For

The way we've handled being able to touch the iterator in java is that we create a DoubleVariable just outside the lambda, that acts as the iterator. You can find this in unknown_function.py generate_code function. 