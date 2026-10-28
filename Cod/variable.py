LLENA = '*'
VACIA = '-'

#########################################################################
# Clase Variable: representa una palabra (horizontal o vertical) del crucigrama
#########################################################################
class Variable:
    def __init__(self, nombre, tipo, fila, col, longitud):
        self.nombre = nombre
        self.tipo = tipo        # 'H' o 'V'
        self.fila = fila
        self.col = col
        self.longitud = longitud

        self.celdas = []
        if tipo == 'H':
            for i in range(longitud):
                self.celdas.append((fila, col + i))
        else:
            for i in range(longitud):
                self.celdas.append((fila + i, col))

        self.dominio = []
        self.valor = None
        self.restricciones = []   # (otraVariable, posSelf, posOtra)
        self.podado = []          # (valor, variableResponsable)

    def getNombre(self):
        return self.nombre

    def getTipo(self):
        return self.tipo

    def getPosicion(self):
        return (self.fila, self.col)

    def getLongitud(self):
        return self.longitud

    def getCeldas(self):
        return self.celdas

    def getDominio(self):
        return self.dominio

    def getValor(self):
        return self.valor

    def getRestricciones(self):
        return self.restricciones

    def getPodado(self):
        return self.podado

    def setDominio(self, dominio):
        self.dominio = dominio

    def asignar(self, valor):
        self.valor = valor

    def desasignar(self):
        self.valor = None

    def estaAsignada(self):
        return self.valor is not None

    def addRestriccion(self, otraVariable, posSelf, posOtra):
        self.restricciones.append((otraVariable, posSelf, posOtra))

    def contieneCelda(self, fila, col):
        return (fila, col) in self.celdas

    #posición (0..longitud-1) de una celda dentro de la variable
    def posicionDeCelda(self, fila, col):
        if (fila, col) in self.celdas:
            return self.celdas.index((fila, col))
        return None

    def __str__(self):
        return (f"Nombre {self.nombre} Posición {self.fila} {self.col} "
                f"Tipo: {'horizontal' if self.tipo == 'H' else 'vertical'} "
                f"Dominio: {self.dominio}")

    def __repr__(self):
        return self.__str__()



#########################################################################
# Recorre el tablero por filas (H) o columnas (V) y devuelve los huecos
# (fila, col, longitud) de casillas consecutivas distintas de LLENA
#########################################################################
def extraerHuecos(tablero):
    huecos = []
    alto = tablero.getAlto()
    ancho = tablero.getAncho()

    for tipo in ('H', 'V'):
        rango_ext, rango_int = (alto, ancho) if tipo == 'H' else (ancho, alto)

        for ext in range(rango_ext):
            inicio = None
            for interno in range(rango_int + 1):
                no_llena = False
                if interno < rango_int:
                    if tipo == 'H':
                        no_llena = (tablero.getCelda(ext, interno) != LLENA)
                    else:
                        no_llena = (tablero.getCelda(interno, ext) != LLENA)

                if interno < rango_int and no_llena:
                    if inicio is None:
                        inicio = interno
                else:
                    if inicio is not None:
                        longitud = interno - inicio
                        if tipo == 'H':
                            huecos.append((tipo, ext, inicio, longitud))
                        else:
                            huecos.append((tipo, inicio, ext, longitud))
                        inicio = None
    return huecos



#########################################################################
# Dominio de una variable: palabras del almacén de su longitud 
# compatibles con los caracteres ya fijados en el tablero
#########################################################################
def calculaDominio(tablero, variable, almacen):
    candidatas = almacen.get(variable.longitud, set())
    dominio = []

    for palabra in candidatas:
        valida = True
        for i, (f, c) in enumerate(variable.celdas):
            contenido = tablero.getCelda(f, c)
            if contenido != VACIA and contenido != LLENA:
                if palabra[i] != contenido:
                    valida = False
                    break
        if valida:
            dominio.append(palabra)

    return dominio



#########################################################################
# Construye el conjunto de variables del crucigrama (con dominio y restricciones)
#########################################################################
def construyeVariables(tablero, almacen):
    variables = []
    nombre = 0

    huecos = extraerHuecos(tablero)

    for (tipo, fila, col, longitud) in huecos:
        v = Variable(nombre, tipo, fila, col, longitud)
        v.setDominio(calculaDominio(tablero, v, almacen))
        variables.append(v)
        nombre += 1

    #restricciones: cruces entre variables horizontales y verticales
    for vh in variables:
        if vh.tipo != 'H':
            continue
        for vv in variables:
            if vv.tipo != 'V':
                continue
            interseccion = set(vh.celdas) & set(vv.celdas)
            if interseccion:
                (f, c) = interseccion.pop()
                posH = vh.posicionDeCelda(f, c)
                posV = vv.posicionDeCelda(f, c)
                vh.addRestriccion(vv, posH, posV)
                vv.addRestriccion(vh, posV, posH)

    return variables



#########################################################################
# Imprime el conjunto de variables
#########################################################################
def imprimeVariables(variables):
    for v in variables:
        print(v)
