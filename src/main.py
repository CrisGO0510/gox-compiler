import sys
from lexer import tokenize
from rich import print
from parser import RecursiveDescentParser
from serialize import save_to_json_file, to_json


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

    print("[bold green]Tokens obtenidos:[/bold green]")
    print(tokens)

    AST = RecursiveDescentParser(tokens, indexToken).program()

    print("[bold blue]Árbol de sintaxis abstracta (AST):[/bold blue]")
    print(AST)

    json_output = to_json(AST)
    print("[bold magenta]JSON generado:[/bold magenta]")
    print(json_output)

    save_to_json_file(AST, "ast_output.json")


if __name__ == "__main__":
    main()
