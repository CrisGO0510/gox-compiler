from enum import Enum
from typing import List


class ErrorType(Enum):
    MISSING_SEMICOLON = "Falta ';' al final de la instrucción."
    TYPE_MISMATCH = "Asignación de diferente tipo."
    UNDECLARED_VARIABLE = "Variable no declarada."
    UNINITIALIZED_VARIABLE = "La variable no está inicializada."
    CONSTANT_ASSIGNMENT = "No se puede asignar valor a una constante."
    UNTYPED_VARIABLE = "Variable sin tipo."
    UNINITIALIZED_CONSTANT = "Una constante debe estar inicializada."
    UNKNOWN_LITERAL = "Literal desconocido."
    NON_BOOLEAN_CONDITION = "Condición del 'if' no booleana."
    LITERAL_TYPE_MISMATCH = "Incompatibilidad entre literales de diferente tipo."
    FUNCTION_ARGUMENT_ERROR = "Solo se le pueden declarar argumentos a una función."
    INVALID_ARGUMENT_COUNT = "Número de argumentos no válidos."
    ARGUMENT_TYPE_MISMATCH = "El tipo del argumento no coincide con el tipo esperado."
    INVALID_UNARY_OPERATION = "Operador unario no válido para este tipo."
    UNKNOWN_FACTOR = "Factor desconocido."
    FUNCTION_REDEFINITION = "Redefinición de función."
    DUPLICATE_PARAMETER = "Parámetro duplicado"
    MISMATCH_RETURN_TYPE = "La función retorna un tipo diferente al declarado."
    MISSING_RETURN = "La función debe tener un return."
    INVALID_GLOBAL_STATEMENT = (
        "Este tipo de statement no puede estar en el ámbito global."
    )


class ErrorManager:
    _errorCount = 0

    @classmethod
    def print(cls, error_type: ErrorType, lineno: int, *extras):
        RED = "\033[91m"
        RESET = "\033[0m"
        cls._errorCount += 1

        # Construir mensaje base
        message = f"{RED}Error en la línea {lineno}: {error_type.value}"

        # Agregar detalles adicionales si los hay
        if extras:
            message += " → " + " ".join(str(extra) for extra in extras)

        print(f"{message}{RESET}")

    @classmethod
    def get_error_count(cls):
        RED = "\033[91m"
        RESET = "\033[0m"
        if cls._errorCount > 0:
            print(f"{RED}Se encontraron {cls._errorCount} errores.{RESET}")
        else:
            print("No se encontraron errores.")
