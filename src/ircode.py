from rich import print
from typing import List, Union
from functools import singledispatchmethod

from parser import *
from symtab import Symtab


class IRModule:
    def __init__(self):
        self.functions = {}
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

        print(f"FUNCTION::: {self.name}, {self.parmnames}, {mapped_parmtypes} ")
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
            # TODO: Agregar call a main

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

    @statement.register
    def _(self, stmt: ReturnStmt, func: IRFunction):
        print("Handling return statement")

    @statement.register
    def _(self, stmt: PrintStmt, func: IRFunction):
        print("Handling print statement")
