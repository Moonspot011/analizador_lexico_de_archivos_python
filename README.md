ESTRUCTURA DEL PROYECTO:
-analizador_lexico_AFD.py
-archivo_test.py

EXPLICACIÓN
Este proyecto implementa un analizador léxico en Python basado en un Autómata Finito Determinista (AFD) explícito.
El analizador recorre el código fuente de entrada, reconoce tokens válidos del lenguaje (identificadores, palabras reservadas, números, cadenas, operadores, símbolos, etc.), 
y detecta errores léxicos.

-Un conjunto de estados (q0, qID, qNUM, qCAD, qCOM, qERR).

-Una función de transición δ, implementada como un diccionario:

  delta={(estado, clase_caracter):(nuevo_estado, accion)}

-Un conjunto de acciones semánticas (iniciar_numero, skip_comentario, etc.) que construyen tokens, ignoran espacios, o registran errores


CARACTERISTICAS:

-Uso de AFD

-Reconocimiento de:

  *Palabras reservadas (if, else, while, class, return, …).

  *Identificadores (combinaciones de letras, dígitos y _, no iniciados en dígito).

  *Números enteros (con o sin signo).

  *Cadenas de caracteres delimitadas por ' o ".

  *Operadores simples y dobles (+, -, *, /, ==, !=, <=, >=, etc.).

  *Símbolos especiales (;, ,, (, ), {, }, …).

  *Comentarios de línea iniciados con #.
  

-Manejo de espacios y saltos de línea (ignorados como tokens).

-Detección de errores léxicos:

  *Caracteres no válidos.

  *Números mal formados (ejemplo: 123abc).

  *Cadenas sin cerrar.


COMO EJECUTAR ?
En la terminal debes ingresar lo siguiente, dependiendo la version de python que tengas:

>python analizador_lexico_AFD.py
ó
>python3 analizador_lexico_AFD.py


Al ejecutar, la salida debe mostrar un mensaje para ingresar el archivo a analizar y ahi se debe ingresar el nombre tal cual del archivo que se usara de prueba, por ejemplo:

ingrese el nombre del archivo a analizar:
archivo_test.py

Entonces al ingresarlo, el programa generara como salida un archivo lex que contiene:

- Una lista de tokens reconocidos.

- El errore léxico (si lo hay).

Realizado por Juan Esteban Martinez Cantero y Juan Camilo Camacho Mejía
