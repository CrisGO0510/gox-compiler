class StackMachine:
    def __init__(self):
        self.stack = []
        self.memory = [0] * 1024
        self.globals = {}
        self.locals_stack = []
        self.call_stack = []
        self.functions = {}
        self.pc = 0
        self.program = []
        self.running = False

    def load_program(self, program):
        self.program = program

    def run(self):
        self.pc = 0
        self.running = True
        while self.running and self.pc < len(self.program):
            instr = self.program[self.pc]
            opname = instr[0]
            args = instr[1:]
            method = getattr(self, f"op_{opname}", None)
            if method:
                method(*args)
            else:
                raise RuntimeError(f"Instrucción desconocida: {opname}")
            self.pc += 1

    def op_CONSTI(self, value):
        self.stack.append(("int", value))

    def op_ADDI(self):
        b_type, b = self.stack.pop()
        a_type, a = self.stack.pop()
        if a_type == b_type == "int":
            self.stack.append(("int", a + b))
        else:
            raise TypeError("ADDI requiere dos enteros")

    def op_PRINTI(self):
        val_type, value = self.stack.pop()
        if val_type == "int":
            print(value)
        else:
            raise TypeError("PRINTI requiere un entero")

    def op_CALL(self, func_label):
        self.call_stack.append(self.pc)
        self.pc = self.functions[func_label] - 1

    def op_LOCAL_SET(self, name):
        val = self.stack.pop()
        self.locals_stack.append((name, val))

    def op_LOCAL_GET(self, name):
        for local in reversed(self.locals_stack):
            if local[0] == name:
                self.stack.append(local[1])
                return
        raise RuntimeError(f"Variable local no encontrada: {name}")

    def op_RET(self):
        if self.call_stack:
            self.pc = self.call_stack.pop()
        else:
            self.running = False


program = [
    ("CONSTI", 4),
    ("LOCAL_SET", "i"),
    ("CONSTI", 3),
    ("LOCAL_SET", "j"),
    ("LOCAL_GET", "i"),
    ("LOCAL_GET", "j"),
    ("ADDI",),
    ("LOCAL_SET", "k"),
    ("LOCAL_GET", "i"),
    ("PRINTI",),
    ("LOCAL_GET", "k"),
    ("RET",),
]

vm = StackMachine()
vm.load_program(program)
vm.run()
