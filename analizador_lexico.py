import sys

class AnalizadorLexico:
    def __init__(self, codigo_base):
        self.codigo_base = codigo_base
        self.tokens =[]
        self.linea_actual = 1
        self.columna_actual = 1
        self.posicion_actual = 0
        self.errores = []
        
    #saltador de comentarios
    def skip_comentario(self):
        while self.posicion_actual < len(self.codigo_base) and self.codigo_base[self.posicion_actual] != '\n':
            self.posicion_actual += 1
            self.columna_actual += 1
    
    #identificadores y palabras claves
    def identicadores_o_keywords(self):
        posicion_inicial = self.posicion_actual
        linea_inicial = self.linea_actual
        columna_inicial = self.columna_actual
        
        while (self.posicion_actual < len(self.codigo_base)) and (self.codigo_base[self.posicion_actual].isalnum() or self.codigo_base[self.posicion_actual] == '_'):
            self.posicion_actual += 1
            self.columna_actual += 1
            
        lexeme = self.codigo_base[posicion_inicial:self.posicion_actual]
        
        #palabras reservadas de python
        keywords = [
            'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
            'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
            'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
            'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
            'try', 'while', 'with', 'yield', 'object', 'bool', 'str', 'int'
        ]
        
        if lexeme in keywords:
            self.tokens.append(f"<{lexeme},{linea_inicial},{columna_inicial}>")
        else:
            self.tokens.append(f"<id,{lexeme},{linea_inicial},{columna_inicial}>")
    
    #prosesar numeros
    def procesar_numeros(self):
        posicion_inicial = self.posicion_actual
        linea_inicial = self.linea_actual
        columna_inicial = self.columna_actual
        
        #manejo de signos
        if (self.codigo_base[self.posicion_actual] =='+' or self.codigo_base[self.posicion_actual] == '-'):
            self.posicion_actual += 1
            self.columna_actual += 1
            
        while (self.posicion_actual < len(self.codigo_base)) and self.codigo_base[self.posicion_actual].isdigit():
            self.posicion_actual += 1
            self.columna_actual += 1
            
        #verificar si es un punto decimal, pero no tomarlo como flotante
        if (self.posicion_actual < len(self.codigo_base)) and self.codigo_base[self.posicion_actual] == '.':
            #tratar el punto '.' como token individual
            lexeme = self.codigo_base[posicion_inicial:self.posicion_actual]
            #lexeme puede estar vacio si solo hay un signo antes del punto
            if lexeme:
                self.tokens.append(f"<tk_entero,{lexeme},{linea_inicial},{columna_inicial}>")
                return
            
            lexeme = self.codigo_base[posicion_inicial:self.posicion_actual]
            self.tokens.append(f"<tk_entero,{lexeme},{linea_inicial},{columna_inicial}>")
            
    #procesar strings
    def procesar_strings(self):
        linea_inicial = self.linea_actual
        columna_inicial = self.columna_actual
        quote_char = self.codigo_base[self.posicion_actual]
        self.posicion_actual += 1
        self.columna_actual += 1
        posicion_inicial = self.posicion_actual
        
        while (self.posicion_actual < len(self.codigo_base) and self.codigo_base[self.posicion_actual] != quote_char):
            if self.codigo_base[self.posicion_actual] == '\n':
                self.errores.append(f">>>error lexico(linea:{linea_inicial},posicion:{columna_inicial})")
                return
            self.posicion_actual += 1
            self.columna_actual += 1
            
        if self.posicion_actual >= len(self.codigo_base):
            self.errores.append(f">>>error lexico(linea:{linea_inicial},posicion:{columna_inicial})")
            return
        
        lexeme = self.codigo_base[posicion_inicial:self.posicion_actual]
        #esta suma es para saltar la comilla de cierre
        self.posicion_actual += 1
        self.columna_actual += 1
        
        self.tokens.append(f"<tk_cadena,\"{lexeme}\",{linea_inicial},{columna_inicial}>")
        
    #procesar operadores y simbolos
    def procesar_operador_y_simbolo(self):
        char = self.codigo_base[self.posicion_actual]
        linea_inicial = self.linea_actual
        columna_inicial = self.columna_actual
        
        #mapeo de operaciones y simbolos con sus respectivos tokens
        operadores = {
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
        
        #se verefica la existencia de un token con 2 caracteres
        if self.posicion_actual + 1 < len(self.codigo_base):
            two_char = self.codigo_base[self.posicion_actual] +  self.codigo_base[self.posicion_actual + 1]
            if two_char in operadores:
                self.tokens.append(f"<{operadores[two_char]},{linea_inicial},{columna_inicial}>")
                self.posicion_actual += 2
                self.columna_actual += 2
                return
            
        #operadores de 1 caracter
        if char in operadores:
            self.tokens.append(f"<{operadores[char]},{linea_inicial},{columna_inicial}>")
            self.posicion_actual += 1
            self.columna_actual += 1
        else:
            #errores
            self.errores.append(f">>>error lexico(linea:{linea_inicial},posicion:{columna_inicial})")
            self.posicion_actual += 1
            self.columna_actual += 1
    
    def analizar(self):
        while self.posicion_actual < len(self.codigo_base):
            char = self.codigo_base[self.posicion_actual]
            
            #ignorar los espacios en blanco pero contar su posicion
            if char in ' \t':
                self.posicion_actual += 1
                self.columna_actual += 1
                continue
                
            #saltos de linea
            if char == '\n':
                self.posicion_actual += 1
                self.columna_actual = 1
                self.linea_actual += 1
                continue
            
            #ignorar comentarios
            if char == '#':
                self.skip_comentario()
                continue
            
            #proseso de diferentes tokens
            if char.isalpha() or char == '_':
                self.identicadores_o_keywords()
            elif char.isdigit():
                self.procesar_numeros()
            elif char == '"' or char == "'":
                self.procesar_strings()
            else:
                self.procesar_operador_y_simbolo()
            
        return self.tokens, self.errores
    
#leer archivo
def main():
        if len(sys.argv) != 2:
            print("uso correcto: python analizador_lexico.py <archivo_entrada>")
            return
        
        archivo = sys.argv[1]
        
        try:
            #la r del segundo argumento es el modo de apertura 'r' = apertura
            #el tercer argumento es la especificacion codificacion del texto
            with open(archivo, 'r',encoding='utf-8') as f:
                codigo_leido = f.read()
                
            analizador = AnalizadorLexico(codigo_leido)
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
            
                
                
                
            