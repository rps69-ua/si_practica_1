#########################################################################
# BACKTRACKING
#########################################################################

def backtracking(variables, k=0):

    #limpiar previamente la lista de variables si se ejecutan dos algoritmos
    #seguidos, desasignando todos los valores y restaurando todas las podas
    if k == 0:
        limpiar(variables) 

    if k == len(variables):
        return True

    variable = variables[k]

    for valor in variable.getDominio():
        if consistente(variable, valor, variables, k):
            variable.asignar(valor)
            if backtracking(variables, k+1):
                return True
            variable.desasignar()

    return False

def consistente(variable, valor, variables, k):

    #comprobar que el valor no corta con una letra (y esta es distinta) de otra variable
    for (otra, posSelf, posOtra) in variable.getRestricciones():
        if otra.estaAsignada():
            if valor[posSelf]!=otra.getValor()[posOtra]:
                return False

    #para variables de más de una letra, comprobar que su valor no se repite con el de otra
    if len(valor) > 1:
        for otra in variables[:k]:
            if otra.getValor() == valor:
                return False

    return True



#########################################################################
# FORWARD CHECKING
#########################################################################

def forward_checking(variables, k=0):

    #limpiar previamente la lista de variables si se ejecutan dos algoritmos
    #seguidos, desasignando todos los valores y restaurando todas las podas
    if k == 0:
        limpiar(variables)        

    if k == len(variables):
        return True

    variable = variables[k]

    for valor in variable.getDominio():
        variable.asignar(valor)              
        if forward(variables, k, valor):
            if forward_checking(variables, k+1):
                return True
        restaurar(variables, k)
        variable.desasignar()

    return False

#Podar de las variables posteriores a "i" aquellos valores 
#que no son consistentes con el valor "a" asignado a "i"
def forward(variables, i, a):
    variable = variables[i]

    for j in range(i+1, len(variables)):
        otra = variables[j]
        for b in list(otra.getDominio()):
            if not es_consistente(variable, a, otra, b):
                otra.getDominio().remove(b)
                otra.getPodado().append((b, variable))

        if len(otra.getDominio()) == 0:
            return False

    return True

#Restaurar los valores podados por "i"
def restaurar(variables, i):
    variable = variables[i]

    for j in range(i+1, len(variables)):
        otra = variables[j]
        for (b, responsable) in list(otra.getPodado()):
            if responsable is variable:
                otra.getPodado().remove((b, responsable))
                otra.getDominio().append(b)

#Comprobar que el valor "a" de "vi" es consistente con el valor "b" de "vj"
def es_consistente(vi, a, vj, b):

    #misma comprobación de no repetición de valores que en backtracking
    if len(a) > 1 and a == b:
        return False
    
    for (otra, posSelf, posOtra) in vi.getRestricciones():
        if otra is vj:
            if a[posSelf] != b[posOtra]:
                return False

    return True



#########################################################################
# UTILIDADES
#########################################################################

#Volcar la solución final en el tablero
def volcarSolucion(tablero, variables):
    for v in variables:
        if v.estaAsignada():
            palabra = v.getValor()
            for i, (f, c) in enumerate(v.getCeldas()):
                tablero.setCelda(f, c, palabra[i])

#Limpiar la lista de variables si se ejecuta backtracking inmediatamente
#después de forward checking o viceversa, desasignando todos los valores
#y restaurando todas las podas
def limpiar(variables):
    for v in variables:
        for (valorPodado, responsable) in list(v.getPodado()):
            v.getPodado().remove((valorPodado, responsable))
            v.getDominio().append(valorPodado)
        v.desasignar()