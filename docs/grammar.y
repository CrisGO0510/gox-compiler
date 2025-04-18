%{
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "grammar.tab.h"

extern int yylex(); // Declaración de la función yylex
extern int yyerror(const char *s); // Declaración de la función yyerror
%}

%union {
    int intval;
    float floatval;
    char charval;
    bool boolval;
    char* id;
}

/* Palabras clave de control */
%token IF ELSE WHILE BREAK CONTINUE

/* Palabras clave de declaración */
%token VAR CONST FUNC

/* Palabras clave integradas */
%token PRINT RETURN IMPORT

/* Literales */
%token <intval> INTEGER_LITERAL
%token <floatval> FLOAT_LITERAL
%token <charval> CHAR_LITERAL
%token <boolval> TRUE FALSE

/* Identificadores */
%token <id> ID

/* Tipos */
%token INT FLOAT CHAR BOOL

/* Operadores de dos caracteres */
%token LE GE EQ NE
%token LAND LOR

/* Operadores de un caracter */
%token PLUS       // +
%token MINUS      // -
%token TIMES      // *
%token DIVIDE     // /
%token LT         // <
%token GT         // >
%token GROW       // ^
%token ASSIGN     // =
%token SEMI       // ;
%token COMMA      // ,
%token LPAREN     // (
%token RPAREN     // )
%token LBRACE     // {
%token RBRACE     // }
%token DEREF      // `
%token NOT        // !

// /* Fin de archivo */
// %token End_Of_File

/* Definición de precedencia y asociatividad */

%left LOR
%left LAND
%left LT GT LE GE EQ NE
%left PLUS MINUS
%left TIMES DIVIDE
%left GROW
%%

program:
    statements
    ;

statements:
    /* Epsilon */
    | statements statement
    ;

statement:
      assignment
    | vardecl
    | funcdecl
    | if_stmt
    | while_stmt
    | BREAK SEMI
    | CONTINUE SEMI
    | RETURN expression SEMI
    | PRINT expression SEMI
    ;

assignment:
    ID ASSIGN expression SEMI ;

vardecl:
      VAR ID type init_opt SEMI
    | CONST ID type init_opt SEMI
    | CONST ID init_opt SEMI
    ;

init_opt:
      /* Epsilon */
    | ASSIGN expression
    ;

funcdecl:
      FUNC ID LPAREN parameters RPAREN type LBRACE statements RBRACE
    | IMPORT FUNC ID LPAREN parameters RPAREN type LBRACE statements RBRACE
    ;

if_stmt:
      IF expression LBRACE statements RBRACE
    | IF expression LBRACE statements RBRACE ELSE LBRACE statements RBRACE
    ;

while_stmt:
      WHILE expression LBRACE statements RBRACE
    ;

parameters:
     /* Epsilon */
    | ID type
    | parameters COMMA ID type
    ;

type:
      INT
    | FLOAT
    | CHAR
    | BOOL
    ;

expression:
      orterm
    | expression LOR orterm
    ;

orterm:
      andterm
    | orterm LAND andterm
    ;

andterm:
      relterm
    | andterm LT relterm
    | andterm GT relterm
    | andterm LE relterm
    | andterm GE relterm
    | andterm EQ relterm
    | andterm NE relterm
    ;

relterm:
      addterm
    | relterm PLUS addterm
    | relterm MINUS addterm
    ;

addterm:
      factor
    | addterm TIMES factor
    | addterm DIVIDE factor
    ;

factor:
      literal
    | PLUS expression
    | MINUS expression
    | GROW expression
    | LPAREN expression RPAREN
    | type LPAREN expression RPAREN
    | ID LPAREN arguments RPAREN
    | ID
    ;

arguments:
      /* Epsilon */
    | expression
    | arguments COMMA expression
    ;

literal:
      INTEGER_LITERAL
    | FLOAT_LITERAL
    | CHAR_LITERAL
    | TRUE
    | FALSE
    ;
%%
