from __future__ import annotations
from dataclasses import dataclass, field
from typing import Union, List, Optional
from enum import Enum


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
    imported: bool = False
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
