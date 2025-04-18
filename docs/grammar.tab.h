/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_GRAMMAR_TAB_H_INCLUDED
# define YY_YY_GRAMMAR_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    VAR = 258,                     /* VAR  */
    CONST = 259,                   /* CONST  */
    FUNC = 260,                    /* FUNC  */
    IF = 261,                      /* IF  */
    ELSE = 262,                    /* ELSE  */
    WHILE = 263,                   /* WHILE  */
    BREAK = 264,                   /* BREAK  */
    CONTINUE = 265,                /* CONTINUE  */
    PRINT = 266,                   /* PRINT  */
    RETURN = 267,                  /* RETURN  */
    IMPORT = 268,                  /* IMPORT  */
    INT = 269,                     /* INT  */
    FLOAT = 270,                   /* FLOAT  */
    CHAR = 271,                    /* CHAR  */
    BOOL = 272,                    /* BOOL  */
    INTEGER_LITERAL = 273,         /* INTEGER_LITERAL  */
    FLOAT_LITERAL = 274,           /* FLOAT_LITERAL  */
    CHAR_LITERAL = 275,            /* CHAR_LITERAL  */
    BOOL_LITERAL = 276,            /* BOOL_LITERAL  */
    IDENTIFIER = 277,              /* IDENTIFIER  */
    ASSIGN = 278,                  /* ASSIGN  */
    SEMI = 279,                    /* SEMI  */
    COMMA = 280,                   /* COMMA  */
    LPAR = 281,                    /* LPAR  */
    RPAR = 282,                    /* RPAR  */
    LBRACE = 283,                  /* LBRACE  */
    RBRACE = 284,                  /* RBRACE  */
    PLUS = 285,                    /* PLUS  */
    MINUS = 286,                   /* MINUS  */
    TIMES = 287,                   /* TIMES  */
    DIVIDE = 288,                  /* DIVIDE  */
    GROW = 289,                    /* GROW  */
    LT = 290,                      /* LT  */
    GT = 291,                      /* GT  */
    LE = 292,                      /* LE  */
    GE = 293,                      /* GE  */
    EQ = 294,                      /* EQ  */
    NE = 295,                      /* NE  */
    LAND = 296,                    /* LAND  */
    LOR = 297,                     /* LOR  */
    NOT = 298,                     /* NOT  */
    DEREF = 299,                   /* DEREF  */
    UMINUS = 300,                  /* UMINUS  */
    EOF = 301                      /* EOF  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 9 "grammar.y"

    int    intval;
    float  floatval;
    char*  strval;

#line 116 "grammar.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_GRAMMAR_TAB_H_INCLUDED  */
