import ast, re
from ircode import IRType


# ---------- 1.  Pequeño "loader" de módulos ---------- #
def parse_module(text: str):
    lines = [l.strip() for l in text.strip().splitlines()]
    program, functions, params_map = [], {}, {}
    i = 0
    while i < len(lines):
        if lines[i].startswith("FUNCTION:::"):
            #  cabecera = nombre,  [params],  [rettypes]   I
            header = lines[i].split(":::")[1].strip()
            m = re.match(r"(\w+),\s*(\[[^\]]*\])", header)

            if not m:
                raise SyntaxError(f"Cabecera de función mal formada: {header}")

            name = m.group(1)
            param_list = ast.literal_eval(m.group(2))
            params_map[name] = param_list
            functions[name] = len(program)
            i += 1
            while i < len(lines) and (lines[i].startswith("locals") or not lines[i]):
                i += 1
            while (
                i < len(lines) and lines[i] and not lines[i].startswith("FUNCTION:::")
            ):
                program.append(ast.literal_eval(lines[i]))
                i += 1
        else:
            i += 1

    # ─── EMPAREJAR LOOP / ENDLOOP ───
    loop_stack, loop_map = [], {}
    for pc, (op, *_) in enumerate(program):
        if op == "LOOP":
            loop_stack.append(pc)
        elif op == "ENDLOOP":
            if not loop_stack:
                raise SyntaxError("ENDLOOP sin LOOP que lo abra")
            start = loop_stack.pop()
            loop_map[start] = pc  # de LOOP → su ENDLOOP
            loop_map[pc] = start  # de ENDLOOP → su LOOP
    if loop_stack:
        raise SyntaxError("Alguno de los LOOP no tiene ENDLOOP")

    return program, functions, params_map, loop_map


# ---------- 2.  Máquina de pila ---------- #
class StackMachine:
    def __init__(self):
        self.stack = []  # (tipo, valor)
        self.frames = []  # marcos locales
        self.call_stack = []  # return addresses
        self.loop_stack = []  # [(pc_LOOP, pc_ENDLOOP), ...]
        self.program, self.functions, self.loop_map, self.params_map = [], {}, {}, {}
        self.pc = 0
        self.running = False

    # ---- carga y arranque ----

    def load_module(self, module_text):
        (self.program, self.functions, self.params_map, self.loop_map) = parse_module(
            module_text
        )

    def run(self, entry: str = "main"):
        if entry not in self.functions:
            raise RuntimeError(f"Punto de entrada '{entry}' no encontrado")
        self.pc = self.functions[entry]
        self.frames.append({})  # marco inicial
        self.running = True
        while self.running and self.pc < len(self.program):
            op, *args = self.program[self.pc]

            # Procesar operaciones con sufijo de tipo (I,F,C,B)
            if len(op) > 1 and op[-1] in ("I", "F", "C", "B"):
                base_op = op[:-1]
                type_suffix = op[-1]
                method = getattr(self, f"op_{base_op}")
                # Para CONST y PRINT el manejo es especial
                if base_op == "CONST":
                    method(args[0], type_suffix)
                elif base_op == "PRINT":
                    method(type_suffix)
                else:
                    # Para operaciones como ADDI, SUBI, MULI, DIVI, EQI, etc.
                    method(type_suffix)
            else:
                # Para el resto de operaciones, comportamiento normal
                method = getattr(self, f"op_{op}")
                method(*args)

            self.pc += 1

    # ---- helpers para marcos ----
    def _frame(self):  # marco actual
        return self.frames[-1]

    # ─────────────  N U E V A S   O P S   D E   B U C L E ───────────── #
    def op_LOOP(self):
        """Marca el inicio del bucle; empuja a loop_stack el par (start,end)."""
        end_pc = self.loop_map[self.pc]  # emparejado por parse_module()
        self.loop_stack.append((self.pc, end_pc))

    def op_ENDLOOP(self):
        if not self.loop_stack:
            raise RuntimeError("ENDLOOP fuera de cualquier bucle")
        start_pc, _ = self.loop_stack.pop()  #  ←  ¡POP AQUÍ!
        self.pc = start_pc - 1  #  -1 porque el while hará +1

    def op_CBREAK(self):
        if not self.loop_stack:
            raise RuntimeError("CBREAK fuera de cualquier bucle")

        _typ, val = self.stack.pop()
        if not bool(val):
            _, end_pc = self.loop_stack.pop()
            self.pc = end_pc

    # ─────────────  R E S T O   D E   O P C O D E S  (ejemplos) ─────── #
    def op_ADD(self, suffix_type: str):
        b_t, b = self.stack.pop()
        a_t, a = self.stack.pop()
        value_type = IRType.getTypeMapInv(suffix_type)
        if a_t == b_t == value_type:
            self.stack.append((value_type, a + b))
        else:
            raise TypeError("ADD requiere dos enteros")

    def op_SUB(self, suffix_type: str):
        b_t, b = self.stack.pop()
        a_t, a = self.stack.pop()
        value_type = IRType.getTypeMapInv(suffix_type)
        if a_t == b_t == value_type:
            self.stack.append((value_type, a - b))
        else:
            raise TypeError("SUB requiere enteros")

    def op_MUL(self, suffix_type: str):
        b_t, b = self.stack.pop()
        a_t, a = self.stack.pop()
        value_type = IRType.getTypeMapInv(suffix_type)
        if a_t == b_t == value_type:
            self.stack.append((value_type, a * b))
        else:
            raise TypeError("MUL requiere enteros")

    def op_DIV(self, suffix_type: str):
        b_t, b = self.stack.pop()
        a_t, a = self.stack.pop()
        value_type = IRType.getTypeMapInv(suffix_type)
        if a_t == b_t == value_type:
            if value_type == "int":
                self.stack.append((value_type, a // b))
            elif value_type == "float":
                self.stack.append((value_type, a / b))
            else:
                raise TypeError("DIV requiere enteros o flotantes")
        else:
            raise TypeError("DIV requiere enteros")

    def op_EQ(self, suffix_type: str):
        b_t, b = self.stack.pop()
        a_t, a = self.stack.pop()
        value_type = IRType.getTypeMapInv(suffix_type)
        if a_t == b_t == value_type:
            self.stack.append((value_type, a == b))
        else:
            raise TypeError("EQ requiere enteros")

    def op_GT(self, suffix_type: str):
        b_t, b = self.stack.pop()
        a_t, a = self.stack.pop()
        value_type = IRType.getTypeMapInv(suffix_type)
        if a_t == b_t == value_type:
            self.stack.append((value_type, a > b))
        else:
            raise TypeError("GT requiere enteros")

    def op_LT(self, suffix_type: str):
        b_t, b = self.stack.pop()
        a_t, a = self.stack.pop()
        value_type = IRType.getTypeMapInv(suffix_type)
        if a_t == b_t == value_type:
            self.stack.append((value_type, a < b))
        else:
            raise TypeError("LT requiere enteros")

    def op_LE(self, suffix_type: str):
        b_t, b = self.stack.pop()
        a_t, a = self.stack.pop()
        value_type = IRType.getTypeMapInv(suffix_type)
        if a_t == b_t == value_type:
            self.stack.append((value_type, a <= b))
        else:
            raise TypeError("LE requiere enteros")

    def op_NE(self, suffix_type: str):
        b_t, b = self.stack.pop()
        a_t, a = self.stack.pop()
        value_type = IRType.getTypeMapInv(suffix_type)
        if a_t == b_t == value_type:
            self.stack.append((value_type, a != b))
        else:
            raise TypeError("NE requiere enteros")

    def op_PRINT(self, suffix_type: str):
        """Imprime el valor del tope de la pila según el tipo especificado"""
        t, v = self.stack.pop()
        print(v)

    # ---- instrucciones ----
    def op_CONST(self, value, suffix_type: str):
        """Maneja constantes y las agrega al stack con su tipo correcto"""
        # Mapear el tipo de IR a nuestro tipo interno

        value_type = IRType.getTypeMapInv(suffix_type)
        if value_type is None:
            raise TypeError(f"Tipo no soportado: {suffix_type}")

        # Convertir el valor al tipo correspondiente
        parsed_value = None

        try:
            if value_type == "int":
                parsed_value = int(value)
            elif value_type == "float":
                parsed_value = float(value)
            elif value_type == "char":
                if isinstance(value, int):
                    parsed_value = chr(value)  # Convertir código ASCII a char
                else:
                    parsed_value = value[0]  # Tomar el primer carácter si es string
            elif value_type == "bool":
                parsed_value = bool(value)

            self.stack.append((value_type, parsed_value))

        except (ValueError, TypeError) as e:
            raise TypeError(f"No se pudo convertir {value} a {value_type}: {str(e)}")

    # — locals —
    def op_LOCAL_SET(self, name):
        self._frame()[name] = self.stack.pop()

    def op_LOCAL_GET(self, name):
        if name in self._frame():
            self.stack.append(self._frame()[name])
        else:
            raise RuntimeError(f"Variable local '{name}' no encontrada")

    # — control de flujo —
    def op_CALL(self, fn_label):
        pts = self.params_map.get(fn_label, [])
        args = [self.stack.pop() for _ in pts][::-1]
        frame = dict(zip(pts, args))

        self.call_stack.append(self.pc)  # ❶  guarda i
        self.frames.append(frame)

        self.pc = self.functions[fn_label] - 1  # ❷  ir a la función (-1)

    def op_RET(self):
        self.frames.pop()  # sale del marco
        if self.call_stack:
            self.pc = self.call_stack.pop()  # recupera i
        else:
            self.running = False
