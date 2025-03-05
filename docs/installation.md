# 📥 Instalación

## Requisitos

Antes de comenzar, asegúrate de tener instalados:
- [Node.js](https://nodejs.org/)
- [Python 3](https://www.python.org/)
- [Visual Studio Code](https://code.visualstudio.com/)
---

Clona el repositorio:
   ```sh
   git clone https://github.com/CrisGO0510/gox-compiler.git
   ```
   
## 🛠️ Instalación de la extensión

1. Instala las dependencias:
   ```sh
   cd gox-compiler/.gox-runner
   ```

    ```sh
    npm i
    ```

2. Empaqueta la extensión de VS Code:
   ```sh
   npx vsce package
   ```

3. Instala el paquete `.vsix` generado:

   - Usando la línea de comandos:
     ```sh
     code --install-extension gox-runner.vsix
     ```

   - Alternativamente, puedes instalar el paquete desde la interfaz gráfica:
     - Abre VS Code y presiona `Ctrl + Shift + P`.
     - Selecciona **Extensions: Install from VSIX**.

       ![Instalar el paquete a vsc](/docs/images/install-VSIX.png)

     - Busca el paquete en la carpeta `./.gox-runner` y selecciona el archivo `.vsix` generado.

       ![Buscar paquete](/docs/images/search-VSIX.png)

     - Reinicia Visual Studio Code.


## 🛠️ Instalación de dependencias en el entorno virtual (Python)

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
