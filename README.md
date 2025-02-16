
# GOX Lexer & VSCode Extension

Este proyecto es un compilador para el lenguaje `.gox`, junto con una extensión de VS Code para facilitar su ejecución y desarrollo.

## 🛠️ Instalación

1. Clona el repositorio:
   ```sh
   git clone https://github.com/CrisGO0510/gox-compiler.git
   ```

2. Instala las dependencias:
   ```sh
   cd gox-compiler/gox-runner
   ```

    ```sh
    npm i
    ```

3. Empaqueta la extensión de VS Code:
   ```sh
   npx vsce package
   ```

4. Instala el paquete `.vsix` generado:
    - Abre VS Code y presiona `Ctrl + Shift + P`.      
    - Selecciona **Extensions: Install from VSIX**.

      ![Instalar el paquete a vsc](/images/install-VSIX.png)

    - Busca el paquete en la carpeta `./gox-runner` y selecciona el archivo `.vsix` generado.
    
      ![Buscar paquete](/images/search-VSIX.png)

    - Reinicia Visual Studio Code.


## 🛠️ Instalación de dependencias en el entorno virtual (Python)

### Requisitos

Si tu proyecto usa un entorno virtual (`.venv`) y un archivo `requirements.txt` para gestionar dependencias, sigue estos pasos para instalar las dependencias de Python.

### 1. Crear el entorno virtual

Primero, crea el entorno virtual en la raíz del proyecto:

```sh
python -m venv .venv
```

Esto generará la carpeta `.venv`, donde se almacenarán las dependencias del proyecto.

### 2. Activar el entorno virtual

#### En Windows:

```sh
.venv\Scripts\activate
```

#### En Linux/macOS:

```sh
source .venv/bin/activate
```

### 3. Instalar las dependencias desde `requirements.txt`

Una vez activado el entorno virtual, instala las dependencias usando el archivo `requirements.txt`. Esto se puede hacer de la siguiente manera:

#### En Windows y Linux/macOS:

```sh
pip install -r requirements.txt
```

### 4. Verificación

Después de la instalación, las dependencias estarán disponibles dentro del entorno virtual y podrás comenzar a trabajar en el proyecto.


## 🚀 Modo de uso

Con la extensión implementada, solo necesitas crear tu archivo `.gox` junto con el archivo `tokenize_1.py`, que se encuentra en el repositorio. Asegúrate de que ambos archivos estén en la misma carpeta antes de ejecutar:

![Ejecución del archivo GOX](/images/run-gox-file.png)

Al ejecutar, se abrirá la terminal con el analizador léxico, tokenizando el código:

![Tokenización en ejecución](/images/example-tokenize.png)

La salida se divide en:

1. **Tokenización**:
    ```sh
    Token(ID, tipo, valor)
    Token(TIPO, VALOR, N° de Línea)
    ```

2. **Captura de errores**:
    ```sh
    15: Caracter ilegal '%'
    N° de Línea: ERROR
    ```

## 🎨 Tema predeterminado

La extensión incluye una gramática para implementar los colores de su tema preferido. Si deseas usar el tema designado por el programa, sigue estos pasos:

1. Abre la paleta de comandos (`Ctrl+Shift+P`) y selecciona **GOX: Seleccionar tema**.

![Seleccionar tema GOX](/images/select-theme.png)

El tema se verá de la siguiente forma:

![Tema GOX predeterminado](/images/example-theme.png)

Si prefieres usar el tema de tu elección, este es el resultado que obtendrás:

![Tema personalizado](/images/example-theme2.png)


## 👥 Integrantes

Este proyecto fue desarrollado por:

- **Cristhian Giraldo Orozco**
- **Jannin Milena Ramirez Piedrahita**