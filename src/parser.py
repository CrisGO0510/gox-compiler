from __future__ import annotations
from dataclasses import dataclass, field
from typing import Union, List, Optional
from enum import Enum

from lexer import Token


class Type(Enum):
    INT = "int"
    FLOAT = "float"
    CHAR = "char"
    BOOL = "bool"


@dataclass
class Assignment:
    location: Location
    expression: Expression


@dataclass
class Vardecl:
    id: str
    type: Optional[Type] = None
    expression: Optional[Expression] = field(default_factory=lambda: None)


@dataclass
class FuncDecl:
    id: str
    parameters: Parameters
    return_type: Type
    statements: List[Statement]


@dataclass
class IfStmt:
    expression: Expression
    if_statement: List[Statement] = field(default_factory=list)
    else_statement: List[Statement] = field(default_factory=list)


@dataclass
class WhileStmt:
    expression: Expression
    statement: List[Statement] = field(default_factory=list)


@dataclass
class BreakStmt:
    pass


@dataclass
class ContinueStmt:
    pass


@dataclass
class ReturnStmt:
    expression: Expression


@dataclass
class PrintStmt:
    expression: Expression


@dataclass
class Parameters:
    id: str
    type: Type
    next: Optional[Parameters] = None


@dataclass
class Location:
    id: Optional[str] = None
    expression: Optional[Expression] = None

    def __post_init__(self):
        if self.id is not None and self.expression is not None:
            raise ValueError(
                "Location no puede tener ambos 'id' y 'expression' establecidos."
            )
        if self.id is None and self.expression is None:
            raise ValueError("Location debe tener 'id' o 'expression' establecidos.")


@dataclass
class Expression:
    orterm: OrTerm
    next: Optional[OrTerm] = None


@dataclass
class OrTerm:
    andterm: AndTerm
    next: Optional[AndTerm] = None


@dataclass
class AndTerm:
    relTerm: RelTerm
    next: Optional[RelTerm] = None


@dataclass
class RelTerm:
    addTerm: AddTerm
    next: Optional[AddTerm] = None


@dataclass
class AddTerm:
    factor: Factor
    next: Optional[Factor] = None


@dataclass
class Factor:
    literal: Optional[Type] = None
    expression: Optional[Expression] = None
    type: Optional[Type] = None
    id: Optional[str] = None
    arguments: Optional[Arguments] = None
    location: Optional[Location] = None


@dataclass
class Arguments:
    expression: Expression
    next: Optional[Arguments] = None


Statement = Union[
    Assignment,
    Vardecl,
    FuncDecl,
    IfStmt,
    WhileStmt,
    BreakStmt,
    ContinueStmt,
    ReturnStmt,
    PrintStmt,
]


@dataclass
class Program:
    statements: List[Statement]


a = Program(
    statements=[
        ReturnStmt(
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(literal=2), next=Factor(literal=3)
                            )
                        )
                    )
                )
            )
        )
    ]
)


@dataclass
class RecursiveDescentParser:
    tokens: List[Token]
    indexToken: int

    def program(self) -> Program:
        return Program(statements=self.statement())

    def statement(self) -> Statement:
        if self.tokens[self.indexToken].value == "return":
            return self.return_stmt()
        elif self.tokens[self.indexToken].value == "int":
            return self.vardecl()
        else:
            return self.assignment()

    def return_stmt(self) -> ReturnStmt:
        self.indexToken += 1
        expression = self.expression()
        return ReturnStmt(expression=expression)

    def expression(self) -> Expression:
        orterm = self.orterm()
        return Expression(orterm=orterm)

    def orterm(self) -> OrTerm:
        andterm = self.andterm()
        return OrTerm(andterm=andterm)

    def andterm(self) -> AndTerm:
        relTerm = self.relTerm()
        return AndTerm(relTerm=relTerm)

    def relTerm(self) -> RelTerm:
        addTerm = self.addTerm()
        return RelTerm(addTerm=addTerm)

    def addTerm(self) -> AddTerm:
        factor = self.factor()
        return AddTerm(factor=factor)

    def factor(self) -> Factor:
        if self.tokens[self.indexToken].type == "INTEGER":
            literal = self.tokens[self.indexToken].value
            self.indexToken += 1
            return Factor(literal=literal)
        if self.tokens[self.indexToken].type == "TIMES":
            self.indexToken += 1
            return Factor(expression=self.expression())
        else:
            raise ValueError("Factor no puede ser vacío.")
