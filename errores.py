import re

# Función para evaluar expresiones
def evaluar_expresion(expresion, tabla_simbolos):
    # Utiliza un diccionario vacío para evitar cambios en la tabla de símbolos
    local_dict = {}
    for variable, entrada in tabla_simbolos.items():
        if entrada['Valor'] is not None:
            local_dict[variable] = entrada['Valor']
    try:
        resultado = eval(expresion, {}, local_dict)
        return resultado
    except (NameError, SyntaxError, ZeroDivisionError):
        return None

# Función para analizar una línea de código y agregar entradas a la tabla de símbolos
def analizar_linea(linea, tabla_simbolos, numero_linea, registro):
    linea = linea.strip()  # Eliminar espacios en blanco al principio y al final
    if linea:
        palabras = re.findall(r'\S+', linea)
        if palabras:
            tipo = palabras[0]
            variables = palabras[1:]
            for variable in variables:
                if ',' in variable:
                    # Elimina las comas y divide las variables
                    variables_divididas = variable.split(',')
                    for variable_dividida in variables_divididas:
                        nombre = variable_dividida.strip(';')
                        if nombre not in tabla_simbolos:
                            print(f"Error en la linea {numero_linea}: Variable '{nombre}' no declarada previamente.")
                else:
                    nombre = variable.strip(';')
                    if nombre not in tabla_simbolos:
                        print(f"Error en la linea {numero_linea}: Variable '{nombre}' no declarada previamente.")
                    else:
                        tabla_simbolos[nombre]['Tipo'] = tipo
                        registro += 1

    return registro

# Inicializar la tabla de símbolos y el registro de memoria
tabla_simbolos = {}
numero_linea = 1
registro_memoria = 0

# Leer el archivo de texto línea por línea
with open('testSemantica.txt', 'r') as archivo:
    lineas = archivo.readlines()

for linea in lineas:
    registro_memoria = analizar_linea(linea, tabla_simbolos, numero_linea, registro_memoria)
    numero_linea += 1

# Imprimir la tabla de símbolos con la variable, el registro de memoria y la verificación de tipos
for nombre, entrada in tabla_simbolos.items():
    print("Nombre:", entrada['Nombre'])
    print("Variable:", entrada['Variable'])
    print("Tipo:", entrada['Tipo'])
    print("Valor:", entrada['Valor'])
    print("Registro (loc):", entrada['Registro (loc)'])
    print("Numero de linea:", entrada['Número de línea'])
    print()

# Analizar expresiones y asignar tipos
for nombre, entrada in tabla_simbolos.items():
    if entrada['Valor']:
        tipo_asignado = type(entrada['Valor']).__name__
        if entrada['Tipo'] != tipo_asignado:
            print(f"Error: Variable '{nombre}' tiene tipo '{entrada['Tipo']}', pero se le asignó un valor de tipo '{tipo_asignado}'.")

# Evaluar expresiones aritméticas constantes
for nombre, entrada in tabla_simbolos.items():
    if entrada['Valor']:
        if isinstance(entrada['Valor'], str):
            valor_asignado = evaluar_expresion(entrada['Valor'], tabla_simbolos)
            if valor_asignado is not None:
                entrada['Valor'] = valor_asignado


