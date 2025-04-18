%{
#include <stdbool.h> 
#include "grammar.tab.h"
%}

%%

"if"                { return IF; }
"else"              { return ELSE; }
"while"             { return WHILE; }
"break"             { return BREAK; }
"continue"          { return CONTINUE; }
"return"            { return RETURN; }
"print"             { return PRINT; }
"import"            { return IMPORT; }
"var"               { return VAR; }
"const"             { return CONST; }
"func"              { return FUNC; }

[0-9]+              { yylval.intval = atoi(yytext); return INTEGER_LITERAL; }
[0-9]+\.[0-9]+      { yylval.floatval = atof(yytext); return FLOAT_LITERAL; }
\'[^\']\'           { yylval.charval = yytext[1]; return CHAR_LITERAL; }
"true"              { yylval.boolval = true; return TRUE; }
"false"             { yylval.boolval = false; return FALSE; }

[a-zA-Z_][a-zA-Z0-9_]* { yylval.id = strdup(yytext); return ID; }

"+"                 { return PLUS; }
"-"                 { return MINUS; }
"*"                 { return TIMES; }
"/"                 { return DIVIDE; }
"<"                 { return LT; }
">"                 { return GT; }
"="                 { return ASSIGN; }
";"                 { return SEMI; }
","                 { return COMMA; }
"("                 { return LPAREN; }
")"                 { return RPAREN; }
"{"                 { return LBRACE; }
"}"                 { return RBRACE; }

.                   { return yytext[0]; }

%%
