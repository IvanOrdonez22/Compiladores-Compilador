from lexico import identificar_tokens
from sintactico import Parser

def main():
    codigo_fuente = """
    int procesarDatos(int x, int y) {
      int resultado = 0;
      if (x > y) {
        println(x);
      } else {
        println(y);
      }
      for (int i = 0; i < x; i = i + 1) {
        resultado = resultado + i;
      }
      while (resultado > 100) {
        resultado = resultado - 1;
      }
      return resultado;
    }
    """
    
    print("--- Generando Traducción a RUST (HT05) ---")
    tokens = identificar_tokens(codigo_fuente)
    parser = Parser(tokens)
    
    try:
        arbol = parser.parsear()
        print(arbol.traducirRust())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()