import re

# 1. Definición de los patrones para los tokens
# Cada tupla contiene el nombre del token y su expresión regular
TOKENS_REGEX = [
    ('NUMBER',   r'\d+(\.\d+)?'),  # Números enteros o decimales
    ('PLUS',     r'\+'),           # Operador suma
    ('MINUS',    r'-'),            # Operador resta
    ('MULTIPLY', r'\*'),           # Operador multiplicación
    ('DIVIDE',   r'/'),            # Operador división
    ('LPAREN',   r'\('),           # Paréntesis izquierdo
    ('RPAREN',   r'\)'),           # Paréntesis derecho
    ('WS',       r'\s+'),          # Espacios en blanco
    ('MISMATCH', r'.'),            # Cualquier otro carácter (Error léxico)
]

def lex(codigo_fuente):
    """
    Función que analiza una cadena de texto y devuelve una lista de tokens.
    """
    tokens_encontrados = []
    # Combinar todas las expresiones regulares en una sola usando el operador OR (|)
    patron_global = '|'.join(f'(?P<{nombre}>{patron})' for nombre, patron in TOKENS_REGEX)
    
    for coincidencia in re.finditer(patron_global, codigo_fuente):
        tipo_token = coincidencia.lastgroup
        valor_token = coincidencia.group(tipo_token)
        
        if tipo_token == 'WS':
            continue  # Se ignoran los espacios en blanco
        elif tipo_token == 'MISMATCH':
            raise RuntimeError(f'Error Léxico: Carácter inesperado {valor_token!r}')
            
        tokens_encontrados.append((tipo_token, valor_token))
        
    return tokens_encontrados

# Código fuente de prueba
codigo_prueba = "(3 + 5) * 10.5"

# Ejecución
try:
    resultado = lex(codigo_prueba)
    print(f"Código fuente: {codigo_prueba}\n")
    print("Tokens generados:")
    for token in resultado:
        print(token)
except RuntimeError as e:
    print(e)
