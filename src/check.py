from rich import print
from parser import *
from symtab import Symtab
from typesys import typenames, check_binop, check_unaryop
from dataclasses import dataclass
from typing import Union
from error import *


@dataclass
class LiteralNode:
    value: Union[int, float, str, bool]


class Checker:
    @classmethod
    def check(cls, node):
        check = cls()
        env = Symtab("global")
        check.visit_program(node, env)
        # env.print()
        return check

    def visit_program(self, node: Program, env: Symtab):
        for stmt in node.statements:
            if isinstance(
                stmt, (ReturnStmt, BreakStmt, ContinueStmt, IfStmt, WhileStmt)
            ):
                ErrorManager.print(
                    ErrorType.INVALID_GLOBAL_STATEMENT, stmt.lineno, type(stmt).__name__
                )
            else:
                self.visit(stmt, env)

    def visit(self, node, env: Symtab):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node, env)

    def generic_visit(self, node, env: Symtab):
        raise NotImplementedError(f"No implementado para {type(node).__name__}")

    def visit_Vardecl(self, node: Vardecl, env: Symtab):
        env.add(node.id, node)
        if node.expression:
            expr_type = self.visit(node.expression, env)
            if not node.type and node.mut == "var":
                ErrorManager.print(ErrorType.UNTYPED_VARIABLE, node.lineno, node.id)

            if node.type and node.type != expr_type:
                ErrorManager.print(ErrorType.TYPE_MISMATCH, node.lineno, node.id)

            node.initialized = True
            node.type = expr_type

        if node.mut == "const" and node.expression is None:
            ErrorManager.print(
                ErrorType.UNINITIALIZED_CONSTANT, node.lineno, node.id
            )


    def visit_Assignment(self, node: Assignment, env: Symtab):
        var = env.get(node.location.id)
        if not var:
            ErrorManager.print(ErrorType.UNINITIALIZED_VARIABLE, node.lineno, node.id)

        if var.mut == "const":
            ErrorManager.print(ErrorType.CONSTANT_ASSIGNMENT, node.lineno, node.id)

        expr_type = self.visit(node.expression, env)

        if expr_type:
            var.initialized = True

        if var.type != expr_type:
            ErrorManager.print(
                ErrorType.TYPE_MISMATCH,
                node.lineno,
                f"Tipo esperado: {var.type}, tipo encontrado: {expr_type}",
            )

    def visit_Literal(self, node, env: Symtab):
        v = node.value
        if isinstance(v, bool):
            return "bool"
        elif isinstance(v, int):
            return "int"
        elif isinstance(v, float):
            return "float"
        elif isinstance(v, str):
            if v in {"\\n"} or len(v) == 1:
                return "char"
        else:
            ErrorManager.print(ErrorType.UNKNOWN_LITERAL, node.lineno, v)

    def visit_PrintStmt(self, node: PrintStmt, env: Symtab):
        self.visit(node.expression, env)

    def visit_IfStmt(self, node: IfStmt, env: Symtab):
        cond_type = self.visit(node.expression, env)
        if cond_type != "bool":
            ErrorManager.print(ErrorType.NON_BOOLEAN_CONDITION, node.lineno, cond_type)
        for stmt in node.if_statement:
            self.visit(stmt, env)
        for stmt in node.else_statement:
            self.visit(stmt, env)

    def visit_WhileStmt(self, node: WhileStmt, env: Symtab):
        cond_type = self.visit(node.expression, env)
        if cond_type != "bool":
            ErrorManager.print(ErrorType.NON_BOOLEAN_CONDITION, node.lineno, cond_type)
        for stmt in node.statement:
            self.visit(stmt, env)

    def visit_ReturnStmt(self, node: ReturnStmt, env: Symtab):
        return self.visit(node.expression, env)

    def visit_Expression(self, node: Expression, env: Symtab):
        left = self.visit(node.orterm, env)
        if node.next:
            right = self.visit(node.next, env)
            result = check_binop(node.symbol, left, right)
            if result is None:
                ErrorManager.print(
                    ErrorType.LITERAL_TYPE_MISMATCH,
                    node.lineno,
                    f"{left} {node.symbol} {right}",
                )
            return result
        return left

    def visit_OrTerm(self, node: OrTerm, env: Symtab):
        left = self.visit(node.andterm, env)
        if node.next:
            right = self.visit(node.next, env)
            result = check_binop(node.symbol, left, right)
            if result is None:
                ErrorManager.print(
                    ErrorType.LITERAL_TYPE_MISMATCH,
                    node.lineno,
                    f"{left} {node.symbol} {right}",
                )
            return result
        return left

    def visit_AndTerm(self, node: AndTerm, env: Symtab):
        left = self.visit(node.relTerm, env)
        if node.next:
            right = self.visit(node.next, env)
            result = check_binop(node.symbol, left, right)
            if result is None:
                ErrorManager.print(
                    ErrorType.LITERAL_TYPE_MISMATCH,
                    node.lineno,
                    f"{left} {node.symbol} {right}",
                )
            return result
        return left

    def visit_RelTerm(self, node: RelTerm, env: Symtab):
        left = self.visit(node.addTerm, env)
        if node.next:
            right = self.visit(node.next, env)
            result = check_binop(node.symbol, left, right)
            if result is None:
                ErrorManager.print(
                    ErrorType.LITERAL_TYPE_MISMATCH,
                    node.lineno,
                    f"{left} {node.symbol} {right}",
                )
            return result
        return left

    def visit_AddTerm(self, node: AddTerm, env: Symtab):
        left = self.visit(node.factor, env)
        if node.next:
            right = self.visit(node.next, env)
            result = check_binop(node.symbol, left, right)
            if result is None:
                ErrorManager.print(
                    ErrorType.LITERAL_TYPE_MISMATCH,
                    node.lineno,
                    f"{left} {node.symbol} {right}",
                )
            return result
        return left

    def visit_Factor(self, node: Factor, env: Symtab):
        if node.literal is not None:
            lit_node = LiteralNode(value=self._parse_literal_value(node.literal))
            return self.visit_Literal(lit_node, env)

        if node.id:
            decl = env.get(node.id)
            if not decl:
                ErrorManager.print(ErrorType.UNDECLARED_VARIABLE, node.lineno, node.id)
                return None

            # Verificar si la variable ha sido inicializada (si no es función)
            if isinstance(decl, Vardecl):
                if not env.is_initialized(node.id):
                    if (
                        not env.is_global_scope()
                    ):  # Solo permitimos uso no inicializado si es global
                        ErrorManager.print(
                            ErrorType.UNINITIALIZED_VARIABLE, node.lineno, node.id
                        )
                return decl.type

            # Si es una llamada a función
            if node.arguments:
                # Recorremos los argumentos pasados y esperados
                arg_exprs = node.arguments
                param = decl.parameters

                for i, expr in enumerate(arg_exprs):
                    if not param:
                        ErrorManager.print(
                            ErrorType.INVALID_ARGUMENT_COUNT, node.lineno
                        )
                        return decl.return_type

                    arg_type = self.visit(expr, env)
                    if arg_type != param.type:
                        ErrorManager.print(
                            ErrorType.ARGUMENT_TYPE_MISMATCH,
                            node.lineno,
                            f"Tipo esperado: {param.type}, tipo encontrado: {arg_type}",
                        )
                        return decl.return_type

                    param = param.next

                if param:
                    ErrorManager.print(ErrorType.INVALID_ARGUMENT_COUNT, node.lineno)

                return decl.return_type

            return decl.type

        if node.unary_expression:
            inner_type = self.visit(node.unary_expression, env)
            result = check_unaryop(node.unary_op, inner_type)
            if result is None:
                ErrorManager.print(ErrorType.INVALID_UNARY_OPERATION, node.lineno)
            return result

        if node.expression:
            inner_type = self.visit(node.expression, env)
            return inner_type

        ErrorManager.print(ErrorType.UNKNOWN_FACTOR, node.lineno, node.id)
        return None

    def _parse_literal_value(self, val):
        if val == "true":
            return True
        elif val == "false":
            return False
        elif isinstance(val, str) and val.replace(".", "", 1).isdigit():
            return float(val) if "." in val else int(val)
        elif isinstance(val, str) and len(val) == 1:
            return val  # char
        return val

    def visit_FuncDecl(self, node: FuncDecl, env: Symtab):
        # 1. Registrar la función en el entorno global
        if env.get(node.id):
            ErrorManager.print(ErrorType.FUNCTION_REDEFINITION, node.lineno, node.id)

        env.add(node.id, node)

        # 2. Crear nuevo entorno local
        local_env = Symtab(name=f"func_{node.id}", parent=env)

        # 3. Agregar parámetros al entorno local
        current_param = node.parameters
        while current_param:
            if local_env.contains(current_param.id):
                ErrorManager.print(
                    ErrorType.DUPLICATE_PARAMETER, node.lineno, current_param.id
                )
            param = Parameters(
                id=current_param.id,
                type=current_param.type,
                lineno=node.lineno,
            )
            local_env.add(current_param.id, param)
            current_param = current_param.next

        # 4. Analizar el cuerpo
        return_found = False
        for stmt in node.statements:
            return_type = self.visit(stmt, local_env)
            if isinstance(stmt, ReturnStmt):
                if return_type != node.return_type:
                    ErrorManager.print(
                        ErrorType.MISMATCH_RETURN_TYPE,
                        node.lineno,
                        f"Tipo esperado: {node.return_type}, tipo encontrado: {return_type}",
                    )
                return_found = True

        # 5. Verificar que haya return si no es void
        if not return_found:
            ErrorManager.print(ErrorType.MISSING_RETURN, node.lineno)

    def visit_ContinueStmt(self, node, env: Symtab):
        pass

    def visit_BreakStmt(self, node, env: Symtab):
        pass
