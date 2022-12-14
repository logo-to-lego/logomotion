*** Settings ***
Library  ../../AppLibrary.py


*** Variables *** 
${PRECONF_FUNCS}    functions/preconf_funcs.logo
${USER_DEFINED_FUNCS}    functions/user_defined_functions.logo

*** Test Cases ***
Preconf Functions
    Compile Logo  ${PRECONF_FUNCS}
    Java Compiles

User-Defined Functions
    Compile Logo  ${USER_DEFINED_FUNCS}
    Java Compiles

    

