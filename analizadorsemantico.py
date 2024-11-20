# Definir una tabla de símbolos
symbol_table = {}

# Función para verificar la declaración de variables
def declare_variable(id, data_type, line_number):
    if id in symbol_table:
        print(f"Error: Variable '{id}' redeclarada en la línea {line_number}.")
    else:
        symbol_table[id] = {"data_type": data_type, "line_number": line_number}

# Función para verificar el uso de variables
def check_variable_usage(id, line_number):
    if id not in symbol_table:
        print(f"Error: Variable '{id}' no declarada en la línea {line_number}.")

# Leer el archivo de código fuente (testSemantica.txt)
file_name = "testSemantica.txt"

try:
    with open(file_name, "r") as file:
        lines = file.readlines()
except FileNotFoundError:
    print(f"Error: El archivo '{file_name}' no se encontró.")
    exit()

# Analizar el código línea por línea
for line_number, line in enumerate(lines, start=1):
    tokens = line.strip().split()
    if len(tokens) < 2:
        print(f"Error en la línea {line_number}: La línea no contiene suficientes tokens.")
        continue

    data_type, variable_declaration = tokens[0], tokens[1]
    if data_type in ["int", "real"]:
        # Verificar la declaración de variables
        variable_declaration = variable_declaration.strip(";")
        variable_ids = variable_declaration.split(",")
        for var in variable_ids:
            declare_variable(var, data_type, line_number)

    if data_type in ["cin", "cout"]:
        # Verificar el uso de variables en entrada o salida
        for token in tokens[1:]:
            if token not in [">>", "<<"]:
                check_variable_usage(token, line_number)

# Imprimir la tabla de símbolos con números de línea
print("\nTabla de Símbolos:")
for id, data in symbol_table.items():
    print(f"Variable -> {id} | Tipo -> {data['data_type']} | Línea -> {data['line_number']}")
