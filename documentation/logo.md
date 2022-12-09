# Logo

This document contains the rules of the Logo language that is used in this project.
The language itself is a variant of Logo, so some rules might differ from the "usual" Logo language.

## Variables

A variable is defined with the keyword `make` (or in Finnish `tee`) and writing `"` before the variable name. The value of a variable is given after the declaring
of the variable's name. For example for variable x we can declare a value 42 in the following way
`make "x 42`

A variable is referenced with a colon. For example for variable x, we can output its value with the commands `show`, `print`, `sano` or `tulosta`. Here's an example of the usage of the command show.
`show :x`

A variable's type cannot be changed later on. The following example below produces an error:

```
make "x 10
make "x "message
ERROR
```

## Functions

Functions have their own scope and variables defined outside of a function can not be used within a function, unless the said variables are given to the function as parameters.
Here is an example of function foo, which prints the value it has received as its parameter.
```
TO foo :n
    show :n
END
```

The function above can be called with a variable. Example of a variable called x:

```
MAKE "x 42
foo :x
```

***It is not possible*** to define or call a function with a global variable because variables defined outside of the function are not visible within the function. Example:

```
TO foo
    show :x
END

MAKE "x 42
foo
ERROR
```

`FOR` loops are defined in the following way:

```
for ["a 1 2 3] {}
for ["a 0 10 1] { show :a}
```
The first argument is an iterator, the second argument is the start value of the iterator, third argument is the end value of the iterator and the fourth value represents a step of a cycle. For example a step of 2 would go 0, 2, 4 and so on. The actions performed within a for-loop are defined within the '{}' brackets.

## Scopes

Variables defined on a global scale are not visible within functions. Functions' inner or own variables are not visible on a global scale.

Variables defined within conditional statements are not visible outside of the condition statements. A conditional statement is still capable of using a variable of upper scope, for example a global variable.
## Conditional Statements

The code below defines a variable called `x` with the value 42. If the value of the variable `x` is below 100 the value is printed:
```
make "x 42
if :x < 100 {
    print :x
}
```

This shows that variables outside of a conditional statement can be referenced in a conditional statement. Conditional statements still have their own scope, this means that within conditional statements, it is possible to still define its own variables which in turn are not visible outside of the conditional statement. The following snippet of code will produce an error, because the variable y is referenced outside of the conditional statement.
```
make "x 42
if :x < 100 {
    make "y 123
}
show :y
ERROR
```


## Mathematical operations

Mathematical operations are possible to do only with a variable of type `FLOAT`. Operations that are possible are `+`, `-`, `*` and `/`

## Relational operations

Variables of type `FLOAT` are comparable with each other with the operators `<`, `<=`, `>`, `>=`, `=` and `<>`.

`STRING` variables can be compared with each other only by using the operators `=` and `<>`.

## Case sensitivity

Variables, commands, function names and other referenced types of information are all case insensitive. For example:

```
make "x 42
```

The variable `x` is now defined with lowercase letters, but can be referenced in upper case in the future:

```
show :X
```

The only exception to case insensitivity is with string literals. This means that if a string literal is printed by using the command `show`, it should be printed the way it is written. Example:

```
show "Cat
show "cat
show "cAt
```
All of the prints differ from each other and are case sensitive.