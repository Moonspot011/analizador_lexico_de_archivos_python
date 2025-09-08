Este proyecto implementa un analizador léxico en Python basado en un Autómata Finito Determinista (AFD) explícito.
El analizador recorre el código fuente de entrada, reconoce tokens válidos del lenguaje (identificadores, palabras reservadas, números, cadenas, operadores, símbolos, etc.), 
y detecta errores léxicos.


Un conjunto de estados (q0, qID, qNUM, qCAD, qCOM, qERR).

Una función de transición δ, implementada como un diccionario:

delta = { (estado, clase_caracter): (nuevo_estado, accion) }

Un conjunto de acciones semánticas (iniciar_numero, skip_comentario, etc.) que construyen tokens, ignoran espacios, o registran errores

Características:

Uso de AFD

Reconocimiento de:

- Palabras reservadas (if, else, while, class, return, …).

- Identificadores (combinaciones de letras, dígitos y _, no iniciados en dígito).

- Números enteros (con o sin signo).

- Cadenas de caracteres delimitadas por ' o ".

- Operadores simples y dobles (+, -, *, /, ==, !=, <=, >=, etc.).

- Símbolos especiales (;, ,, (, ), {, }, …).

- Comentarios de línea iniciados con #.

Manejo de espacios y saltos de línea (ignorados como tokens).

Detección de errores léxicos:

- Caracteres no válidos.

- Números mal formados (ejemplo: 123abc).

- Cadenas sin cerrar.

Uso:

Ejecutar el analizador:

python3 analizador_lexico_AFD.py

Ingresar el archivo a analizar cuando lo solicite, por ejemplo:

ingrese el nombre del archivo a analizar:
archivo_test.py

El programa generará como salida:

- Una lista de tokens reconocidos.

- El errore léxico (si lo hay).
