from rich import print
from typing import List
from functools import singledispatchmethod
from parser import *


class IRModule:
    def __init__(self):
        self.functions: dict[str, IRFunction] = {}
        self.globals = {}

    def dump(self):
        print("MODULE:::")
        for glob in self.globals.values():
            glob.dump()
        for func in self.functions.values():
            func.dump()


class IRGlobal:
    def __init__(self, name, type, value=None):
        self.name = name
        self.type = type
        self.value = value

    def dump(self):
        mapped_type = IRType.getTypeMap(self.type)
        if self.value is not None:
            print(f"GLOBAL::: {self.name} {mapped_type} {self.value}")
        else:
            print(f"GLOBAL::: {self.name} {mapped_type}")


class IRInstruction:
    """Representa una instrucción en el código intermedio"""

    def __init__(self, opcode: str, *args):
        self.opcode = opcode
        self.args = args

    def __repr__(self):
        return str((self.opcode, *self.args))


class IRFunction:
    def __init__(self, module, name, parmnames, parmtypes, return_type, imported=False):
        self.module = module
        module.functions[name] = self
        self.name = name
        self.parmnames = parmnames
        self.parmtypes = parmtypes
        self.return_type = return_type
        self.imported = imported
        self.locals = {}
        self.code: List[IRInstruction] = []

    def dump(self):
        mapped_parmtypes = [IRType.getTypeMap(t) for t in self.parmtypes]
        mapped_return_type = IRType.getTypeMap(self.return_type)

        print(
            f"\nFUNCTION::: {self.name}, {self.parmnames}, {mapped_parmtypes} {mapped_return_type}"
        )
        mapped_locals = {
            name: IRType.getTypeMap(type) for name, type in self.locals.items()
        }

        print(f"locals: {mapped_locals}")
        for instr in self.code:
            print(instr)


class IRType:
    _typemap = {
        "int": "I",
        "float": "F",
        "bool": "I",
        "char": "I",
    }

    _binop_code = {
        ("int", "+", "int"): "ADDI",
        ("int", "-", "int"): "SUBI",
        ("int", "*", "int"): "MULI",
        ("int", "/", "int"): "DIVI",
        ("int", "<", "int"): "LTI",
        ("int", "<=", "int"): "LEI",
        ("int", ">", "int"): "GTI",
        ("int", ">=", "int"): "GEI",
        ("int", "==", "int"): "EQI",
        ("int", "!=", "int"): "NEI",
        ("float", "+", "float"): "ADDF",
        ("float", "-", "float"): "SUBF",
        ("float", "*", "float"): "MULF",
        ("float", "/", "float"): "DIVF",
        ("float", "<", "float"): "LTF",
        ("float", "<=", "float"): "LEF",
        ("float", ">", "float"): "GTF",
        ("float", ">=", "float"): "GEF",
        ("float", "==", "float"): "EQF",
        ("float", "!=", "float"): "NEF",
        ("char", "<", "char"): "LTI",
        ("char", "<=", "char"): "LEI",
        ("char", ">", "char"): "GTI",
        ("char", ">=", "char"): "GEI",
        ("char", "==", "char"): "EQI",
        ("char", "!=", "char"): "NEI",
    }

    @classmethod
    def getTypeMap(cls, type: str) -> str:
        if type in cls._typemap:
            return cls._typemap[type]
        else:
            raise Exception(f"Tipo {type} no soportado")

    @classmethod
    def getConst(cls, type: str) -> str:
        if type in cls._typemap:
            return "CONST" + cls._typemap[type]
        else:
            raise Exception(f"Tipo {type} no soportado")

    @classmethod
    def getPrint(cls, type: str) -> str:
        if type in cls._typemap:
            return "PRINT" + cls._typemap[type]
        else:
            raise Exception(f"Tipo {type} no soportado")

    @classmethod
    def getBinOpCode(cls, type: str, op: str) -> str:
        if (type, op, type) in cls._binop_code:
            return cls._binop_code[(type, op, type)]
        else:
            raise Exception(f"Operador {op} no soportado para el tipo {type}")


class IRCode:
    def __init__(self):
        pass

    def gencode(self, program: Program) -> IRModule:
        module = IRModule()
        IRFunction(module, "main", [], [], "int")

        for stmt in program.statements:
            print(f"Processing {stmt}")
            self.statement(stmt, module)

        return module

    @singledispatchmethod
    def statement(self, stmt, module: IRModule):
        raise NotImplementedError(
            f"No hay un handler implementado para el tipo {type(stmt).__name__}\n"
        )

    @statement.register
    def _(self, stmt: FuncDecl, module: IRModule):
        print("Handling function declaration")
        if stmt.id == "main":
            stmt.id = "_actual_main"
            instr = [IRInstruction("CALL", "_actual_main"), IRInstruction("RET")]
            module.functions["main"].code = instr

        param_names = []
        param_types = []
        current_param = stmt.parameters
        while current_param:
            param_names.append(current_param.id)
            param_types.append(current_param.type)
            current_param = current_param.next

        func = IRFunction(
            module,
            stmt.id,
            param_names,
            param_types,
            stmt.return_type,
        )

        for instruction in stmt.statements:
            print(f"Processing {instruction}")
            self.statement(instruction, func)

    @statement.register
    def _(self, stmt: Vardecl, ctx):
        if isinstance(ctx, IRFunction):
            ctx.locals[stmt.id] = stmt.type

            if stmt.expression is not None:
                assignment = Assignment(
                    lineno=stmt.lineno,
                    location=Location(lineno=stmt.lineno, id=stmt.id),
                    symbol="=",
                    expression=stmt.expression,
                )
                self.statement(assignment, ctx)

        elif isinstance(ctx, IRModule):
            func: IRFunction = IRFunction(
                IRModule(),
                stmt.id,
                [],
                [],
                stmt.type,
            )

            self.statement(stmt.expression, func)
            ctx.globals[stmt.id] = IRGlobal(stmt.id, stmt.type, func.code[0].args[0])

    @statement.register
    def _(self, stmt: Assignment, func: IRFunction):
        self.statement(stmt.expression, func)
        instr = IRInstruction("LOCAL_SET", stmt.location.id)
        func.code.append(instr)

    @statement.register
    def _(self, stmt: Expression, func: IRFunction):
        self.statement(stmt.orterm, func)

    @statement.register
    def _(self, stmt: OrTerm, func: IRFunction):
        self.statement(stmt.andterm, func)

    @statement.register
    def _(self, stmt: AndTerm, func: IRFunction):
        self.statement(stmt.relTerm, func)
        if stmt.symbol:
            self.statement(stmt.next, func)
            instr = IRInstruction(IRType.getBinOpCode("int", stmt.symbol))
            func.code.append(instr)

    @statement.register
    def _(self, stmt: RelTerm, func: IRFunction):
        self.statement(stmt.addTerm, func)
        if stmt.symbol:
            self.statement(stmt.next, func)
            instr = IRInstruction(IRType.getBinOpCode("int", stmt.symbol))
            func.code.append(instr)

    @statement.register
    def _(self, stmt: AddTerm, func: IRFunction):
        self.statement(stmt.factor, func)
        if stmt.symbol:
            self.statement(stmt.next, func)
            instr = IRInstruction(IRType.getBinOpCode("int", stmt.symbol))
            func.code.append(instr)

    @statement.register
    def _(self, stmt: Factor, func: IRFunction):
        if stmt.literal:
            instr = IRInstruction(IRType.getConst("int"), stmt.literal)
            func.code.append(instr)
            return

        if stmt.arguments:
            print(f"Arguments: {stmt.arguments}")
            for arg in stmt.arguments:
                self.statement(arg, func)

            instr = IRInstruction("CALL", stmt.id)
            func.code.append(instr)
            return

        if stmt.id:
            if stmt.id in func.locals:
                instr = IRInstruction("LOCAL_GET", stmt.id)
                func.code.append(instr)
                return
            if stmt.id in func.module.globals:
                instr = IRInstruction("GLOBAL_GET", stmt.id)
                func.code.append(instr)
                return

            raise Exception(f"Variable {stmt.id} no encontrada en el contexto actual")

        if stmt.unary_expression:
            instr = IRInstruction(
                IRType.getConst("int"),
                f"{stmt.unary_op}{stmt.unary_expression.literal}",
            )
            func.code.append(instr)
            return

        raise NotImplementedError(
            f"No hay un handler implementado para el tipo {stmt}\n"
        )

    @statement.register
    def _(self, stmt: ReturnStmt, func: IRFunction):
        self.statement(stmt.expression, func)
        instr = IRInstruction("RET")
        func.code.append(instr)

    @statement.register
    def _(self, stmt: PrintStmt, func: IRFunction):
        self.statement(stmt.expression, func)
        instr = IRInstruction(IRType.getPrint("int"))
        func.code.append(instr)

    @statement.register
    def _(self, stmt: IfStmt, func: IRFunction):
        self.statement(stmt.expression, func)
        instr = IRInstruction("IF")
        func.code.append(instr)

        for statement in stmt.if_statement:
            self.statement(statement, func)

        if stmt.else_statement:
            instr = IRInstruction("ELSE")
            func.code.append(instr)
            for statement in stmt.else_statement:
                self.statement(statement, func)

        instr = IRInstruction("ENDIF")
        func.code.append(instr)

    @statement.register
    def _(self, stmt: WhileStmt, func: IRFunction):
        instr = IRInstruction("LOOP")
        func.code.append(instr)
        self.statement(stmt.expression, func)
        instr = IRInstruction("CBREAK_IF_FALSE")
        func.code.append(instr)

        for statement in stmt.statement:
            self.statement(statement, func)

        instr = IRInstruction("ENDLOOP")
        func.code.append(instr)

    @statement.register
    def _(self, stmt: ContinueStmt, func: IRFunction):
        instr = IRInstruction("CONTINUE")
        func.code.append(instr)

    @statement.register
    def _(self, stmt: BreakStmt, func: IRFunction):
        instr = IRInstruction("CBREAK")
        func.code.append(instr)
