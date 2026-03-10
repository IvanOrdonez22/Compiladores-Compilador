class NodoAST: pass

class NodoFuncion(NodoAST):
    def __init__(self, tipo, nombre, parametros, cuerpo):
        self.tipo, self.nombre, self.parametros, self.cuerpo = tipo, nombre, parametros, cuerpo
    def traducirPy(self):
        params = ", ".join(p.traducirPy() for p in self.parametros)
        cuerpo = "\n  ".join(c.traducirPy() for c in self.cuerpo)
        return f"def {self.nombre[1]}({params}):\n  {cuerpo}"

class NodoIf(NodoAST):
    def __init__(self, condicion, cuerpo_if, cuerpo_else=None):
        self.condicion, self.cuerpo_if, self.cuerpo_else = condicion, cuerpo_if, cuerpo_else
    def traducirPy(self):
        c_if = "\n    ".join(c.traducirPy() for c in self.cuerpo_if)
        res = f"if {self.condicion.traducirPy()}:\n    {c_if}"
        if self.cuerpo_else:
            c_else = "\n    ".join(c.traducirPy() for c in self.cuerpo_else)
            res += f"\n  else:\n    {c_else}"
        return res

class NodoWhile(NodoAST):
    def __init__(self, condicion, cuerpo):
        self.condicion, self.cuerpo = condicion, cuerpo
    def traducirPy(self):
        c = "\n    ".join(inst.traducirPy() for inst in self.cuerpo)
        return f"while {self.condicion.traducirPy()}:\n    {c}"

class NodoFor(NodoAST):
    def __init__(self, inicial, condicion, incremento, cuerpo):
        self.inicial, self.condicion, self.incremento, self.cuerpo = inicial, condicion, incremento, cuerpo
    def traducirPy(self):
        c = "\n    ".join(inst.traducirPy() for inst in self.cuerpo)
        return f"{self.inicial.traducirPy()}\n  while {self.condicion.traducirPy()}:\n    {c}\n    {self.incremento.traducirPy()}"

class NodoPrint(NodoAST):
    def __init__(self, exp): self.exp = exp
    def traducirPy(self): return f"print({self.exp.traducirPy()})"

class NodoAsignacion(NodoAST):
    def __init__(self, tipo, nombre, expresion):
        self.tipo, self.nombre, self.expresion = tipo, nombre, expresion
    def traducirPy(self): return f"{self.nombre[1]} = {self.expresion.traducirPy()}"

class NodoOperacion(NodoAST):
    def __init__(self, izq, op, der): self.izq, self.op, self.der = izq, op, der
    def traducirPy(self): return f"{self.izq.traducirPy()} {self.op[1]} {self.der.traducirPy()}"

class NodoIdent(NodoAST):
    def __init__(self, n): self.n = n
    def traducirPy(self): return self.n[1]

class NodoNumero(NodoAST):
    def __init__(self, v): self.v = v
    def traducirPy(self): return self.v[1]

class NodoRetorno(NodoAST):
    def __init__(self, e): self.e = e
    def traducirPy(self): return f"return {self.e.traducirPy()}"

class NodoParametro(NodoAST):
    def __init__(self, tipo, nombre):
        self.tipo, self.nombre = tipo, nombre
    def traducirPy(self): return self.nombre[1]