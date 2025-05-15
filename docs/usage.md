## 🚀 Modo de uso

Con la extensión implementada, solo necesitas crear tu archivo `.gox` junto con el archivo `lexer.py`, que se encuentra en el repositorio. Asegúrate de que ambos archivos estén en la misma carpeta antes de ejecutar.

### 🔹 Ejemplo de código GOX

Antes de ejecutar, asegúrate de tener un archivo `.gox` con código válido. Aquí tienes un ejemplo:

```gox
var x = 10;
print(x);
```

### 🔹 Ejecución del código

Puedes ejecutar el archivo `.gox` con la extensión de VS Code o directamente desde la terminal.

#### 1️⃣ Desde VS Code (usando la extensión)

Al abrir el archivo en VS Code, selecciona la opción de ejecución disponible en la barra superior:

![Ejecución del archivo GOX](/docs/images/run-gox-file.png)

#### 2️⃣ Desde la terminal (manualmente con Python)

Si prefieres ejecutarlo manualmente, usa el siguiente comando:

```sh
python main.py archivo.gox
```

Esto abrirá la terminal con el **analizador léxico (Lexer)**, el cual se encargará de descomponer el código en tokens.

---

## 🔍 **Lexer: Tokenización del código**

El **Lexer** se encarga de analizar el código y convertirlo en una lista de tokens. La salida se divide en dos partes:

### ✅ **Tokens generados**

```sh
Token(TIPO, VALOR, N° de Línea)
```

Por ejemplo, si ejecutamos el código GOX anterior, la salida podría ser:

```sh
Token(VAR, 'var', 1)
Token(ID, 'x', 1)
Token(ASSIGN, '=', 1)
Token(NUM, '10', 1)
Token(SEMICOLON, ';', 1)
Token(PRINT, 'print', 2)
Token(OPEN_PAREN, '(', 2)
Token(ID, 'x', 2)
Token(CLOSE_PAREN, ')', 2)
Token(SEMICOLON, ';', 2)
```

para ejecutar el lexer usamos
```sh
python lexer.py archivo.gox
```

### ❌ **Captura de errores en el Lexer**

Si hay un error léxico en el código, la terminal mostrará algo como:

```sh
15: Caracter ilegal '%'
N° de Línea: ERROR
```

Esto indica que en la línea 15 se encontró un carácter no válido (`%`).

---

## 🏗️ **Parser: Análisis de la estructura del código**

El **Parser** analiza la estructura del código GOX basándose en los tokens generados por el **Lexer** y construye el **AST** (Árbol de Sintaxis Abstracta). 

Si el código es válido, se imprimirá el AST en formato JSON. 

Ejemplo de salida:

```json
{
    "statements": [
        {
            "type": "Vardecl",
            "mut": "const",
            "id": "PI",
            "var_type": "float",
            "assignment": "=",
            "expression": {
                "literal": "3.1415"
            }
        }
    ]
}
```

Si hay errores de sintaxis, se mostrará un mensaje indicando el problema y la línea afectada.
```sh
  File "/home/cris/Documents/Repo/gox-compiler/src/parser.py", line 254, in vardecl
    raise ValueError(
        f"El statement no terminó correctamente. Se esperaba ';'. {self.current_token().lineno}"
    )
ValueError: El statement no terminó correctamente. Se esperaba ';'. 10
```
---

## 📄 **Serialización: Guardado del AST**

El AST generado se guarda automáticamente en el archivo `ast_output.json`.

---

## 🧠 **Análisis Semántico**

Valida aspectos como:

- Tipos compatibles en asignaciones y operaciones

- Variables declaradas e inicializadas

- Uso correcto de constantes

- Declaración y uso de funciones, retorno esperado, etc.

Ejemplo de errores:

```sh
    Error en la línea 4: La variable no está inicializada → x
    Error en la línea 8: La función retorna un tipo diferente al declarado → Tipo esperado: int, tipo encontrado: float
```
Si no hay errores, se imprime:

```sh
✔ Análisis semántico exitoso
```
---
## ⚙️ **Generación de Código Intermedio (IR)**

Si no hay errores semánticos, se genera automáticamente un archivo .ir en src/ircode-files.

```sh
Código intermedio generado
```

🔹 Ejemplo de salida IR:
```sh
MODULE:::

FUNCTION::: main, [], [] I
locals: {}

FUNCTION::: mod, [], [] I
locals: {}
('CONSTI', 1)
('CONSTI', 1)
('EQI',)
('IF',)
('CONSTI', 1)
('RET',)
('ENDIF',)
('CONSTI', 0)
('RET',)
```
💾 Archivo generado: src/ircode-files/archivo.ir