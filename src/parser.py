from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Union, List, Optional
from lexer import Token
from rich import print


class ReprMixin:
    def __repr__(self):
        attrs = []
        for field_name, value in self.__dict__.items():
            if value is not None:
                attrs.append(f"{field_name}={repr(value)}")
        return f"{self.__class__.__name__}({', '.join(attrs)})"


@dataclass(repr=False)
class Assignment(ReprMixin):
    lineno: int
    location: Location
    symbol: Literal["="]
    expression: Expression


@dataclass(repr=False)
class Vardecl(ReprMixin):
    lineno: int
    mut: Literal["var", "const"]
    id: str
    type: Optional[str] = None
    assignment: Optional[Literal["="]] = None
    expression: Optional[Expression] = field(default_factory=lambda: None)
    initialized: bool = False  # Indica si la variable ha sido inicializada


@dataclass(repr=False)
class FuncDecl(ReprMixin):
    lineno: int
    id: str
    return_type: str
    statements: List[Statement]
    parameters: Optional[Parameters] = None


@dataclass(repr=False)
class IfStmt(ReprMixin):
    lineno: int
    expression: Expression
    if_statement: List[Statement] = field(default_factory=list)
    else_statement: List[Statement] = field(default_factory=list)


@dataclass(repr=False)
class WhileStmt(ReprMixin):
    lineno: int
    expression: Expression
    statement: List[Statement] = field(default_factory=list)


@dataclass(repr=False)
class BreakStmt(ReprMixin):
    lineno: int


@dataclass(repr=False)
class ContinueStmt(ReprMixin):
    lineno: int


@dataclass(repr=False)
class ReturnStmt(ReprMixin):
    lineno: int
    expression: Expression


@dataclass(repr=False)
class PrintStmt(ReprMixin):
    lineno: int
    expression: Expression


@dataclass(repr=False)
class Parameters(ReprMixin):
    lineno: int
    id: str
    type: str
    next: Optional[Parameters] = None
    mut = "var"


@dataclass(repr=False)
class Location(ReprMixin):
    lineno: int
    id: Optional[str] = None
    expression: Optional[Expression] = None

    def __post_init__(self):
        if self.id is not None and self.expression is not None:
            raise ValueError(
                "Location no puede tener ambos 'id' y 'expression' establecidos."
            )
        if self.id is None and self.expression is None:
            raise ValueError("Location debe tener 'id' o 'expression' establecidos.")


@dataclass(repr=False)
class Expression(ReprMixin):
    lineno: int
    orterm: OrTerm
    symbol: Optional[str] = None
    next: Optional[Expression] = None


@dataclass(repr=False)
class OrTerm(ReprMixin):
    lineno: int
    andterm: AndTerm
    symbol: Optional[str] = None
    next: Optional[OrTerm] = None


@dataclass(repr=False)
class AndTerm(ReprMixin):
    lineno: int
    relTerm: RelTerm
    symbol: Optional[str] = None
    next: Optional[AndTerm] = None


@dataclass(repr=False)
class RelTerm(ReprMixin):
    lineno: int
    addTerm: AddTerm
    symbol: Optional[str] = None
    next: Optional[RelTerm] = None


@dataclass(repr=False)
class AddTerm(ReprMixin):
    lineno: int
    factor: Factor
    symbol: Optional[str] = None
    next: Optional[AddTerm] = None


@dataclass(repr=False)
class Factor(ReprMixin):
    lineno: int
    literal: Optional[str] = None
    type: Optional[str] = None
    id: Optional[str] = None
    arguments: Optional[List[Expression]] = None
    location: Optional[Location] = None
    unary_expression: Optional[Factor] = None
    unary_op: Optional[str] = None
    expression: Optional[Expression] = None


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


@dataclass(repr=False)
class Program(ReprMixin):
    lineno: int
    statements: List[Statement]


@dataclass(repr=False)
class RecursiveDescentParser(ReprMixin):
    tokens: List[Token]
    indexToken: int

    def program(self) -> Program:
        program = []
        while self.indexToken < len(self.tokens):
            statement = self.statement()
            program.append(statement)

            if self.token_type() == "EOF":
                break

        if not program:
            raise ValueError("No se encontraron declaraciones en el programa.")
        if self.token_type() != "EOF":
            raise ValueError(
                f"El programa no terminó correctamente. {self.current_token().lineno}"
            )

        return Program(statements=program, lineno=self.current_token().lineno)

    def statement(self) -> Statement:
        if self.token_type() == "ID":
            next_type = self.next_token().type
            if next_type == "ASSIGN":
                return self.assignment()

        if self.token_type() == "FUNC":
            return self.func_decl()

        if self.current_token().value in {"var", "const"}:
            return self.vardecl()

        if self.token_type() == "IF":
            return self.if_stmt()

        if self.token_type() == "WHILE":
            return self.while_stmt()

        if self.token_type() == "BREAK":
            return self.break_stmt()

        if self.token_type() == "CONTINUE":
            return self.continue_stmt()

        if self.token_type() == "RETURN":
            return self.return_stmt()

        if self.token_type() == "PRINT":
            return self.print_stmt()

        raise ValueError(f"El statement no es válido. {self.current_token().lineno}")

    def assignment(self) -> Assignment:
        location = Location(
            id=self.current_token().value, lineno=self.current_token().lineno
        )
        self.indexToken += 2
        expression = self.expression()

        if self.token_type() != "SEMI":
            raise ValueError(
                f"El statement no terminó correctamente. Se esperaba ';'. {self.current_token().lineno}"
            )
        self.indexToken += 1

        return Assignment(
            location=location,
            symbol="=",
            expression=expression,
            lineno=self.current_token().lineno,
        )

    def vardecl(self) -> Vardecl:
        token_value = self.current_token().value
        if token_value not in ("var", "const"):
            raise ValueError(f"Expected 'var' or 'const', got {token_value}")
        mut: Literal["var", "const"] = token_value
        type = None
        assignment = None
        expression = None
        self.indexToken += 1

        if self.token_type() == "ID":
            id = self.current_token().value
            self.indexToken += 1

            if self.token_type() == "TYPE":
                type = self.current_token().value
                self.indexToken += 1

            if self.current_token().value == "=":
                assignment = "="
                self.indexToken += 1
                expression = self.expression()

        else:
            raise ValueError(f"ID no válido. {self.current_token().lineno}")

        if self.token_type() != "SEMI":
            raise ValueError(
                f"El statement no terminó correctamente. Se esperaba ';'. {self.current_token().lineno}"
            )
        self.indexToken += 1

        return Vardecl(
            id=id,
            mut=mut,
            type=type,
            assignment=assignment,
            expression=expression,
            lineno=self.current_token().lineno,
        )

    def func_decl(self) -> FuncDecl:
        self.indexToken += 1

        id = self.current_token().value
        self.indexToken += 1

        if self.token_type() != "LPAREN":
            raise ValueError(f"Se esperaba '('. {self.current_token().lineno}")
        self.indexToken += 1

        parameters: Parameters | None = None
        if self.token_type() != "RPAREN":
            parameters = self.parameters()

        if self.token_type() != "RPAREN":
            raise ValueError(f"Se esperaba ')'. {self.current_token().lineno}")
        self.indexToken += 1

        if self.token_type() != "TYPE":
            raise ValueError(
                f"Se esperaba un tipo de retorno. {self.current_token().lineno}"
            )
        return_type = self.current_token().value
        self.indexToken += 1

        if self.token_type() != "LBRACE":
            raise ValueError(
                "Se esperaba '{' para el bloque de la función.",
                self.current_token().lineno,
            )
        self.indexToken += 1

        statements = self.block()

        return FuncDecl(
            id=id,
            parameters=parameters,
            return_type=return_type,
            statements=statements,
            lineno=self.current_token().lineno,
        )

    def if_stmt(self) -> IfStmt:
        self.indexToken += 1
        expression = self.expression()

        if self.token_type() != "LBRACE":
            raise ValueError(
                "Se esperaba '{' para el bloque if.", self.current_token().lineno
            )
        self.indexToken += 1

        if_statement = self.block()

        else_statement = []
        if self.token_type() == "ELSE":
            self.indexToken += 1
            if self.token_type() != "LBRACE":
                raise ValueError(
                    "Se esperaba '{' para el bloque else.", self.current_token().lineno
                )
            self.indexToken += 1
            else_statement = self.block()

        return IfStmt(
            expression=expression,
            if_statement=if_statement,
            else_statement=else_statement,
            lineno=self.current_token().lineno,
        )

    def while_stmt(self) -> WhileStmt:
        self.indexToken += 1
        expression = self.expression()

        if self.token_type() != "LBRACE":
            raise ValueError(
                "Se esperaba '{' para el bloque while.", self.current_token().lineno
            )
        self.indexToken += 1

        statement = self.block()
        return WhileStmt(
            expression=expression,
            statement=statement,
            lineno=self.current_token().lineno,
        )

    def break_stmt(self) -> BreakStmt:
        self.indexToken += 1  # Consumir 'BREAK'

        if self.token_type() != "SEMI":
            raise ValueError(
                "Se esperaba ';' después de 'break'.", self.current_token().lineno
            )
        self.indexToken += 1  # Consumir ';'

        return BreakStmt(lineno=self.current_token().lineno)

    def continue_stmt(self) -> ContinueStmt:
        self.indexToken += 1
        if self.token_type() != "SEMI":
            raise ValueError(
                "Se esperaba ';' después de 'continue'.", self.current_token().lineno
            )
        self.indexToken += 1
        return ContinueStmt(lineno=self.current_token().lineno)

    def return_stmt(self) -> ReturnStmt:
        self.indexToken += 1
        expression = self.expression()

        if self.token_type() != "SEMI":
            raise ValueError(
                "Se esperaba ';' después de 'return'.", self.current_token().lineno
            )
        self.indexToken += 1

        return ReturnStmt(expression=expression, lineno=self.current_token().lineno)

    def print_stmt(self) -> PrintStmt:
        self.indexToken += 1
        expression = self.expression()

        if self.token_type() != "SEMI":
            raise ValueError(
                "Se esperaba ';' después de 'print'.", self.current_token().lineno
            )
        self.indexToken += 1

        return PrintStmt(expression=expression, lineno=self.current_token().lineno)

    def block(self) -> list[Statement]:
        """Parsea un bloque de código entre llaves `{ ... }`."""
        statements = []
        while self.token_type() != "RBRACE":
            statements.append(self.statement())

        if self.token_type() != "RBRACE":
            raise ValueError(
                "Se esperaba '}' al final del bloque.", self.current_token().lineno
            )
        self.indexToken += 1

        return statements

    def parameters(self) -> Parameters:
        if self.token_type() != "ID":
            raise ValueError(
                "Se esperaba un identificador.", self.current_token().lineno
            )

        id = self.current_token().value
        self.indexToken += 1

        if self.token_type() != "TYPE":
            raise ValueError(
                "Se esperaba un tipo de dato.", self.current_token().lineno
            )

        type = self.current_token().value
        self.indexToken += 1

        next = None

        if self.token_type() == "COMMA":
            self.indexToken += 1
            next = self.parameters()

        return Parameters(
            id=id, type=type, next=next, lineno=self.current_token().lineno
        )

    def arguments(self) -> list[Expression]:
        args = []

        # Si el siguiente token es RPAREN, significa que no hay argumentos (caso vacío)
        if self.token_type() == "RPAREN":
            return args  # Retorna lista vacía

        # Agregar el primer argumento
        args.append(self.expression())

        # Procesar argumentos adicionales separados por comas
        while self.token_type() == "COMMA":
            self.indexToken += 1  # Consumir la coma
            args.append(self.expression())

        return args

    def expression(self) -> Expression:
        orterm = self.orterm()
        symbol = None
        next: Optional[Expression] = None

        if self.token_type() == "LOR":
            symbol = self.current_token().value
            self.indexToken += 1
            next = self.expression()

        return Expression(
            orterm=orterm,
            symbol=symbol,
            next=next,
            lineno=self.current_token().lineno,
        )

    def orterm(self) -> OrTerm:
        andterm = self.andterm()
        symbol = None
        next: Optional[OrTerm] = None
        if self.token_type() == "LAND":
            symbol = self.current_token().value
            self.indexToken += 1
            next = self.orterm()

        return OrTerm(
            andterm=andterm,
            symbol=symbol,
            next=next,
            lineno=self.current_token().lineno,
        )

    def andterm(self) -> AndTerm:
        relTerm = self.relTerm()
        symbol = None
        next: Optional[AndTerm] = None

        if self.current_token().value in {"<", ">", "==", "!=", "<=", ">="}:
            symbol = self.current_token().value
            self.indexToken += 1
            next = self.andterm()

        return AndTerm(
            relTerm=relTerm,
            symbol=symbol,
            next=next,
            lineno=self.current_token().lineno,
        )

    def relTerm(self) -> RelTerm:
        addTerm = self.addTerm()
        symbol = None
        next: Optional[RelTerm] = None

        if self.current_token().value in {"+", "-"}:
            symbol = self.current_token().value
            self.indexToken += 1
            next = self.relTerm()

        return RelTerm(
            addTerm=addTerm,
            symbol=symbol,
            next=next,
            lineno=self.current_token().lineno,
        )

    def addTerm(self) -> AddTerm:
        factor = self.factor()
        symbol = None
        next: Optional[AddTerm] = None

        if self.current_token().value in {"*", "/"}:
            symbol = self.current_token().value
            self.indexToken += 1
            next = self.addTerm()

        return AddTerm(
            factor=factor, symbol=symbol, next=next, lineno=self.current_token().lineno
        )

    def factor(self) -> Factor:
        if self.token_type() == "ID":
            id = self.current_token().value
            arguments = None
            self.indexToken += 1

            if self.token_type() == "LPAREN":
                self.indexToken += 1
                arguments = self.arguments()
                if self.token_type() != "RPAREN":
                    raise ValueError("Se esperaba un ')'.", self.current_token().lineno)
                self.indexToken += 1

            return Factor(
                id=id, arguments=arguments, lineno=self.current_token().lineno
            )

        if self.current_token().value in {"+", "-", "^"}:
            unary_op = self.current_token().value
            self.indexToken += 1
            factor = self.factor()
            return Factor(
                unary_expression=factor,
                unary_op=unary_op,
                lineno=self.current_token().lineno,
            )

        if self.token_type() in {"INTEGER", "FLOAT", "CHAR", "BOOL"}:
            literal = self.current_token().value
            self.indexToken += 1
            return Factor(literal=literal, lineno=self.current_token().lineno)

        if self.token_type() == "LPAREN":
            self.indexToken += 1  # Consumir '('
            expr = self.expression()
            if self.token_type() != "RPAREN":
                raise ValueError(f"Se esperaba ')'. {self.current_token().lineno}")
            self.indexToken += 1  # Consumir ')'
            return Factor(
                expression=expr,
                lineno=self.current_token().lineno,
            )

        else:
            raise ValueError("Factor no puede ser vacío.", self.current_token().lineno)

    def current_token(self) -> Token:
        return self.tokens[self.indexToken]

    def next_token(self) -> Token:
        return self.tokens[self.indexToken + 1]

    def token_type(self) -> str:
        return self.tokens[self.indexToken].type

    def _rest_value(self):
        print("resto", self.tokens[self.indexToken :])
