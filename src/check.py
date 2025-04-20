from rich import print
from parser import *
from symtab import Symtab
from typesys import typenames, check_binop, check_unaryop
from dataclasses import dataclass
from typing import Union


@dataclass
class LiteralNode:
    value: Union[int, float, str, bool]


class Checker:
    @classmethod
    def check(cls, node):
        check = cls()
        env = Symtab("global")
        check.visit_program(node, env)
        return check

    def visit_program(self, node: Program, env: Symtab):
        for stmt in node.statements:
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
            if not node.type and node.mut == "const":
                node.type = expr_type
            elif node.type and node.type != expr_type:
                raise TypeError(
                    f"[Error] Tipo incompatible en declaración de variable '{node.id}'"
                )

    def visit_Assignment(self, node: Assignment, env: Symtab):
        var = env.get(node.location.id)
        if not var:
            raise NameError(f"[Error] Variable no declarada: {node.location.id}")
        if var.mut == "const":
            raise TypeError(f"[Error] No se puede asignar a constante '{var.id}'")
        expr_type = self.visit(node.expression, env)
        if var.type != expr_type:
            raise TypeError(f"[Error] Asignación de tipo incorrecto a '{var.id}'")

        # Marcar como inicializada
        var.initialized = True

    def visit_Literal(self, node, env: Symtab):
        v = node.value
        if isinstance(v, bool):
            return "bool"
        elif isinstance(v, int):
            return "int"
        elif isinstance(v, float):
            return "float"
        elif isinstance(v, str):
            # Validar si es un carácter de escape válido
            if v in {"\\n"} or len(v) == 1:
                return "char"
        else:
            raise TypeError(f"[Error] Literal desconocido: {v!r}")

    def visit_PrintStmt(self, node: PrintStmt, env: Symtab):
        self.visit(node.expression, env)

    def visit_IfStmt(self, node: IfStmt, env: Symtab):
        cond_type = self.visit(node.expression, env)
        if cond_type != "bool":
            raise TypeError("[Error] Condición del if no es booleana")
        for stmt in node.if_statement:
            self.visit(stmt, env)
        for stmt in node.else_statement:
            self.visit(stmt, env)

    def visit_WhileStmt(self, node: WhileStmt, env: Symtab):
        cond_type = self.visit(node.expression, env)
        if cond_type != "bool":
            raise TypeError("[Error] Condición del while no es booleana")
        for stmt in node.statement:
            self.visit(stmt, env)

    def visit_ReturnStmt(self, node: ReturnStmt, env: Symtab):
        return self.visit(node.expression, env)

    def visit_Expression(self, node: Expression, env: Symtab):
        left = self.visit(node.orterm, env)
        if node.next:
            right = self.visit(node.next, env)
            result = check_binop(node.orSymbol, left, right)
            if result is None:
                raise TypeError(
                    f"[Error] Operador '{node.orSymbol}' incompatible entre {left} y {right}"
                )
            return result
        return left

    def visit_OrTerm(self, node: OrTerm, env: Symtab):
        left = self.visit(node.andterm, env)
        if node.next:
            right = self.visit(node.next, env)
            result = check_binop(node.andSymbol, left, right)
            if result is None:
                raise TypeError(
                    f"[Error] Operador '{node.andSymbol}' incompatible entre {left} y {right}"
                )
            return result
        return left

    def visit_AndTerm(self, node: AndTerm, env: Symtab):
        left = self.visit(node.relTerm, env)
        if node.next:
            right = self.visit(node.next, env)
            result = check_binop(node.relSymbol, left, right)
            if result is None:
                raise TypeError(
                    f"[Error] Operador '{node.relSymbol}' incompatible entre {left} y {right}"
                )
            return result
        return left

    def visit_RelTerm(self, node: RelTerm, env: Symtab):
        left = self.visit(node.addTerm, env)
        if node.next:
            right = self.visit(node.next, env)
            result = check_binop(node.symbol, left, right)
            if result is None:
                raise TypeError(
                    f"[Error] Operador '{node.symbol}' incompatible entre {left} y {right}"
                )
            return result
        return left

    def visit_AddTerm(self, node: AddTerm, env: Symtab):
        left = self.visit(node.factor, env)
        if node.next:
            right = self.visit(node.next, env)
            result = check_binop(node.symbol, left, right)
            if result is None:
                raise TypeError(
                    f"[Error] Operador '{node.symbol}' incompatible entre {left} y {right}"
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
                raise NameError(f"[Error] Variable o función no declarada: {node.id}")

            # Verificar si la variable ha sido inicializada (si no es función)
            if isinstance(decl, Vardecl):
                if not env.is_initialized(node.id):
                    if (
                        not env.is_global_scope()
                    ):  # Solo permitimos uso no inicializado si es global
                        raise NameError(
                            f"[Error] Variable '{node.id}' usada sin inicializar"
                        )

            # Si es una llamada a función
            if node.arguments:
                if not isinstance(decl, FuncDecl):
                    raise TypeError(f"[Error] '{node.id}' no es una función.")

                # Recorremos los argumentos pasados y esperados
                actual_args = []
                formal = decl.parameters
                arg_exprs = node.arguments
                param = decl.parameters

                for i, expr in enumerate(arg_exprs):
                    if not param:
                        raise TypeError(
                            f"[Error] Número incorrecto de argumentos en llamada a '{node.id}'"
                        )
                    arg_type = self.visit(expr, env)
                    if arg_type != param.type:
                        raise TypeError(
                            f"[Error] Argumento {i + 1} en llamada a '{node.id}': esperado '{param.type}', recibido '{arg_type}'"
                        )
                    param = param.next

                if param:
                    raise TypeError(
                        f"[Error] Número incorrecto de argumentos en llamada a '{node.id}'"
                    )

                return decl.return_type

            return decl.type

        if node.unary_expression:
            inner_type = self.visit(node.unary_expression, env)
            result = check_unaryop(node.unary_op, inner_type)
            if result is None:
                raise TypeError(
                    f"[Error] Operador unario '{node.unary_op}' incompatible con tipo {inner_type}"
                )
            return result

        raise TypeError("[Error] Factor inválido")

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
            raise TypeError(f"[Error] Redefinición de función '{node.id}'")

        env.add(node.id, node)

        # 2. Crear nuevo entorno local
        local_env = Symtab(name=f"func_{node.id}", parent=env)

        # 3. Agregar parámetros al entorno local
        current_param = node.parameters
        while current_param:
            if local_env.contains(current_param.id):
                raise NameError(f"[Error] Parámetro duplicado: {current_param.id}")
            vardecl = Vardecl(mut="var", id=current_param.id, type=current_param.type)
            vardecl.initialized = True
            local_env.add(current_param.id, vardecl)
            current_param = current_param.next

        # 4. Analizar el cuerpo
        return_found = False
        for stmt in node.statements:
            if isinstance(stmt, ReturnStmt):
                return_type = self.visit(stmt, local_env)
                if return_type != node.return_type:
                    raise TypeError(
                        f"[Error] La función '{node.id}' debe retornar '{node.return_type}', pero retornó '{return_type}'"
                    )
                return_found = True
            else:
                self.visit(stmt, local_env)

        # 5. Verificar que haya return si no es void
        if node.return_type != "void" and not return_found:
            raise TypeError(f"[Error] La función '{node.id}' debe tener un return.")

    def visit_ContinueStmt(self, node, env: Symtab):
        pass

    def visit_BreakStmt(self, node, env: Symtab):
        pass
