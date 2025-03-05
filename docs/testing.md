## ✅ Pruebas unitarias

El lexer cuenta con pruebas unitarias en `test_lexer.py`, usando `unittest`. Para ejecutarlas:

```sh
python -m unittest discover
```

Las pruebas verifican los siguientes casos:

- **Palabras reservadas**: `const`, `var`, `print`, `return`, etc.
- **Identificadores válidos**: `variable`, `_var1`, `a1b2c3`
- **Números**: `123`, `45.67`, `.456`, `123.`
- **Operadores**: `+`, `-`, `*`, `/`, `<=`, `>=`, `==`, `!=`, `&&`, `||`, `^`
- **Símbolos misceláneos**: `=`, `;`, `(`, `)`, `{`, `}`, `,`
- **Comentarios**: Se ignoran correctamente.
- **Errores detectados**:
  - Caracteres ilegales: `@`, `$`, `#`, etc.
  - Comentarios sin cerrar: `/* comentario no cerrado`
  - Cadenas sin cerrar: `'texto sin cerrar`

### 🔹 **Ejemplo de ejecución**

Al ejecutar las pruebas, se obtiene una salida similar a esta:

![Ejemplo de pruebas unitarias](/docs/images/example-unittest.png)