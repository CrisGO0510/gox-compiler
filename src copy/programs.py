# programs.py
#
# En las entrañas de su compilador, debe representar programas
# como estructuras de datos. En este archivo, codificará manualmente
# algunos programas goxlang simples usando el modelo de datos que
# se ha desarrollado en el archivo goxlang/model.py
#
# El propósito de este ejercicio es doble:
#
# 1. Asegúrese de comprender el modelo de datos de su compilador.
# 2. Tenga algunas estructuras de programas que pueda usar para pruebas
# y experimentación posteriores.
#
# Este archivo está dividido en secciones. Siga las instrucciones para
# cada parte. Es posible que se haga referencia a partes de este archivo
# en partes posteriores del proyecto. Planifique tener muchos debates.
#
from parser import *

# ---------------------------------------------------------------------
# Expression Simple
#
# Esto se le da a usted como un ejemplo

expr_source = "2 + 3 * 4"

expr_model = RelTerm(
    addTerm=AddTerm(factor=Factor(literal="2"), next=None),
    symbol="+",
    next=AddTerm(factor=Factor(literal="3"), symbol="*", next=Factor(literal="4")),
)
# ---------------------------------------------------------------------
# Programa 1: Printing
#
# Codifique el siguiente programa el cual prueba la impresión y expresion simple
#
source1 = """
    print 2 + 3 * -4;
    print 2.0 - 3.0 / -4.0;
    print -2 + 3;
"""

model1 = Program(
    [
        PrintStmt(
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(literal="2"),
                                symbol="+",
                                next=AddTerm(
                                    factor=Factor(literal="3"),
                                    symbol="*",
                                    next=Factor(literal="-4"),
                                ),
                            )
                        )
                    )
                )
            )
        ),
        PrintStmt(
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(literal="2.0"),
                                symbol="-",
                                next=AddTerm(
                                    factor=Factor(literal="3.0"),
                                    symbol="/",
                                    next=Factor(literal="-4.0"),
                                ),
                            )
                        )
                    )
                )
            )
        ),
        PrintStmt(
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(literal="-2"),
                                symbol="+",
                                next=Factor(literal="3"),
                            )
                        )
                    )
                )
            )
        ),
    ]
)

# ---------------------------------------------------------------------
# Programa 2: Declaración de Variables y Constantes.
#            Expresiones y Asignaciones
#
# Codifique la siguiente sentencia.

source2 = """
    const pi = 3.14159;
    var tau float;
    tau = 2.0 * pi;
    print(tau);
"""

model2 = Program(
    [
        Vardecl(
            id="pi",
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(factor=Factor(literal="3.14159"))
                        )
                    )
                )
            ),
        ),
        Vardecl(
            id="tau",
            type="float",
            mut=True,
        ),
        Assignment(
            location=Location(
                id="tau",
            ),
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(literal="2.0"),
                                symbol="*",
                                next=Factor(literal="pi"),
                            )
                        )
                    )
                )
            ),
        ),
        PrintStmt(
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(id="tau"),
                            )
                        )
                    )
                )
            )
        ),
    ]
)

# ---------------------------------------------------------------------
# Programa 3: Condicionales. Este programa imprime el mínimo de
#            dos valores
#
# Codifique la siguiente sentencia.

source3 = """
    var a int = 2;
    var b int = 3;
    if a < b {
        print a;
    } else {
        print b;
    }
"""

model3 = Program(
    [
        Vardecl(
            id="a",
            type="int",
            mut=True,
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(literal="2"),
                            )
                        )
                    )
                )
            ),
        ),
        Vardecl(
            id="b",
            type="int",
            mut=True,
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(literal="3"),
                            )
                        )
                    )
                )
            ),
        ),
        IfStmt(
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(id="a"),
                                symbol="<",
                                next=Factor(id="b"),
                            )
                        )
                    )
                )
            ),
            if_statement=PrintStmt(
                expression=Expression(
                    orterm=OrTerm(
                        andterm=AndTerm(
                            relTerm=RelTerm(
                                addTerm=AddTerm(
                                    factor=Factor(id="a"),
                                )
                            )
                        )
                    )
                )
            ),
            else_statement=PrintStmt(
                expression=Expression(
                    orterm=OrTerm(
                        andterm=AndTerm(
                            relTerm=RelTerm(
                                addTerm=AddTerm(
                                    factor=Factor(id="b"),
                                )
                            )
                        )
                    )
                )
            ),
        ),
    ]
)

# ---------------------------------------------------------------------
# Programa 4: Ciclos.  Este programa imprime los primeros 10 factoriales.
#
source4 = """
    const n = 10;
    var x int = 1;
    var fact int = 1;

    while x < n {
        fact = fact * x;
        print fact;
        x = x + 1;
    }
"""

model4 = Program(
    [
        Vardecl(
            id="n",
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(addTerm=AddTerm(factor=Factor(literal="10")))
                    )
                )
            ),
        ),
        Vardecl(
            id="x",
            type="int",
            mut=True,
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(addTerm=AddTerm(factor=Factor(literal="1")))
                    )
                )
            ),
        ),
        Assignment(
            location=Location(id="fact"),
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(addTerm=AddTerm(factor=Factor(literal="1")))
                    )
                )
            ),
        ),
        WhileStmt(
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(id="x"),
                                symbol="<",
                                next=Factor(id="n"),
                            )
                        )
                    )
                )
            ),
            statement=[
                Assignment(
                    location=Location(id="fact"),
                    expression=Expression(
                        orterm=OrTerm(
                            andterm=AndTerm(
                                relTerm=RelTerm(
                                    addTerm=AddTerm(
                                        factor=Factor(id="fact"),
                                        symbol="*",
                                        next=Factor(id="x"),
                                    )
                                )
                            )
                        )
                    ),
                ),
                PrintStmt(
                    expression=Expression(
                        orterm=OrTerm(
                            andterm=AndTerm(
                                relTerm=RelTerm(
                                    addTerm=AddTerm(
                                        factor=Factor(id="fact"),
                                    )
                                )
                            )
                        )
                    ),
                ),
                Assignment(
                    location=Location(id="x"),
                    expression=Expression(
                        orterm=OrTerm(
                            andterm=AndTerm(
                                relTerm=RelTerm(
                                    addTerm=AddTerm(
                                        factor=Factor(id="x"),
                                        symbol="+",
                                        next=Factor(literal="1"),
                                    )
                                )
                            )
                        )
                    ),
                ),
            ],
        ),
    ]
)

# ---------------------------------------------------------------------
# Programa 5: Funciones (simple)
#
source5 = """
    func square(x int) int {
        return x*x;
    }

    print square(4);
    print square(10);
"""

model5 = Program(
    [
        FuncDecl(
            id="square",
            parameters=Parameters(
                id="x",
                type="int",
            ),
            statements=[
                ReturnStmt(
                    expression=Expression(
                        orterm=OrTerm(
                            andterm=AndTerm(
                                relTerm=RelTerm(
                                    addTerm=AddTerm(
                                        factor=Factor(id="x"),
                                        symbol="*",
                                        next=Factor(id="x"),
                                    )
                                )
                            )
                        )
                    )
                )
            ],
        ),
        PrintStmt(
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(id="square"),
                                arguments=Arguments(
                                    expression=Expression(
                                        orterm=OrTerm(
                                            andterm=AndTerm(
                                                relTerm=RelTerm(
                                                    addTerm=AddTerm(
                                                        factor=Factor(literal="4"),
                                                    )
                                                )
                                            )
                                        )
                                    )
                                ),
                            )
                        )
                    )
                )
            )
        ),
        PrintStmt(
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(id="square"),
                                arguments=Arguments(
                                    expression=Expression(
                                        orterm=OrTerm(
                                            andterm=AndTerm(
                                                relTerm=RelTerm(
                                                    addTerm=AddTerm(
                                                        factor=Factor(literal="10"),
                                                    )
                                                )
                                            )
                                        )
                                    )
                                ),
                            )
                        )
                    )
                )
            )
        ),
    ]
)

# ---------------------------------------------------------------------
# Programa 6: Funciones (complejas)
#
source6 = """
    func fact(n int) int {
        var x int = 1;
        var result int = 1;
        while x < n {
            result = result * x;
            x = x + 1;
        }
        return result;
    }

    print(fact(10));
"""

model6 = Program(
    {
        FuncDecl(
            id="fact",
            parameters=Parameters(
                id="n",
                type="int",
            ),
            return_type="int",
            statements=[
                Vardecl(
                    id="x",
                    type="int",
                    mut=True,
                    expression=Expression(
                        orterm=OrTerm(
                            andterm=AndTerm(
                                relTerm=RelTerm(
                                    addTerm=AddTerm(factor=Factor(literal="1"))
                                )
                            )
                        )
                    ),
                ),
                Vardecl(
                    id="result",
                    type="int",
                    mut=True,
                    expression=Expression(
                        orterm=OrTerm(
                            andterm=AndTerm(
                                relTerm=RelTerm(
                                    addTerm=AddTerm(factor=Factor(literal="1"))
                                )
                            )
                        )
                    ),
                ),
                WhileStmt(
                    expression=Expression(
                        orterm=OrTerm(
                            andterm=AndTerm(
                                relTerm=RelTerm(
                                    addTerm=AddTerm(
                                        factor=Factor(id="x"),
                                        symbol="<",
                                        next=Factor(id="n"),
                                    )
                                )
                            )
                        )
                    ),
                    statement=[
                        Assignment(
                            location=Location(id="result"),
                            expression=Expression(
                                orterm=OrTerm(
                                    andterm=AndTerm(
                                        relTerm=RelTerm(
                                            addTerm=AddTerm(
                                                factor=Factor(id="result"),
                                                symbol="*",
                                                next=Factor(id="x"),
                                            )
                                        )
                                    )
                                )
                            ),
                        ),
                        Assignment(
                            location=Location(id="x"),
                            expression=Expression(
                                orterm=OrTerm(
                                    andterm=AndTerm(
                                        relTerm=RelTerm(
                                            addTerm=AddTerm(
                                                factor=Factor(id="x"),
                                                symbol="+",
                                                next=Factor(literal="1"),
                                            )
                                        )
                                    )
                                )
                            ),
                        ),
                    ],
                ),
                ReturnStmt(
                    expression=Expression(
                        orterm=OrTerm(
                            andterm=AndTerm(
                                relTerm=RelTerm(
                                    addTerm=AddTerm(
                                        factor=Factor(id="result"),
                                    )
                                )
                            )
                        )
                    )
                ),
            ],
        ),
        PrintStmt(
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(id="fact"),
                                arguments=Arguments(
                                    expression=Expression(
                                        orterm=OrTerm(
                                            andterm=AndTerm(
                                                relTerm=RelTerm(
                                                    addTerm=AddTerm(
                                                        factor=Factor(literal="10"),
                                                    )
                                                )
                                            )
                                        )
                                    )
                                ),
                            )
                        )
                    )
                )
            )
        ),
    }
)

# ---------------------------------------------------------------------
# Programa 7: Conversión de tipos
#
source7 = """
    var pi = 3.14159;
    var spam = 42;

    print(spam * int(pi));
    print(float(spam) * pi;)
    print(int(spam) * int(pi));
"""

model7 = Program(
    [
        Vardecl(
            id="pi",
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(factor=Factor(literal="3.14159"))
                        )
                    )
                )
            ),
        ),
        Vardecl(
            id="spam",
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(addTerm=AddTerm(factor=Factor(literal="42")))
                    )
                )
            ),
        ),
        PrintStmt(
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(id="spam"),
                                symbol="*",
                                next=Factor(
                                    literal="int(pi)",
                                ),
                            )
                        )
                    )
                )
            )
        ),
        PrintStmt(
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(literal="float(spam)"),
                                symbol="*",
                                next=Factor(id="pi"),
                            )
                        )
                    )
                )
            )
        ),
        PrintStmt(
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(literal="int(spam)"),
                                symbol="*",
                                next=Factor(literal="int(pi)"),
                            )
                        )
                    )
                )
            )
        ),
    ]
)

# ---------------------------------------------------------------------
# Programa 8: Acceso a memoria
#
source8 = """
    var x int = ^8192;      // Incrementa memoria por 8192 bytes
    var addr int = 1234;
    `addr = 5678;           // Almacena 5678 en addr
    print(`addr + 8);
"""

model8 = Program(
    [
        Vardecl(
            id="x",
            type="int",
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(literal="^8192"),
                            )
                        )
                    )
                )
            ),
        ),
        Vardecl(
            id="addr",
            type="int",
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(literal="1234"),
                            )
                        )
                    )
                )
            ),
        ),
        Assignment(
            location=Location(id="`addr"),
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(literal="5678"),
                            )
                        )
                    )
                )
            ),
        ),
        PrintStmt(
            expression=Expression(
                orterm=OrTerm(
                    andterm=AndTerm(
                        relTerm=RelTerm(
                            addTerm=AddTerm(
                                factor=Factor(id="`addr"),
                                symbol="+",
                                next=Factor(literal="8"),
                            )
                        )
                    )
                )
            )
        ),
    ]
)
