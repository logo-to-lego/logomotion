# Tests miscellaneous logo programs, that test all features we have implemented

*** Settings ***
Library  ../../AppLibrary.py


*** Variables *** 
${PROG1}    logo_programs/prog1.logo
${PROG2}    logo_programs/prog2.logo
${PROG3}    logo_programs/prog3.logo

*** Test Cases ***
Prog1
    Compile Logo  ${PROG1}
    Java Compiles

Prog2
    Compile Logo  ${PROG2}
    Java Compiles

Prog3
    Compile Logo  ${PROG3}
    Java Compiles
