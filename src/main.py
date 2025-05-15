import sys
import os
from error import ErrorManager
from lexer import tokenize
from rich import print
from parser import Program, RecursiveDescentParser
from serialize import save_to_json_file, to_json
from check import Checker
from ircode import IRCode


def main():
    if len(sys.argv) < 2:
        print(
            "[red]Error: Debes proporcionar un archivo de código fuente como argumento.[/red]"
        )
        print("Uso: python main.py archivo.txt")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"[red]Error: El archivo '{filename}' no existe.[/red]")
        sys.exit(1)

    tokens = list(tokenize(text))
    indexToken = 0

    # print("[bold green]Tokens obtenidos:[/bold green]")
    # print(tokens)

    try:
        AST = RecursiveDescentParser(tokens, indexToken).program()
    except Exception as e:
        print(f"[red]❌ Error de sintaxis:[/red] {e}")
        sys.exit(1)

    # print("[bold blue]Árbol de sintaxis abstracta (AST):[/bold blue]")
    # print(AST)

    json_output = to_json(AST)
    # print("[bold magenta]JSON generado:[/bold magenta]")
    # print(json_output)

    save_to_json_file(AST, "ast_output.json")

    try:
        Checker.check(AST)
        print("[bold green]✔ Análisis semántico exitoso[/bold green]")
    except Exception as e:
        print(f"[red]❌ Error semántico:[/red] {e}")
        sys.exit(1)

    if ErrorManager.get_error_count():
        ircode_main(AST, filename)


def ircode_main(AST: Program, filename: str):
    base_name = os.path.splitext(os.path.basename(filename))[0]
    ir_filename = f"./src/ircode-files/{base_name}.ir"

    print("[bold yellow]Código intermedio generado[/bold yellow]")
    ir = IRCode().gencode(AST).dump()
    with open(ir_filename, "w") as f:
        f.write(ir)

if __name__ == "__main__":
    main()
