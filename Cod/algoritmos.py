from collections import deque

#########################################################################
# BACKTRACKING
#########################################################################

def backtracking(variables, k=0):
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
# AC3
#########################################################################

def ac3(variables):

    #cola con todos los arcos (vi, vj, posición del cruce en vi, posición en vj)
    cola = deque()
    for vi in variables:
        for (vj, posI, posJ) in vi.getRestricciones():
            cola.append((vi, vj, posI, posJ))
    enCola = set(cola)

    while cola:
        arco = cola.popleft()
        enCola.discard(arco)
        (vi, vj, posI, posJ) = arco

        if revisar(vi, vj, posI, posJ):
            if not vi.getDominio():
                return False

            #el dominio de vi ha cambiado: hay que revisar los arcos (vk, vi)
            for (vk, posI2, posK) in vi.getRestricciones():
                if vk is not vj:
                    nuevo = (vk, vi, posK, posI2)
                    if nuevo not in enCola:
                        cola.append(nuevo)
                        enCola.add(nuevo)

    return True

def revisar(vi, vj, posI, posJ):
    dominioJ = vj.getDominio()

    #cuántos valores de vj tiene cada letra en la celda de cruce
    letras = {}
    for b in dominioJ:
        letras[b[posJ]] = letras.get(b[posJ], 0) + 1

    setJ = None
    nuevo = []
    for a in vi.getDominio():
        soportes = letras.get(a[posI], 0)

        #el propio valor "a" en vj no vale como soporte, ya que no valen 
        #palabras repetidas. Solo hace falta comprobarlo si "a" es el único candidato
        if soportes == 1 and len(a) > 1 and len(a) == vj.getLongitud() and a[posJ] == a[posI]:
            if setJ is None:
                setJ = set(dominioJ)
            if a in setJ:
                soportes = 0

        if soportes > 0:
            nuevo.append(a)

    if len(nuevo) != len(vi.getDominio()):
        vi.setDominio(nuevo)
        return True
    return False


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