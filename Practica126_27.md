

## SISTEMAS INTELIGENTES
Departamento de Ciencia de la Computación e Inteligencia Artificial
Universidad de Alicante   Curso 2026/2027

Práctica 1. Satisfacción de restricciones

## Objetivos:
- Implementar algoritmos básicos en satisfacción de restricciones.
- Aplicar estos algoritmos a un problema concreto, la generación de crucigramas.

Sesión 1: Introducción, entorno de trabajo y clase Variable
En esta primera práctica de la asignatura se deben desarrollar algoritmos de búsqueda en problemas
de satisfacción de restricciones para generar un crucigrama, es decir, encontrar las palabras que se
ajustan a los huecos del crucigrama, tanto en horizontal como en vertical.
Cuando una palabra colocada en horizontal en el crucigrama se cruza con otra vertical, la posición en
la  que  se  cruzan  debe  contener  el  mismo  carácter.  Hay  que  tener  en  cuenta  que  en  cada  fila  o
columna del tablero puede haber más de una palabra dependiendo de las casillas negras que tenga
el crucigrama.
Se proporcionan 2 plantillas para realizar, una de ellas usa el paquete tkinter y la otra no. Se puede
usar cualquiera de las dos.
Plantilla A: usa tkinter
Entorno gráfico desarrollado en Python en el cual es posible establecer tanto las casillas ocupadas
como  caracteres  concretos  en  cualquier  casilla.  Haciendo  click  con  el  botón  izquierdo  del  ratón
introduciremos una casilla ocupada (cuadrado relleno en negro) o bien dejaremos vacía una casilla
que no lo estuviera. Con el botón derecho se nos presentará un dialogo para introducir un carácter
en la casilla.



El tamaño del crucigrama (número de filas y número de columnas), así como el fichero de texto que
actúa como diccionario (contiene las palabras que se pueden emplear para generar el crucigrama) se
introducen como parámetro al ejecutar el código. Si no se especifican parámetros toma como valores
por defecto 5 filas, 6 columnas y el fichero d0.txt como diccionario.
Ejecución del proyecto
Ejecutar  el  fichero  main.py con  los  parámetros  que  se  desee:  número  de  filas  y  columnas  del
crucigrama y fichero de texto con palabras
main.py --filas M --columnas N --dic fichero.txt
Plantilla B: no usa tkinter
Entorno gráfico desarrollado en Python en el se crea un crucigrama a partir de un fichero de texto
que contiene la información necesaria. El formato de este fichero de texto es tantas líneas como filas
tiene el crucigrama, 0 para las celdas en blanco, 1 para las celdas en negro y una letra para las celdas
ya asignadas. Si no se especifican parámetros toma como valores por defecto el fichero plantilla1.txt
para construir en crucigrama y el fichero d0.txt como diccionario.
Ejemplo de fichero de texto para la construcción del crucigrama:

Ejecución del proyecto
Ejecutar el  fichero main.py  con  los  parámetros  que  se  desee: plantilla del crucigrama  y  fichero  de
texto con palabras
main.py --plantilla fichero.txt --dic fichero.txt
## Funcionamiento
Al  ejecutar  el programa aparecerá la  cuadrícula  del  crucigrama En  la  parte derecha aparecen  tres
botones que cuando se pulsa en ellos se ocupan de llamar a los algoritmos que hay que implementar.
Para poder generar un crucigrama es necesario disponer de una lista de palabras que se usarán para
rellenar las celdas. Estas palabras estarán en un fichero de texto que se cargará al iniciar el entorno.
## Botones:
- BK:   aplicar   el   algoritmo   backtracking/backjumping.  Estos algoritmos pueden
aplicarse tanto para una cuadrícula con su configuración inicial como tras la ejecución
de AC3. En este último caso los dominios de las variables al comenzar a ejecutar serán
los devueltos por AC3.

- FC:  aplicar el algoritmo Forward Checking. Este algoritmo puede aplicarse tanto para
una  cuadrícula  con  su  configuración  inicial  como  tras  la  ejecución  de  AC3.  En  este
último  caso  los  dominios  de  las  variables  al  comenzar  a  ejecutar  FC  serán  los
devueltos por AC3.
- AC3:  aplicar  el  algoritmo  AC3.  Este  algoritmo  permite  reducir  los  dominios  de  las
variables y elimina inconsistencias de arista.

Al pinchar  en  los botones BK  o  FC se generará el crucigrama empleando  el  algoritmo
correspondiente y se mostrará en el tablero la solución del crucigrama.


## Desarrollo
El entorno se ha desarrollado en Python usando el paquete pygame. Pygame facilita la creación de
videojuegos en dos dimensiones y permite programar la parte multimedia (gráficos, sonido y manejo
de eventos) de forma sencilla.
El entorno proporcionado está compuesto por 2 ficheros:
- main: es el fichero que hay que ejecutar para lanzar el entorno. Tiene el bucle principal de
manejo, así como el desarrollo del interfaz gráfico
- tablero: permite construir un objeto tablero que contiene las dimensiones de este, así como
la matriz que representa las celdas del crucigrama.

Como herramienta de desarrollo se utilizará Thonny.  Thonny es un IDE con los elementos básicos
para crear aplicaciones en el lenguaje Python, es posible depurar y observar las variables en ejecución
de forma sencilla.
Cuando se lanza el entorno, la función creaAlmacen() se ocupa de abrir el fichero de texto y crear el
almacén de palabras, es decir, un diccionario de palabras organizados por el tamaño de la palabra.

El entorno muestra en todo momento el contenido de la variable tablero. Por eso, cuando una celda
del tablero tiene valor muestra su contenido en pantalla (función pintarTablero)
La clase Variable
Para  implementar  los algoritmos  descritos  es  esta  práctica  es  fundamental  la  clase  Variable.  El
objetivo  de  los  algoritmos  es  encontrar  un  valor  válido  para  cada  variable.  En  este  problema  una
variable se corresponde con el conjunto de celdas (horizontal o vertical) que contiene una palabra.
La figura ilustra dos variables horizontales (borde rojo) y dos verticales (borde verde).

La clase Variable debe contener toda la información necesaria para ello: nombre, tipo (h/v), posición,
dominio, restricciones, etc.
Para  resolver  el  problema  hay  que  encontrar  asignaciones  válidas  para  todas  las  variables  del
crucigrama. No debe haber palabras repetidas en el crucigrama.
Tareas a realizar en esta sesión:
- Prueba el entorno. Averigua cómo acceder a una celda del crucigrama.
- Implementa la clase Variable con las funcionalidades que consideres adecuadas
- Construye el conjunto de variables

Sesión 2: Implementación del algoritmo backtracking
El algoritmo backtracking cada vez que asigna un valor a la variable actual (Vk) comprueba que sea
consistente con las variables ya asignadas. Si no lo es, abandona esta asignación y prueba con otro
valor del dominio. Si ya ha probado todos los valores del dominio retrocede para probar otro valor
para la variable Vk-1. Si prueba todos los valores del dominio de esta variable y ningún valor es
válido retrocede a la variable anterior y así sucesivamente.


La función test devuelve verdadero si la asignación de valor a Vk es consistente con las variables ya
asignadas.
Tareas a realizar en esta sesión:
- Implementa el algoritmo backtracking

Sesiones 3 y 4: Implementación del algoritmo Forward Checking.
Hito intermedio de entrega
El algoritmo Forward Checking asigna valores a las variables que componen el problema. Cada vez
que asigna un valor a una variable (variable actual), comprueba esa asignación con las variables que
todavía  están  sin  instanciar  (variables  futuras)  que  están  restringidas  con  la  variable  actual.  Los
valores de   las   variables   futuras   que   son   inconsistentes   con   esa   asignación   son   eliminados
temporalmente de los dominios de las variables. Si el dominio de una variable futura se queda vacío,
la instanciación de la variable actual se deshace y se prueba con otro valor.

Detalles de implementación

Para  que  se  considere  válido  el  algoritmo  forward  checking  se  debe  implementar  de  manera
adecuada.  Debe  haber  una  clase Variable y  los  objetos  de  dicha  clase  deben  tener  un  dominio, el
algoritmo  va  eliminando  y  restaurando valores de  ese  dominio  conforme  va  avanzando  en  la
ejecución.  El  objetivo  final  del  algoritmo  es  que  cada  variable  tenga  un  valor  asignado.  Cuando  se
asigna  un  valor  a  una  variable,  esa  asignación  debe  causar  podas  en  los  dominios  de  las  variables
futuras (variables que todavía no tienen un valor asignado) y cuando se deshace una asignación de
un  valor  a  una  variable,  el  procedimiento  restaura  debe  revisar  las  variables  futuras  que  están
restringidas con la variable actual y debe deshacer las eliminaciones causadas por dicha variable.

Tareas a realizar en estas sesiones:
- Implementar el algoritmo Forward checking.
- Antes de la sesión 5 se debe entregar el proyecto

Sesiones 5 y 6: Implementación del algoritmo AC3
En estas sesiones se va a implementar el algoritmo AC3. Este algoritmo transforma un problema en
otro sin inconsistencias de arco. Cuando se pulse en el botón del AC3 se debe mostrar por pantalla
los dominios de cada variable antes y después de ejecutar el algoritmo. Ejemplo:




Este algoritmo no resuelve el problema, solo reduce los valores inconsistentes del dominio.



Si se pulsa primero en el botón del AC3 y a continuación en el botón FC o en el BK, estos algoritmos
deben trabajar con los dominios ya reducidos por el AC3.
Tarea a realizar en estas sesiones:
- Implementar el algoritmo AC3
Sesión 7: Implemementación del algoritmo backjumping (optativo)
Este algoritmo evita el trashing que se produce en el backtracking debido a que cuando todas las
asignaciones de valor a una variable fallan, el algoritmo vuelve a la variable anterior para probar
otro valor, cuando a lo mejor la inconsistencia viene generada por un valor que se asignó a una
variable varios niveles anteriores. Bakctracking probará muchas combinaciones y hará múltiples
retrocesos hasta llegar a la causa del conflicto.
Backjumping mejora el baktracking saltando directamente al origen del conflicto, para ello cada
variable lleva un conjunto de conflictos, es decir, ha de saber qué variables pasadas son las
responsables de que no pueda usar alguno de los valores de su dominio.


Sesión 8: Documentación y pruebas. Hito final
Esta última sesión está dedicada a terminar las pruebas y finalizar la documentación que se habrá ido
elaborando de manera continua durante todo el desarrollo de la práctica.
La documentación es la parte más importante de la práctica. Como mínimo debe contener:
- Explicación de la clase Variable
- Explicación de cómo se han tratado las casillas con caracteres fijos.
- Especificación formal del problema. La especificación formal debe detallar la tupla <V, E, c,
l,  a> para  un  crucigrama  concreto de  máximo  8  variables  que  se  ponga  como  ejemplo
ilustrativo, así como un pequeño diccionario de palabras.
- Traza del problema pequeño de FC. Realizar una traza a partir del crucigrama especificado
en  el  punto  anterior de  cómo  evolucionan  los  dominios  de  las variables  indicando  valores
podados tras cada asignación que hace el algoritmo.
- Traza con el mismo crucigrama anterior del algoritmo AC3.
- Experimentación en la que se  describan las diferentes pruebas realizadas a los algoritmos,
dejando bien claro el objetivo de las pruebas. Debe haber pruebas con distintos tamaños de
crucigramas y distintas casuísticas: sin solución ya determinado por el AC3, AC3 deja valores
en el dominio, pero el problema no tiene solución, y con solución
- Estudio  de  tiempos  de  los  algoritmos  para  distintos  tamaños  de  crucigramas  y  distintos
diccionarios: BK, BJ, FC, AC3, AC3+BK, AC3+FC, AC3+BJ.

- Utilización de gráficas para el análisis de tiempos.
- Dificultades encontradas.
- Conclusiones obtenidas tras la realización de la práctica.
- Uso de IAs generativas: explicación del uso que se ha hecho de ellas.
- Apartado de referencias bibliográficas.
Entrega de la práctica
La  fecha  límite  de  entrega  de  la práctica completa es  el 1 de noviembre de  2026 a las  23:55h.  La
entrega se realizará a través de Moodle.

Evaluación de la practica
La  realización  de  la  parte  obligatoria  de  la  práctica  supone  el 85%  de  la  nota,  el  15%  restante  se
obtiene con la implementación de la parte optativa

Formato de entrega del proyecto para el hito 2 (entrega final)
La entrega debe consistir en un fichero comprimido zip con dos carpetas:
- /Cod: todos los ficheros .py, elementos gráficos y ficheros de texto para construir los
crucigramas que constituyen la práctica
- /Doc: fichero pdf con la documentación

## ¡¡¡AVISO IMPORTANTE!!!

No cumplir cualquiera de las normas de formato/entrega puede suponer un suspenso en la práctica.

Recordad que las prácticas son INDIVIDUALES y NO se pueden hacer en parejas o grupos.

Cualquier código copiado supondrá un suspenso de la práctica para todas las personas implicadas
en  la  copia y,  como  indica  el  Reglamento  para  la  Evaluación  de  Aprendizajes  de  la  Universidad  de
Alicante (BOUA 24/07/2025) y el documento de Actuación ante copia en pruebas de evaluación de
la  EPS, se  informará  a  la  dirección  de  la  Escuela  Politécnica  Superior  para  la  toma  de  medidas
oportunas.


Plan de entrega por hitos
Durante  el  periodo  de  ejecución  de  la  práctica  se  realizarán dos hitos  de  entrega.  Es
obligatorio cumplir las fechas de las entregas correspondientes:
Hito  Entrega Fecha tope
## 1
## (intermedio)
Todos los ficheros .py y elementos gráficos que constituyen
la práctica. No es necesario entregar documentación
11 de octubre
2 (final) Práctica completa siguiendo la estructura del formato
de entrega
1 de noviembre


- La no entrega del hito 1 en la fecha prevista supone una penalización del 20%.
- Para la entrega final se dejará el programa empleando la heurística más adecuada.
Las otras heurísticas analizadas aparecerán en el código, aunque no se utilicen.

La nota de la práctica sufrirá una penalización de dos puntos si no se cumple rigurosamente
con los requisitos de la entrega (tanto en la estructura de los ficheros entregados como en la
salida que debe generar la práctica)
