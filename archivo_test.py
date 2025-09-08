# Esto es un comentario que debe ser ignorado
class Animal(object):
    makes_noise: bool = False

    def make_noise(self: "Animal") -> object:
        if self.makes_noise:
            print("El animal hace:", self.sound())
    
    def sound(self: "Animal") -> str:
        return "???"

class Perro(Animal):
    def __init__(self: "Perro"):
        self.makes_noise = True
    
    def sound(self: "Perro") -> str:
        return "Guau!"

mi_mascota: Animal = None
mi_mascota = Perro()
mi_mascota.make_noise()  

# Operaciones matemáticas
x = 10 + 5 * 3
y = (x - 15) / 2.5
z = x ** 2 // y

# Comparaciones
if x > y and y <= z:
    print("Condición cumplida")