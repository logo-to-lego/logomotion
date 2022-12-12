*** Settings ***
Library  ../../AppLibrary.py


*** Variables *** 
${MAKE_LOGO}    basic_operations/make.logo
${BINOPS_LOGO}  basic_operations/binops.logo
${RELOPS_LOGO}  basic_operations/relops.logo
${MOVE_LOGO}    basic_operations/move.logo

*** Test Cases ***
Make Variables In All Types
    Compile Logo  ${MAKE_LOGO}
    Java Compiles

All Binary Operations
    Compile Logo  ${BINOPS_LOGO}
    Java Compiles

All Relative Operations
    Compile Logo  ${RELOPS_LOGO}
    Java Compiles

Move In All Directions
    Compile Logo  ${MOVE_LOGO}
    Java Compiles
