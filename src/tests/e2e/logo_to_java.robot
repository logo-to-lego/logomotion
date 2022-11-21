*** Settings ***
Resource  resource.robot
Library  OperatingSystem


*** Variables *** 
${MOVE_LOGO}    move.logo
${MOVE_JAVA}    move.java

${TYPE_LOGO}    type.logo
${TYPE_JAVA}    type.java


*** Test Cases ***
Move In All Directions
    Compile Logo  ${MOVE_LOGO}
    Java Is Valid  ${MOVE_JAVA}
    Java Compiles

Make Variables In All Types
    Compile Logo  ${TYPE_LOGO}
    Java Is Valid  ${TYPE_JAVA}
    Java Compiles