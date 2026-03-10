from lexico import identificar_tokens
from sintactico import Parser

def main():
    codigo = """
    int tareaHT03(int n) {
      if (n > 0) {
        println(n);
      } else {
        print(0);
      }
      for (int i = 0; i < n; i = i + 1) {
        print(i);
      }
      while (n > 0) {
        n = n - 1;
      }
      return n;
    }
    """
    tokens = identificar_tokens(codigo)
    parser = Parser(tokens)
    try:
        arbol = parser.parsear()
        print("--- AST Generado y Traducido (HT03) ---")
        print(arbol.traducirPy())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()