*** Settings ***
Resource  resource.robot


*** Variables *** 
${TYPE_LOGO}    type.logo
${TYPE_JAVA}    type.java

${BINOPS_LOGO}    binops.logo
${BINOPS_JAVA}    binops.java

${RELOPS_LOGO}    relops.logo
${RELOPS_JAVA}    relops.java


*** Test Cases ***
Make Variables In All Types
    Compile Logo  ${TYPE_LOGO}
    Java Is Valid  ${TYPE_JAVA}
    Java Compiles

All Binary Operations
    Compile Logo  ${BINOPS_LOGO}
    Java Is Valid  ${BINOPS_JAVA}
    Java Compiles

All Relative Operations
    Compile Logo  ${RELOPS_LOGO}
    Java Is Valid  ${RELOPS_JAVA}
    Java Compiles
