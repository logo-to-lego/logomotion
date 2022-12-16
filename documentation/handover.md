# Handover document

## Stuff that we know that is currently broken and suggestions for fixing

### For
For seems to work with simple cases but we suspect that it won't work with more complex cases.

** add code which breaks for **

Suggestion is to add a new concept to handle for's 'control list' that is the ["i 1 2 3]. This would make it possible/easier to handle fors without step argument etc. Likely to require parsing rules, new Logotype, new node.

### Loops inside conditional statement
When using loops inside conditional statements, the logo code compiles, but the compiled java is not valid. 

```
if (true) {
    for ["i 0 20 1] {
        fd 42
    }
}
```

```
if (true) {
    repeat 4 {
        fd 42
    }
}
```

The function call in java should be surrounded with a try/catch block.
```
try {
    this.func1(temp, temp);
} catch (ReturnException error) {
    System.out.println("An unidentified error occurred.");
}
```

This requires fixes in [code_generator](https://github.com/logo-to-lego/logomotion/tree/main/src/code_generator).

## Open brances

### typeconcat_bug_fix

The logo below cannot concatenate typeclasses, since variable a is not defined in the symbol table after the if-statement ends.
```
TO f :x
    make "b :x
    if true {
        make "a :x
        make "a 1
    }
    make "b :x
END
```

Branch [typeconcat_bug_fix](https://github.com/logo-to-lego/logomotion/tree/typeconcat_bug_fix) fixes this but it's not properly tested. All unittests pass and everything should work normally, but making a PR during the last day was a bit too much of a risk.

### Parsing-errors
