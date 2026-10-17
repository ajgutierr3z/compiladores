
import ply.lex as lex
import ply.yacc as yacc

# --- 1. ANALIZADOR LÉXICO (Tokens) ---
tokens = (
    'NUMERO',
    'SUMA',
    'RESTA',
    'MULTIPLICA',
    'DIVIDE',
    'PAREN_IZQ',
    'PAREN_DER',
)

t_SUMA       = r'\+'
t_RESTA      = r'-'
t_MULTIPLICA = r'\*'
t_DIVIDE     = r'/'
t_PAREN_IZQ  = r'\('
t_PAREN_DER  = r'\)'

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# --- 2. ANALIZADOR SINTÁCTICO (Gramática y Precedencia) ---
# RECUERDA: EL ESTUDIANTE DEBE AJUSTAR LA PRECEDENCIA PARA EVITAR AMBIGÜEDAD
precedence = (
    # (Completar como parte de la práctica: definir precedencia de +, -, *, /)
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICA', 'DIVIDE'),
)

def p_expresion_binaria(p):
    '''expresion : expresion SUMA expresion
                 | expresion RESTA expresion
                 | expresion MULTIPLICA expresion
                 | expresion DIVIDE expresion'''
    if p[2] == '+': p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expresion_agrupacion(p):
    'expresion : PAREN_IZQ expresion PAREN_DER'
    p[0] = p[2]

def p_expresion_numero(p):
    'expresion : NUMERO'
    p[0] = p[1]

def p_error(p):
    print("Error de sintaxis en la entrada!")

parser = yacc.yacc()

# --- 3. PRUEBA DEL ANALIZADOR EN ENTORNO COLABORATIVO ---
if __name__ == '__main__':
    print("Iniciando pruebas automáticas del Analizador Sintáctico...\n")
    
    # Lista estática de expresiones para evitar el uso de input() que bloquea Colab/Jupyter
    casos_de_prueba = [
        "3 + 4 * 5",               # Prueba de precedencia simple
        "(3 + 4) * 5",             # Prueba de agrupación
        "10 / 2 + 3",              # División y suma
        "(10 + 2) / 3 * 4",        # Agrupación con operadores de diferente precedencia
        "100 - 20 * 3 + 10 / 2"    # Expresión compleja
    ]

    for expresion in casos_de_prueba:
        print(f"Evaluando: {expresion}")
        try:
            resultado = parser.parse(expresion)
            print(f"Resultado calculado: {resultado}\n")
        except Exception as e:
            print(f"Error procesando la expresión: {e}\n")
            
    print("Pruebas finalizadas. Si los resultados no son los matemáticamente correctos, revisa la tupla de precedencia.")
