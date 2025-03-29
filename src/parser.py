from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Union, List, Optional
from lexer import Token


@dataclass
class Assignment:
    location: Location
    symbol: Literal["="]
    expression: Expression


@dataclass
class Vardecl:
    mut: Literal["var", "const"]
    id: str
    type: Optional[str] = None
    assignment: Optional[Literal["="]] = None
    expression: Optional[Expression] = field(default_factory=lambda: None)


@dataclass
class FuncDecl:
    id: str
    parameters: Parameters
    return_type: str
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
    type: str
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
    orSymbol: Optional[str] = None
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
    symbol: Optional[str] = None
    next: Optional[AddTerm] = None


@dataclass
class AddTerm:
    factor: Factor
    symbol: Optional[str] = None
    next: Optional[Factor] = None


@dataclass
class Factor:
    literal: Optional[str] = None
    expression: Optional[Expression] = None
    type: Optional[str] = None
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


@dataclass
class RecursiveDescentParser:
    tokens: List[Token]
    indexToken: int

    def program(self) -> Program:
        return Program(statements=self.statement())

    def statement(self) -> Statement:
        if self.current_token().type == "ID" and self.next_token().type == "ASSIGN":
            return self.assignment()

        if self.current_token().value in {"var", "const"}:
            return self.vardecl()

        # if self.current_token().value == "return":
        #     return self.return_stmt()

        raise ValueError("El statement no es válido.")

    def assignment(self) -> Assignment:
        location = Location(id=self.current_token().value)
        self.indexToken += 2
        expression = self.expression()
        return Assignment(location=location, symbol="=", expression=expression)

    def return_stmt(self) -> ReturnStmt:
        self.indexToken += 1
        expression = self.expression()
        return ReturnStmt(expression=expression)

    def vardecl(self) -> Vardecl:
        mut = self.current_token().value
        isConst = mut == "const"
        type = None
        assignment = None
        expression = None
        self.indexToken += 1

        if self.current_token().type == "ID":
            id = self.current_token().value
            self.indexToken += 1

            # Verificar si tiene un tipo en caso de que no sea constante

            if self.current_token().type == "TYPE":
                type = self.current_token().value
                self.indexToken += 1
            elif not isConst:
                raise ValueError("La variable necesita un tipo de dato.")

            if self.current_token().value == "=":
                assignment = self.current_token().value
                self.indexToken += 1
                expression = self.expression()

        else:
            raise ValueError("ID no válido.")

        return Vardecl(
            id=id, mut=mut, type=type, assignment=assignment, expression=expression
        )

    def expression(self) -> Expression:
        orterm = self.orterm()
        orSymbol = None
        next = None

        print(self.current_token())

        if self.current_token().type == "LOR":
            orSymbol = self.current_token().value
            self.indexToken += 1
            next = self.orterm()

        return Expression(orterm=orterm, orSymbol=orSymbol, next=next)

    def orterm(self) -> OrTerm:
        andterm = self.andterm()
        return OrTerm(andterm=andterm)

    def andterm(self) -> AndTerm:
        relTerm = self.relTerm()
        return AndTerm(relTerm=relTerm)

    def relTerm(self) -> RelTerm:
        if self.next_token().type == "PLUS" or self.next_token().type == "MINUS":
            addTerm = self.addTerm()

            # Guardar el símbolo y avanzar el índice del token
            symbol = self.current_token().value
            self.indexToken += 1

            nextAddTerm = self.addTerm()
            return RelTerm(addTerm, symbol, nextAddTerm)
        addTerm = self.addTerm()
        return RelTerm(addTerm=addTerm)

    def addTerm(self) -> AddTerm:
        factor = self.factor()
        return AddTerm(factor=factor)

    def factor(self) -> Factor:
        if self.current_token().type == "INTEGER":
            literal = self.current_token().value
            self.indexToken += 1
            return Factor(literal=literal)
        if self.current_token().type == "TIMES":
            self.indexToken += 1
            return Factor(expression=self.expression())
        else:
            raise ValueError("Factor no puede ser vacío.")

    def current_token(self) -> Token:
        return self.tokens[self.indexToken]

    def next_token(self) -> Token:
        return self.tokens[self.indexToken + 1]
