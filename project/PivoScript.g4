grammar PivoScript;

program: statement* ;

statement
    : varDecl
    | assignment ';'
    | output
    | ifStatement
    | forStatement
    ;

varDecl: 'dejmi' IDENTIFIER ('=' expr)? ';' ;

output: 'kecni' '(' expr ')' ';' ;

ifStatement: 'hele' '(' condition ')' block ('jinac' block)? ;

forStatement: 'jestejedno' '(' varDecl condition ';' assignment ')' block ;

block: '{' statement* '}' ;

assignment
    : IDENTIFIER '=' expr
    ;

condition
    : logicalOr
    ;

logicalOr
    : logicalAnd ('nebojak' logicalAnd)*
    ;

logicalAnd
    : logicalNot ('tojejasny' logicalNot)*
    ;

logicalNot
    : 'nenekamo' logicalNot
    | comparison
    ;

comparison
    : expr ('==' | '<' | '>') expr
    | '(' condition ')'
    ;

expr
    :   term (( '+' | '-' ) term)*    # addSubExpr
    ;

term
    :   factor (( '*' | '/' ) factor)* # mulDivExpr
    ;

factor
    :   '-' factor                    # negExpr
    |   INT                           # intExpr
    |   BINARY                        # binaryExpr
    |   HEX                           # hexExpr
    |   STRING                        # stringExpr
    |   IDENTIFIER                    # idExpr
    |   '(' expr ')'                  # parensExpr
    ;

IDENTIFIER: [a-zA-Z_][a-zA-Z_0-9]* ;
INT: [0-9]+ ;
BINARY: '0b' [01]+ ;
HEX: '0x' [0-9a-fA-F]+ ;
STRING: '"' (~["\r\n])* '"' ;

WS: [ \t\r\n]+ -> skip ;
