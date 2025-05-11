from rich import print
from typing import List, Union
from functools import singledispatchmethod

from parser import *
from symtab import Symtab


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
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def dump(self):
        print(f"GLOBAL::: {self.name}: {self.type}")


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

    def new_local(self, name: str, type: str):
        self.locals[name] = type

    def append(self, opcode: str, *args):
        self.code.append(IRInstruction(opcode, *args))

    def extend(self, instructions: List[IRInstruction]):
        self.code.extend(instructions)

    def dump(self):
        mapped_parmtypes = [_typemap.get(t, t) for t in self.parmtypes]
        mapped_return_type = _typemap.get(self.return_type, self.return_type)

        print(
            f"\nFUNCTION::: {self.name}, {self.parmnames}, {mapped_parmtypes} {mapped_return_type}"
        )
        mapped_locals = {
            name: _typemap.get(type, type) for name, type in self.locals.items()
        }
        print(f"locals: {mapped_locals}")
        for instr in self.code:
            print(instr)


_typemap = {
    "int": "I",
    "float": "F",
    "bool": "I",
    "char": "I",
}


def new_temp(n=[0]):
    n[0] += 1
    return f"$temp{n[0]}"


class IRCode:
    def __init__(self):
        pass

    def gencode(self, program: Program) -> IRModule:
        module = IRModule()
        main_func = IRFunction(module, "main", [], [], "I")

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
    def _(self, stmt: Vardecl, func: IRFunction):
        func.locals[stmt.id] = stmt.type

        if stmt.expression is not None:
            # Creamos la asignación completa con todos sus campos
            assignment = Assignment(
                lineno=stmt.lineno,
                location=Location(lineno=stmt.lineno, id=stmt.id),
                symbol="=",
                expression=stmt.expression,
            )

            self.statement(assignment, func)

    @statement.register
    def _(self, stmt: Assignment, func: IRFunction):
        self.statement(stmt.expression, func)
        instr = IRInstruction("LOCAL_SET", stmt.location.id)
        func.code.append(instr)

    @statement.register
    def _(self, stmt: Expression, func: IRFunction):
        self.statement(stmt.orterm, func)
        # TODO: Agregar el resto de la expresión

    @statement.register
    def _(self, stmt: OrTerm, func: IRFunction):
        self.statement(stmt.andterm, func)

    @statement.register
    def _(self, stmt: AndTerm, func: IRFunction):
        self.statement(stmt.relTerm, func)

    @statement.register
    def _(self, stmt: RelTerm, func: IRFunction):
        self.statement(stmt.addTerm, func)
        if stmt.next:
            self.statement(stmt.next, func)
            instr = IRInstruction("ADD")
            func.code.append(instr)

    @statement.register
    def _(self, stmt: AddTerm, func: IRFunction):
        self.statement(stmt.factor, func)

    @statement.register
    def _(self, stmt: Factor, func: IRFunction):
        if stmt.literal:
            instr = IRInstruction("CONST", stmt.literal)
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
            instr = IRInstruction("LOCAL_GET", stmt.id)
            func.code.append(instr)
            return

        raise NotImplementedError(
            f"No hay un handler implementado para el tipo {type(stmt).__name__}\n"
        )

    @statement.register
    def _(self, stmt: ReturnStmt, func: IRFunction):
        self.statement(stmt.expression, func)
        instr = IRInstruction("RET")
        func.code.append(instr)

    @statement.register
    def _(self, stmt: PrintStmt, func: IRFunction):
        self.statement(stmt.expression, func)
        instr = IRInstruction("PRINT")
        func.code.append(instr)
