%%writefile analizador.py
import ply.lex as lex

# 1. Diccionario de Palabras Reservadas
reserved = {
    'if': 'RESERVADA_IF',
    'else': 'RESERVADA_ELSE',
    'while': 'RESERVADA_WHILE',
    'int': 'RESERVADA_INT',
    'float': 'RESERVADA_FLOAT'
}

# 2. Lista de todos los Tokens
tokens = [
    'ID',
    'NUMERO',
    'OPERADOR',
    'PUNTUACION',
] + list(reserved.values())

# 3. Expresiones Regulares para tokens simples
t_OPERADOR = r'[\+\-\*/=]'
t_PUNTUACION = r'[\{\}\(\);,]'

# Ignorar espacios y tabulaciones
t_ignore  = ' \t'

# 4. Reglas con lógica adicional (Funciones)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Verifica si el identificador es en realidad una palabra reservada
    t.type = reserved.get(t.value, 'ID')    
    return t

def t_NUMERO(t):
    r'\d+(\.\d+)?'
    # Convierte el valor a float o int para mantener el tipo de dato
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Regla para contar saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# 5. Manejo de Errores Léxicos
def t_error(t):
    print(f"Línea {t.lexer.lineno}: ERROR LÉXICO (Carácter no reconocido) -> '{t.value[0]}'")
    t.lexer.skip(1)

# 6. Construcción del Analizador Léxico
lexer = lex.lex()

# Bloque principal de ejecución
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        archivo_entrada = sys.argv[1]
        try:
            with open(archivo_entrada, 'r') as file:
                data = file.read()
                
            print("--- INICIANDO ANÁLISIS LÉXICO CON PLY ---")
            lexer.input(data)
            
            # Recorrer y mostrar cada token encontrado
            for tok in lexer:
                print(f"Línea {tok.lineno}: {tok.type} -> {tok.value}")
                
            print("--- FIN DEL ANÁLISIS ---")
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{archivo_entrada}'")
    else:
        print("Uso correcto: python analizador.py codigo_prueba.txt")
