import os
from lexico import identificar_tokens
from sintactico import Parser

def compilar_nasm(codigo_asm):
    # 1. Guardar el código en un archivo .asm
    with open("salida.asm", "w") as f:
        f.write(codigo_asm)
    
    print("Compilando con NASM...")
    # 2. Ejecutar NASM (Genera archivo objeto .o)
    os.system("nasm -f elf64 salida.asm -o salida.o")
    
    print("Enlazando con LD...")
    # 3. Ejecutar LD (Enlaza con librerías de C para usar printf)
    os.system("ld salida.o -o programa -lc -I /lib64/ld-linux-x86-64.so.2")
    
    print("¡Listo! Ejecutable 'programa' generado.")

def main():
    codigo_fuente = """
    void main() {
      print(100);
      print(25);
    }
    """
    tokens = identificar_tokens(codigo_fuente)
    parser = Parser(tokens)
    
    try:
        arbol = parser.parsear()
        codigo_asm = arbol.traducirAsm()
        print("--- CÓDIGO ENSAMBLADOR GENERADO ---")
        print(codigo_asm)
        
        # Llamamos al método de compilación
        compilar_nasm(codigo_asm)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()