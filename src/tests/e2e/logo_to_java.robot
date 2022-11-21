*** Settings ***
Resource  resource.robot
Library  OperatingSystem


*** Variables *** 
${MOVE_LOGO}    move.logo
${MOVE_JAVA}    move.java


*** Test Cases ***
Move In All Directions
    Compile Logo  ${MOVE_LOGO}
    Java Is Valid  ${MOVE_JAVA}
    Java Compiles