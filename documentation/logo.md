# Logo

This document contains the syntax and grammar of the Logo variant that is used in this project. Some rules may differ from the typical Logo language.

- [Data types and syntax](#data-types-and-syntax)
- [Debugging](#debugging)
- [Moving the robot](#moving-the-robot)
- [Mathematical operations](#mathematical-operations)
- [Unary operations](#unary-operations)
- [Relational operations](#relational-operations)
- [Conditional statements](#conditional-statements)
    - [About the scope of conditional statements](#about-the-scope-of-conditional-statements)
- [Variables](#variables)
    - [Variable declaration](#variable-declaration)
    - [About typing](#about-typing)
- [Procedures](#procedures)
    - [Procedure declaration](#procedure-declaration)
    - [Procedure call](#procedure-call)
    - [Output](#output)
    - [About parameter typing](#about-parameter-typing)
    - [About the scope of procedures](#about-the-scope-of-procedures)
- [Loops](#loops)
    - [About the scope of loops](#about-the-scope-of-loops)
- [Scopes](#scopes)
- [Case insensitivity](#case-sensitivity)

## Data types and syntax

***"string***\
***'string***\
***number***\
***boolean***

*Example*
```
show "word
show 'word
show 1.23
show 1,23
show true
show false
```

***:variable***

*Example*
```
show :variable
```

***( expression )***\
Parentheses can be used to group expressions.

*Example*
```
show (1 + 2) * 3
```

***procedure param***\
Call a procedure with the default number of parameteres.

*Example*
```
show "word
```

***( procedure param ... )***\
Call a procedure that supports an arbitrary number of parameters.

*Example*
```
(show "hello "world)
```

## Debugging
### show
`show` can be used to print out various values. `show` will always print with a line break, even when given multiple inputs.

*Example*
```
show "hello
-> hello

show "hello
show "hi
-> hello
-> hi

(show "hello "hi)
-> hello
-> hi
```

## Moving the robot
For instructions on how to set up your EV3 brick, see [Instructions](https://github.com/logo-to-lego/logomotion/blob/main/documentation/instructions.md).

***forward expr***\
***fd expr***\
Move forward *expr* units.

***backward expr***\
***bk expr***\
Move backward *expr* units.

***left expr***\
***lt expr***\
Turn left *expr* degrees.

***right expr***\
***rt expr***\
Turn right *expr* degrees.

*Example*
```
fd 100
rt 90
bk 100
lt 90
make "x 200
forward :x
```

## Mathematical operations

Mathematical operations are possible to do only with an expression of type `FLOAT`. Operations that are possible are `+`, `-`, `*` and `/`

***expr + expr***\
sum

***expr - expr***\
subtract

***expr * expr***\
multiply

***expr / expr***\
divide

## Unary operations

The only unary operator denotes a negative number, and hence only works with expressions of type `FLOAT`.

***( - number )***\
***( - ( expr ) )***

*Example*
```
show (-1)
show (-(1 + 2))
```

## Relational operations

Expressions of type `FLOAT` are comparable with each other with the operators `<`, `<=`, `>`, `>=`, `=` and `<>`.

`STRING` expressions can be compared with each other only by using the operators `=` and `<>`.

***expr < expr***\
less than

***expr <= expr***\
less than or equal

***expr > expr***\
greater than

***expr >= expr***\
greater than or equal

***expr = expr***\
equal

***expr <> expr***\
not equal

## Conditional statements

***if expr { statements }***\
Run *statements* if *expr* is true.

*Example*
```
if :x > 999 { show "large }
```

***ifelse expr { statements1 } { statements2 }***\
Run *statements1* if *expr* is true. Otherwise run *statements2*.

*Example*
```
ifelse :x > 999 { show "large } { show "small }
```

### About the scope of conditional statements
Variables outside of a conditional statement can be referenced in a conditional statement.
```
make "x 42
if :x < 100 {
    show :x
}
```

Conditional statements still have their own scope. This means that variables defined within a conditional statement are not visible outside of it.

The following snippet of code will produce an error, because the variable *y* is referenced outside of the conditional statement.
```
make "x 42
if :x < 100 {
    make "y 123
}
show :y
-> ERROR
```

## Variables
A variable is defined with the keyword `make` and writing `"` or `'` before the variable name. The value of a variable is given after declaring
the variable's name. For variable x we can declare a value 42 in the following way: `make "x 42`

Referring to variables happens with `:` in front of the variable name, `:variable` as defined in [Data types and syntax](#data-types-and-syntax). For example, to refer to variable *x* above: `show :x` 

### Variable declaration
***make "varname expr***\
Create a variable named *varname* and assign *expr* as its value.

*Example*
```
make "a 42
```

### About typing
Variables are assigned a type (*number*, *string* or *boolean*) based on the type of its assigned value. This Logo variant is statically typed, i.e. you cannot change a variable's type after assignment.

*Example*
```
make "x 10
make "x "message
-> ERROR
```

## Procedures

### Procedure declaration
***to procname :params ... statements ... end***

*Example: Procedure **foo** doubles the numeric value it has received as its parameter **n** and prints the result.*
```
TO foo :n
    show :n*2
END
```

The procedure above can be called with a variable. Example of a variable called x:

```
MAKE "x 42
foo :x
```

### Procedure call
***procname args***

*Example: Run procedure **proc** with string **"string**, variable **:variable** and number **2.5** as arguments.*
```
proc "string :variable 2.5
```

### Output
***output***\
Use inside a procedure declaration's *statements* to have the procedure put out a value.

*Example: Procedure **square** puts out its parameter **x** squared.*
```
TO square :x
    output :x * :x
END
```

This value can be used in the same way as any other value.
```
make "x square 2
make "y (square 2) + 5
if 10 < square 5 {}
```

### About parameter typing
You must be able to determine the procedure parameter types from your code or it won't compile. Most often this can be done by reassigning the parameter value with `make` or using [Mathematical operations](#mathematical-operations) and [Relational operations](#relational-operations).

*Example: Code that won't compile and a suggested fix.*
```
TO foo :x
    show :x
END
-> Type of :x is not defined
```
```
TO foo :x
    show :x+0
END
```

### About the scope of procedures
Procedures have their own closed scopes. It is not possible to refer to an outside variable from within a procedure.
```
make "x 10
TO foo
    output :x
END
-> ERROR, :x is not defined
```
Similarly, it is not possible to refer to a variable defined within a procedure outside of it.
```
TO foo
    make "x 10
END
    show :x
-> ERROR, :x is not defined
```

## Loops
***repeat expr { statements }***\
Run *statements* *expr* times.

*Example*
```
repeat 10 { fd 20 }
```

***for [ "variable expr expr expr ] { statements }***\
Typical **for** loop. The arguments inside the square brackets are, in order, *iterable*, *start*, *limit* and *step*.

*Iterable* is created as a new local variable and can be referred to within the for loop in the same way as other variables.

*Start* is the value the *iterable* starts at.

*Limit* is the value the *iterable* ends at. Inclusive.

*Step* is the value added to *iterable* after each loop of *statements*.

*Example: Count to 10*
```
for ["a 1 10 1] { show :a }
```

*Example: Print out the multiplication table of 2*
```
for ["a 2 20 2] { show :a }
```

### About the scope of loops

Similar to the [Scope of conditional statements](#about-the-scope-of-conditional-statements), variables defined outside of the loops can be used inside them
```
make "x 10
repeat 10 { show :x }
for ["i 1 10 1] { show :x }
```
and variables defined inside the loops cannot be used outside of them.
```
repeat 10 { make "x 10 }
for ["i 1 10 1] { make "y 10 }
show :x
-> ERROR, :x is not defined
show :y
-> ERROR, :y is not defined
```
A **for** loop's iterable variable can only be used within its own scope.
```
for ["i 1 10 1] { show :i }

show :i
-> ERROR, :i is not defined
```

## Scopes

To sum up the scopes:

Variables defined on a global scale are not visible within [Procedures](#procedures). Procedures' inner or own variables are not visible on a global scale.

Variables defined within [Conditional statements](#conditional-statements) and [Loops](#loops) are not visible outside of them. However, they are still capable of using a variables of an upper scope. For example, a global variable.

## Case sensitivity

Variables, commands, function names and other referenced types of information are all case insensitive. For example:

```
make "x 42
```

The variable `x` is now defined with lowercase letters, but can be referenced in upper case later:

```
show :X
-> 42
```

String literals are the only exception to case insensitivity.

```
show "cat = "CAT
-> false
```