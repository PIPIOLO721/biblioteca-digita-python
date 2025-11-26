from clases.libros import Libro
from clases.prestamos import Prestamo
from clases.usuarios import Usuario


class Biblioteca:
    def __init__(self):
        
        self.libros = [
            Libro("1984", "George Orwell"),
            Libro("Cien años de soledad", "Gabriel García Márquez"),
            Libro("Don Quijote de la Mancha", "Miguel de Cervantes"),
            Libro("La casa de los espíritus", "Isabel Allende"),
            Libro("Crimen y castigo", "Fyodor Dostoevsky"),
            Libro("El gran Gatsby", "F. Scott Fitzgerald"),
            Libro("Orgullo y prejuicio", "Jane Austen"),
            Libro("El principito", "Antoine de Saint-Exupéry"),
            Libro("Matar a un ruiseñor", "Harper Lee"),
            Libro("Ulises", "James Joyce"),
        ]
        
        self.usuarios = [
            Usuario("Juan Pérez", 12345678),
            Usuario("Ana Gómez", 23456789),
            Usuario("keyner lozano", 1109381992),
            Usuario("Marlon solis", 1107835973)
            
        ]
        self.prestamos = []  

    
    def mostrar_libros(self):
        print("\nLista de Libros Disponibles:")
        for libro in self.libros:
            print(f"- {libro.titulo} de {libro.autor}")

    
    def registrar_libro(self, titulo, autor):
        libro = Libro(titulo, autor)
        self.libros.append(libro)  
        print(f"El libro '{titulo}' ha sido registrado exitosamente.")

    
    def registrar_usuario(self, nombre, CC):
        
        if any(u.CC == CC for u in self.usuarios):
            print(f"El usuario con CC {CC} ya está registrado.")
        else:
            usuario = Usuario(nombre, CC)
            self.usuarios.append(usuario)
            print(f"El usuario {nombre} con CC {CC} ha sido registrado.")

    
    def prestar_libro(self, CC, titulo):
        usuario = next((u for u in self.usuarios if u.CC == CC), None)
        libro = next((l for l in self.libros if l.titulo.lower().strip() == titulo.lower().strip() and l.disponible), None)
        if usuario and libro:
            libro.disponible = False
            prestamo = Prestamo(usuario, libro)  
            usuario.prestamos.append(prestamo)  
            print(
                f"El libro '{titulo}' ha sido prestado a {usuario.nombre}. Fecha de préstamo: {prestamo.fecha_prestamo.strftime('%d/%m/%Y %H:%M:%S')}."
            )
        else:
            print(
                "No se puede realizar el préstamo. Verifica que el libro esté disponible y el usuario esté registrado."
            )

    
    def devolver_libro(self, CC, titulo):
        usuario = next((u for u in self.usuarios if u.CC == CC), None)
        prestamo = next(
            (
                p
                for p in usuario.prestamos
                if p.libro.titulo == titulo and p.fecha_devolucion is None
            ),
            None,
        )
        if usuario and prestamo:
            prestamo.devolver_libro()  
            prestamo.libro.disponible = True  
            print(
                f"El libro '{titulo}' ha sido devuelto por {usuario.nombre}. Fecha de devolución: {prestamo.fecha_devolucion.strftime('%d/%m/%Y %H:%M:%S')}."
            )
        else:
            print(
                "No se puede devolver el libro. Verifica que el libro esté prestado al usuario."
            )

    
    def mostrar_usuarios_prestados(self):
        for usuario in self.usuarios:
            if usuario.prestamos: 
                libros_prestados = [
                    prestamo.libro.titulo for prestamo in usuario.prestamos
                ]
                print(
                    f"{usuario.nombre} ha solicitado los siguientes libros: {', '.join(libros_prestados)}."
                )
            else:
                print(f"{usuario.nombre} no ha solicitado libros.")

   
    def mostrar_usuarios(self):
        print("\nLista de Usuarios Registrados:")
        for usuario in self.usuarios:
            print(f"- {usuario.nombre}, CC: {usuario.CC}")