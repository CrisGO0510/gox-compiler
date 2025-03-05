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
python lexer.py archivo.gox
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

### ❌ **Captura de errores en el Lexer**

Si hay un error léxico en el código, la terminal mostrará algo como:

```sh
15: Caracter ilegal '%'
N° de Línea: ERROR
```

Esto indica que en la línea 15 se encontró un carácter no válido (`%`).

---

## 🏗️ **Parser: Análisis de la estructura del código**

El siguiente paso en la ejecución del código será el **Parser**, el cual analizará la estructura y sintaxis del código GOX basándose en los tokens generados por el **Lexer**.
