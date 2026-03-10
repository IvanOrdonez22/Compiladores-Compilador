from node import *

class Parser:
    def __init__(self, tokens):
        self.tokens, self.pos = tokens, 0

    def obtener_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def coincidir(self, tipo):
        t = self.obtener_token()
        if t and t[0] == tipo:
            self.pos += 1
            return t
        raise SyntaxError(f"Se esperaba {tipo}, se encontró {t}")

    def parsear(self): return self.funcion()

    def funcion(self):
        tipo, nom = self.coincidir('KEYWORD'), self.coincidir('IDENTIFIER')
        self.coincidir('DELIMITER'); params = self.parametros(); self.coincidir('DELIMITER')
        self.coincidir('DELIMITER'); cuerpo = self.cuerpo(); self.coincidir('DELIMITER')
        return NodoFuncion(tipo, nom, params, cuerpo)

    def parametros(self):
        lista = []
        if self.obtener_token() and self.obtener_token()[1] != ')':
            lista.append(NodoParametro(self.coincidir('KEYWORD'), self.coincidir('IDENTIFIER')))
            while self.obtener_token() and self.obtener_token()[1] == ',':
                self.coincidir('DELIMITER'); lista.append(NodoParametro(self.coincidir('KEYWORD'), self.coincidir('IDENTIFIER')))
        return lista

    def cuerpo(self):
        insts = []
        while self.obtener_token() and self.obtener_token()[1] != '}':
            val = self.obtener_token()[1]
            if val == 'if': insts.append(self.sentencia_if())
            elif val == 'while': insts.append(self.sentencia_while())
            elif val == 'for': insts.append(self.sentencia_for())
            elif val in ('print', 'println'): insts.append(self.sentencia_print())
            elif val == 'return': insts.append(self.retorno())
            else: insts.append(self.asignacion())
        return insts

    def sentencia_if(self):
        self.coincidir('KEYWORD'); self.coincidir('DELIMITER')
        cond = self.expresion(); self.coincidir('DELIMITER')
        self.coincidir('DELIMITER'); c_if = self.cuerpo(); self.coincidir('DELIMITER')
        c_else = None
        if self.obtener_token() and self.obtener_token()[1] == 'else':
            self.coincidir('KEYWORD'); self.coincidir('DELIMITER')
            c_else = self.cuerpo(); self.coincidir('DELIMITER')
        return NodoIf(cond, c_if, c_else)

    def sentencia_while(self):
        self.coincidir('KEYWORD'); self.coincidir('DELIMITER')
        cond = self.expresion(); self.coincidir('DELIMITER')
        self.coincidir('DELIMITER'); cuer = self.cuerpo(); self.coincidir('DELIMITER')
        return NodoWhile(cond, cuer)

    def sentencia_for(self):
        self.coincidir('KEYWORD'); self.coincidir('DELIMITER')
        ini = self.asignacion()
        cond = self.expresion(); self.coincidir('DELIMITER')
        nom = self.coincidir('IDENTIFIER'); self.coincidir('OPERATOR')
        inc = NodoAsignacion(None, nom, self.expresion()); self.coincidir('DELIMITER')
        self.coincidir('DELIMITER'); cuer = self.cuerpo(); self.coincidir('DELIMITER')
        return NodoFor(ini, cond, inc, cuer)

    def sentencia_print(self):
        self.coincidir('KEYWORD'); self.coincidir('DELIMITER')
        exp = self.expresion(); self.coincidir('DELIMITER'); self.coincidir('DELIMITER')
        return NodoPrint(exp)

    def asignacion(self):
        t, n = self.coincidir('KEYWORD'), self.coincidir('IDENTIFIER')
        self.coincidir('OPERATOR'); e = self.expresion(); self.coincidir('DELIMITER')
        return NodoAsignacion(t, n, e)

    def retorno(self):
        self.coincidir('KEYWORD'); e = self.expresion(); self.coincidir('DELIMITER')
        return NodoRetorno(e)

    def expresion(self):
        izq = self.termino()
        while self.obtener_token() and self.obtener_token()[0] == "OPERATOR":
            op, der = self.coincidir("OPERATOR"), self.termino()
            izq = NodoOperacion(izq, op, der)
        return izq

    def termino(self):
        t = self.obtener_token()
        if t[0] == "NUMBER": return NodoNumero(self.coincidir("NUMBER"))
        if t[0] == "IDENTIFIER": return NodoIdent(self.coincidir("IDENTIFIER"))
        raise SyntaxError("Error sintáctico")