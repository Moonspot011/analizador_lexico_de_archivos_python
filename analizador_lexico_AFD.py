class AnalizadorLexicoAFD:
    def __init__(self, codigo_base):
        self.codigo_base = codigo_base
        self.tokens =[]
        self.linea_actual = 1
        self.columna_actual = 1
        self.posicion_actual = 0
        self.lexema = ""
        self.errores = []
        #todas las palabras reservadas de python
        self.keywords = [
            'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
            'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
            'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
            'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
            'try', 'while', 'with', 'yield', 'object', 'bool', 'str', 'int'
        ] 
        #mapeo de operaciones y simbolos con sus respectivos tokens
        self.operadores = {
            '(': 'tk_par_izq',
            ')': 'tk_par_der',
            '[': 'tk_cor_izq',
            ']': 'tk_cor_der',
            '{': 'tk_llave_izq',
            '}': 'tk_llave_der',
            ',': 'tk_coma',
            ':': 'tk_dos_puntos',
            '.': 'tk_punto',
            ';': 'tk_punto_coma',
            '+': 'tk_suma',
            '-': 'tk_resta',
            '*': 'tk_multi',
            '/': 'tk_div',
            '%': 'tk_modulo',
            '=': 'tk_asignar',
            '==': 'tk_igual',
            '!=': 'tk_distinto',
            '<': 'tk_menor',
            '>': 'tk_mayor',
            '<=': 'tk_menor_igual',
            '>=': 'tk_mayor_igual',
            '->': 'tk_ejecuta',
            '**': 'tk_potencia',
            '//': 'tk_div_entera',
            '@': 'tk_arroba',
        }
        self.delta = {
            # Estado q0
            ("q0", "letra"): ("q0", "iniciar_lexema"),
            ("q0", "digito"): ("q0", "iniciar_numero"),
            ("q0", "signo"): ("q0", "signo_o_operador"),
            ("q0", "comilla"): ("q0", "iniciar_string"),
            ("q0", "comentario"): ("q0", "skip_comentario"),
            ("q0", "espacio"): ("q0", "skip"),
            ("q0", "nueva_linea"): ("q0", "nueva_linea"),
            ("q0", "operador"): ("q0", "check_operador"),
            ("q0", "otro"): ("qERR", "error"),
            ("q0", "EOF"): ("q0", "final"),

            # Estado qCAD (cadena)
            ("qCAD", "comilla"): ("q0", "emit_string"),  # cerrar cadena
            ("qCAD", "nueva_linea"): ("qERR", "error"),  # error si salto dentro
            ("qCAD", "EOF"): ("qERR", "error"),          # error si fin antes de cierre
            # cualquier otro char en cadena sigue siendo parte del string
            ("qCAD", "letra"): ("qCAD", "add_char"),
            ("qCAD", "digito"): ("qCAD", "add_char"),
            ("qCAD", "signo"): ("qCAD", "add_char"),
            ("qCAD", "comentario"): ("qCAD", "add_char"),
            ("qCAD", "espacio"): ("qCAD", "add_char"),
            ("qCAD", "operador"): ("qCAD", "add_char"),
            ("qCAD", "otro"): ("qCAD", "add_char"),

            # Estado qCOM (comentario hasta fin de línea)
            ("qCOM", "nueva_linea"): ("q0", "skip"),   # termina comentario
            ("qCOM", "EOF"): ("q0", "skip"),           # comentario al final del archivo
            # cualquier otro carácter dentro del comentario simplemente se ignora
            ("qCOM", "letra"): ("qCOM", "skip"),
            ("qCOM", "digito"): ("qCOM", "skip"),
            ("qCOM", "signo"): ("qCOM", "skip"),
            ("qCOM", "comilla"): ("qCOM", "skip"),
            ("qCOM", "comentario"): ("qCOM", "skip"),
            ("qCOM", "espacio"): ("qCOM", "skip"),
            ("qCOM", "operador"): ("qCOM", "skip"),
            ("qCOM", "otro"): ("qCOM", "skip"),

        }
    
    def mirar(self, k = 0):
        if self.posicion_actual + k < len(self.codigo_base):
            return self.codigo_base[self.posicion_actual + k]
        return None
    
    def avance(self, n=1):
        for _ in range(n):
            if self.posicion_actual >= len(self.codigo_base):
                return
            caracter = self.codigo_base[self.posicion_actual]
            self.posicion_actual += 1
            
            if caracter == '\n':
                self.linea_actual += 1
                self.columna_actual = 1
            else:
                self.columna_actual += 1
            
    def tipo_caracter(self, caracter):
        if caracter is None:
            return 'EOF'
        if caracter.isalpha() or caracter == '_':
            return 'letra'
        if caracter.isdigit():
            return 'digito'
        if caracter in '+-':
            return 'signo'
        if caracter in ("'", '"'):
            return 'comilla'
        if caracter in (' ', '\t'):
            return 'espacio'
        if caracter == '\n':
            return 'nueva_linea'
        if caracter == '#':
            return 'comentario'
        if caracter in self.operadores:
            return 'operador'
        return 'otro'
        
    def ejecutar_accion(self, accion, caracter):
        if accion == "iniciar_lexema":
            self.lexema = caracter
            self.avance()
           
            while self.tipo_caracter(self.mirar()) in ('letra', 'digito'):
                self.lexema += self.mirar()
                self.avance()
            
            if self.lexema in self.keywords:
                self.tokens.append(f"<{self.lexema},{self.linea_actual},{self.columna_actual - len(self.lexema)}>")
            else:
                self.tokens.append(f"<id,{self.lexema},{self.linea_actual},{self.columna_actual - len(self.lexema)}>")
            self.lexema = ""
        elif accion == "iniciar_numero":
            self.lexema = caracter
            self.avance()
            while self.tipo_caracter(self.mirar()) == 'digito':
                self.lexema += self.mirar()
                self.avance()
            self.tokens.append(f"<tk_entero,{self.lexema},{self.linea_actual},{self.columna_actual - len(self.lexema)}>")
            self.lexema = ""
        elif accion == "signo_o_operador":
            if self.mirar(1) and self.mirar(1).isdigit():
                self.lexema = caracter
                self.avance()
            else:
                self.tokens.append(f"<{self.operadores[caracter]},{self.linea_actual},{self.columna_actual}>")
                self.avance()
        elif accion == "iniciar_string":
            comilla = caracter
            self.avance()
            posicion_inicial = self.posicion_actual
            while True:
                char = self.mirar()
                if char is None or char == '\n':
                    self.errores.append(f">>>error lexico(lines:{self.linea_actual},posicion:{self.columna_actual})")
                    return "qERR"
                if char == comilla:
                    self.lexema = self.codigo_base[posicion_inicial:self.posicion_actual]
                    self.tokens.append(f"<tk_string,{self.lexema},{self.linea_actual},{self.columna_actual - len(self.lexema) - 1}>")
                    self.lexema = ""
                    self.avance()
                    break
                self.avance()  
        elif accion == "skip":
            self.avance()
        elif accion == "nueva_linea":
            self.avance()
        elif accion == "skip_comentario":
            while self.mirar() not in (None, '\n'):
                self.avance()
            if self.mirar() == '\n':
                self.avance()
        elif accion == "check_operador":
            dos_operadores = (self.mirar() or '') + (self.mirar(1) or '')
            if dos_operadores in self.operadores:
                self.tokens.append(f"<{self.operadores[dos_operadores]},{self.linea_actual},{self.columna_actual}>")
                self.avance(2)
            elif self.mirar() in self.operadores:
                self.tokens.append(f"<{self.operadores[self.mirar()]},{self.linea_actual},{self.columna_actual}>")
                self.avance()
            else:
                self.errores.append(f">>>error lexico(linea:{self.linea_actual},posicion:{self.columna_actual})")
                return "qERR"
        elif accion == "error":
            self.errores.append(f">>>error lexico(linea:{self.linea_actual},posicion:{self.columna_actual})")
            return "qERR"
        elif accion == "final":
            return "final" 
    
    def analizar(self):
        estado = "q0"
        while True:
            caracter = self.mirar()
            tipo = self.tipo_caracter(caracter)
            nuevo_estado, accion = self.delta.get((estado, tipo), ("qERR", "error"))
            estado_resultado = self.ejecutar_accion(accion, caracter)
            if estado_resultado in ("qERR", "final"):
                break
            estado = nuevo_estado
        return self.tokens, self.errores
    
#leer archivo
def main():
        
        try:
            archivo = input("ingrese el nombre del archivo a analizar: \n")
            
            #la r del segundo argumento es el modo de apertura 'r' = apertura
            #el tercer argumento es la especificacion codificacion del texto
            with open(archivo, 'r',encoding='utf-8') as f:
                codigo_leido = f.read()
                
            analizador = AnalizadorLexicoAFD(codigo_leido)
            tokens, errores = analizador.analizar()
            
            if errores:
                print(errores)
            else:
                #poner los tokens en el archivo a crear
                archivo_salida = archivo + '.lex'
                # 'w' = modo escritura
                with open(archivo_salida, 'w', encoding='utf-8') as f:
                    for token in tokens:
                        f.write(token + '\n')
                        
                print(f"Analisis lexico completo, resultado en el archivo {archivo_salida}")
        
        except FileNotFoundError:
            print(f"Error: No se pudo encontrar el archivo {archivo}")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            
if __name__ == "__main__":
    main()




