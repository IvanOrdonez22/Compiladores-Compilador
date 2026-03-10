class NodoAST:
    pass

class NodoFuncion(NodoAST):
    def __init__(self, tipo, nombre, parametros, cuerpo):
        self.tipo = tipo
        self.nombre = nombre
        self.parametros = parametros
        self.cuerpo = cuerpo

    def traducirRust(self):
        params = ", ".join(p.traducirRust() for p in self.parametros)
        cuerpo = "\n    ".join(c.traducirRust() for c in self.cuerpo)
        # Rust usa fn nombre(p: tipo) -> tipo { ... }
        return f"fn {self.nombre[1]}({params}) -> {self.tipo[1]} {{\n    {cuerpo}\n}}"

class NodoParametro(NodoAST):
    def __init__(self, tipo, nombre):
        self.tipo, self.nombre = tipo, nombre
    def traducirRust(self):
        # Rust usa nombre: tipo
        return f"{self.nombre[1]}: {self.tipo[1]}"

class NodoAsignacion(NodoAST):
    def __init__(self, tipo, nombre, expresion):
        self.tipo, self.nombre, self.expresion = tipo, nombre, expresion
    def traducirRust(self):
        # Si tiene tipo, es una declaración 'let mut'
        if self.tipo:
            return f"let mut {self.nombre[1]}: {self.tipo[1]} = {self.expresion.traducirRust()};"
        return f"{self.nombre[1]} = {self.expresion.traducirRust()};"

class NodoIf(NodoAST):
    def __init__(self, condicion, cuerpo_if, cuerpo_else=None):
        self.condicion, self.cuerpo_if, self.cuerpo_else = condicion, cuerpo_if, cuerpo_else
    def traducirRust(self):
        c_if = "\n        ".join(c.traducirRust() for c in self.cuerpo_if)
        res = f"if {self.condicion.traducirRust()} {{\n        {c_if}\n    }}"
        if self.cuerpo_else:
            c_else = "\n        ".join(c.traducirRust() for c in self.cuerpo_else)
            res += f" else {{\n        {c_else}\n    }}"
        return res

class NodoWhile(NodoAST):
    def __init__(self, condicion, cuerpo):
        self.condicion, self.cuerpo = condicion, cuerpo
    def traducirRust(self):
        c = "\n        ".join(inst.traducirRust() for inst in self.cuerpo)
        return f"while {self.condicion.traducirRust()} {{\n        {c}\n    }}"

class NodoFor(NodoAST):
    def __init__(self, inicial, condicion, incremento, cuerpo):
        self.inicial, self.condicion, self.incremento, self.cuerpo = inicial, condicion, incremento, cuerpo
    def traducirRust(self):
        # Traducimos el for de C a un bloque loop/while de Rust
        c = "\n        ".join(inst.traducirRust() for inst in self.cuerpo)
        return f"{self.inicial.traducirRust()}\n    while {self.condicion.traducirRust()} {{\n        {c}\n        {self.incremento.traducirRust()}\n    }}"

class NodoPrint(NodoAST):
    def __init__(self, exp): self.exp = exp
    def traducirRust(self): 
        # Rust usa macros con ! para imprimir
        return f'println!("{{}}", {self.exp.traducirRust()});'

class NodoOperacion(NodoAST):
    def __init__(self, izq, op, der): self.izq, self.op, self.der = izq, op, der
    def traducirRust(self): return f"{self.izq.traducirRust()} {self.op[1]} {self.der.traducirRust()}"

class NodoIdent(NodoAST):
    def __init__(self, n): self.n = n
    def traducirRust(self): return self.n[1]

class NodoNumero(NodoAST):
    def __init__(self, v): self.v = v
    def traducirRust(self): return self.v[1]

class NodoRetorno(NodoAST):
    def __init__(self, e): self.e = e
    def traducirRust(self): return f"return {self.e.traducirRust()};"