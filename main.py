from lexico import identificar_tokens

def main():
    # Ejemplo que contiene todas las instrucciones de la HT02
    codigo_prueba = """
    int main() {
        if (x > 0) {
            print(x);
        } else {
            println(0);
        }
        for (int i = 0; i < 10; i = i + 1) {
            while (i < 5) {
                print(i);
            }
        }
    }
    """
    
    print("Iniciando Analizador Léxico para HT02...")
    tokens = identificar_tokens(codigo_prueba)
    
    # Imprimimos los tokens de forma ordenada
    print(f"{'TIPO DE TOKEN':<20} | {'VALOR':<15}")
    print("-" * 40)
    for tipo, valor in tokens:
        print(f"{tipo:<20} | {valor:<15}")

if __name__ == "__main__":
    main()