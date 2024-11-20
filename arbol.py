class Nodo:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def __str__(self, nivel=0):
        nodo_str = "  " * nivel + f"Tipo: {self.tipo}"
        if self.valor is not None:
            nodo_str += f", Valor: {self.valor}"
        nodo_str += "\n"
        for hijo in self.hijos:
            nodo_str += hijo.__str__(nivel + 1)
        return nodo_str

# Función para analizar el código fuente y construir el árbol sintáctico
def analizar_codigo(codigo):
    raiz = Nodo("Programa")
    funcion_main = Nodo("Funcion", "main")
    raiz.agregar_hijo(funcion_main)

    # Lógica para analizar las declaraciones y asignaciones
    declaraciones = Nodo("Declaraciones")
    funcion_main.agregar_hijo(declaraciones)
    declaraciones.agregar_hijo(Nodo("Declaracion", "int x, y, z;"))
    declaraciones.agregar_hijo(Nodo("Declaracion", "real a, b, c, x, a;"))
    declaraciones.agregar_hijo(Nodo("Asignacion", "suma := 45;"))
    declaraciones.agregar_hijo(Nodo("Asignacion", "x := 32.32;"))
    declaraciones.agregar_hijo(Nodo("Asignacion", "x := 23;"))
    declaraciones.agregar_hijo(Nodo("Asignacion", "y := 2 + 3 - 1;"))
    declaraciones.agregar_hijo(Nodo("Asignacion", "z := y + 7;"))
    declaraciones.agregar_hijo(Nodo("Asignacion", "y := y + 1;"))
    declaraciones.agregar_hijo(Nodo("Asignacion", "a := 24.0 + 4 - 1 / 3 * 2 + 34 - 1;"))
    declaraciones.agregar_hijo(Nodo("Asignacion", "x := (5 - 3) * (8 / 2);"))
    declaraciones.agregar_hijo(Nodo("Asignacion", "y := 5 + 3 - 2 * 4 / 7 - 9;"))
    declaraciones.agregar_hijo(Nodo("Asignacion", "z := 8 / 2 + 15 * 4;"))
    declaraciones.agregar_hijo(Nodo("Asignacion", "y := 14.54;"))

    # Lógica para analizar las estructuras condicionales y bucles
    condicional = Nodo("Condicional")
    funcion_main.agregar_hijo(condicional)
    condicional.agregar_hijo(Nodo("Condicion", "if (2 > 3)"))
    entonces = Nodo("Entonces")
    condicional.agregar_hijo(entonces)
    entonces.agregar_hijo(Nodo("Asignacion", "y := a + 3;"))
    sino = Nodo("Sino")
    condicional.agregar_hijo(sino)
    sino.agregar_hijo(Nodo("Condicion", "if (4 > 2)"))
    dentro_sino = Nodo("Entonces")
    sino.agregar_hijo(dentro_sino)
    dentro_sino.agregar_hijo(Nodo("Asignacion", "b = 3.2;"))
    sino.agregar_hijo(Nodo("Sino"))
    dentro_sino.agregar_hijo(Nodo("Asignacion", "b = 5.0;"))
    dentro_sino.agregar_hijo(Nodo("FinSino"))
    condicional.agregar_hijo(Nodo("Asignacion", "y := y + 1;"))
    condicional.agregar_hijo(Nodo("FinCondicion"))

    funcion_main.agregar_hijo(Nodo("Asignacion", "a++;"))
    funcion_main.agregar_hijo(Nodo("Asignacion", "c--;"))
    funcion_main.agregar_hijo(Nodo("Asignacion", "x := 3 + 4;"))

    bucle = Nodo("Bucle")
    funcion_main.agregar_hijo(bucle)
    bucle.agregar_hijo(Nodo("Asignacion", "do"))
    dentro_bucle = Nodo("DentroBucle")
    bucle.agregar_hijo(dentro_bucle)
    dentro_bucle.agregar_hijo(Nodo("Asignacion", "y = (y + 1) * 2 + 1;"))
    dentro_bucle.agregar_hijo(Nodo("Bucle", "while (x > 7)"))
    dentro_bucle.agregar_hijo(Nodo("Asignacion", "{"))
    dentro_bucle.agregar_hijo(Nodo("Asignacion", "x := 6 + 8 / 9 * 8 / 3;"))
    dentro_bucle.agregar_hijo(Nodo("Entrada", "cin x;"))
    dentro_bucle.agregar_hijo(Nodo("Asignacion", "mas := 36 / 7;"))
    dentro_bucle.agregar_hijo(Nodo("Asignacion", "};"))
    bucle.agregar_hijo(Nodo("Bucle", "while (y == 5);"))
    bucle.agregar_hijo(Nodo("Bucle", "while (y == 0)"))
    dentro_bucle = Nodo("DentroBucle")
    bucle.agregar_hijo(dentro_bucle)
    dentro_bucle.agregar_hijo(Nodo("Entrada", "cin mas;"))
    dentro_bucle.agregar_hijo(Nodo("Salida", "cout x + 32 / 54;"))
    dentro_bucle.agregar_hijo(Nodo("FinBucle"))

    return raiz

# Código fuente proporcionado
codigo_fuente = """
main {
    int x, y, z;
    real a, b, c, x, a;
    suma := 45;
    x := 32.32;
    x := 23;
    y := 2 + 3 - 1;
    z := y + 7;
    y := y + 1;
    a := 24.0 + 4 - 1 / 3 * 2 + 34 - 1;
    x := (5 - 3) * (8 / 2);
    y := 5 + 3 - 2 * 4 / 7 - 9;
    z := 8 / 2 + 15 * 4;
    y := 14.54;
    if (2 > 3) then
        y := a + 3;
    else
        if (4 > 2) then
            b = 3.2;
        else
            b = 5.0;
        end;
    y := y + 1;
    end;
    a++;
    c--;
    x := 3 + 4;
    do
        y = (y + 1) * 2 + 1;
    while (x > 7) {
        x := 6 + 8 / 9 * 8 / 3;
        cin x;
        mas := 36 / 7;
    };
    while (y == 5);
    while (y == 0) {
        cin mas;
        cout x + 32 / 54;
    };
}
"""

# Analizar el código y construir el árbol sintáctico
arbol_sintactico = analizar_codigo(codigo_fuente)

# Imprimir el árbol con anotaciones de tipo y valor
print(arbol_sintactico)
