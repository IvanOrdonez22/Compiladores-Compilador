class NodoAST: pass

class NodoFuncion(NodoAST):
    def __init__(self, tipo, nombre, parametros, cuerpo):
        self.nombre = nombre
        self.cuerpo = cuerpo

    def traducirAsm(self):
        encabezado = (
            "section .data\n"
            "    fmt db '%d', 10, 0\n\n"
            "section .text\n"
            "    global _start\n"
            "    extern printf, exit\n\n"
            "_start:\n"
        )
        # Solo traducimos los prints para la HT06
        instrucciones = []
        for inst in self.cuerpo:
            if isinstance(inst, NodoPrint):
                instrucciones.append(inst.traducirAsm())
        
        cuerpo = "\n    ".join(instrucciones)
        final = "\n    mov rdi, 0\n    call exit\n"
        return encabezado + "    " + cuerpo + final

class NodoPrint(NodoAST):
    def __init__(self, exp): self.exp = exp
    def traducirAsm(self):
        return (
            f"mov rsi, {self.exp.traducirAsm()}\n"
            "    mov rdi, fmt\n"
            "    mov rax, 0\n"
            "    call printf"
        )

class NodoNumero(NodoAST):
    def __init__(self, v): self.v = v
    def traducirAsm(self): return self.v[1]

# Nodos "cascarón" para que el Parser no de error al encontrarlos
class NodoParametro(NodoAST):
    def __init__(self, tipo, nombre): pass

class NodoAsignacion(NodoAST):
    def __init__(self, tipo, nombre, expresion): pass

class NodoIf(NodoAST):
    def __init__(self, condicion, cuerpo_if, cuerpo_else=None): pass

class NodoWhile(NodoAST):
    def __init__(self, condicion, cuerpo): pass

class NodoFor(NodoAST):
    def __init__(self, inicial, condicion, incremento, cuerpo): pass

class NodoOperacion(NodoAST):
    def __init__(self, izq, op, der): pass

class NodoIdent(NodoAST):
    def __init__(self, n): pass

class NodoRetorno(NodoAST):
    def __init__(self, e): pass