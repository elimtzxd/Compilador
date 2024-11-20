import re

# Función para evaluar expresiones
def evaluar_expresion(expresion, tabla_simbolos):
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
                            tabla_simbolos[nombre] = {
                                'Nombre': nombre,
                                'Variable': '',
                                'Tipo': tipo,
                                'Valor': None,
                                'Registro (loc)': registro,
                                'Número de línea': [numero_linea]
                            }
                else:
                    nombre = variable.strip(';')
                    if nombre not in tabla_simbolos:
                        tabla_simbolos[nombre] = {
                            'Nombre': nombre,
                            'Variable': '',
                            'Tipo': tipo,
                            'Valor': None,
                            'Registro (loc)': registro,
                            'Número de línea': [numero_linea]
                        }
    return registro + 1

# Función para imprimir la tabla de símbolos en el formato deseado
def imprimir_tabla_simbolos(tabla_simbolos):
    print("{:<11} {:<7} {:<8} {:<13} {:<70}".format("Variable", "Tipo", "Valor", "L.Memoria", "# de Linea"))
    print("-" * 115)
    for nombre, entrada in tabla_simbolos.items():
        print("{:<11} {:<7} {:<8} {:<13} {}".format(entrada['Nombre'], entrada['Tipo'], entrada['Valor'], entrada['Registro (loc)'], ", ".join(map(str, entrada['Número de línea']))))

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

# Imprimir la tabla de símbolos con el nuevo formato
imprimir_tabla_simbolos(tabla_simbolos)

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

# Imprimir la tabla de símbolos actualizada
print("\nTabla de Simbolos Actualizada:")
imprimir_tabla_simbolos(tabla_simbolos)
