import unittest
import tempfile
import os
import csv
from librery import ( 
    Librery, Libro, Revista,
    cargar_librery, checkout_librery,
    contador_objetos, encontrar_titulo, guardar_en_csv
)

class TestLibrerySystem(unittest.TestCase):

    # 1. Pruebas de constructores
    def test_creacion_libro_valido(self):
        """Debería crear un libro con datos correctos"""
        libro = Libro("Cien años de soledad", 1, "García Márquez", 432)
        self.assertEqual(libro.title, "Cien años de soledad")
        self.assertEqual(libro.paginas, 432)

    def test_libro_titulo_vacio(self):
        """Debería fallar si el título está vacío"""
        with self.assertRaises(ValueError) as context:
            Libro("", 2, "Autor", 100)
        self.assertIn("no puede estar vacío", str(context.exception))

    def test_revista_emision_negativa(self):
        """Debería fallar si el número de emisión es negativo"""
        with self.assertRaises(ValueError) as context:
            Revista("National Geographic", 3, -1)
        self.assertIn("entero positivo", str(context.exception))

    # 2. Pruebas de Checkout
    def test_mensaje_checkout_libro(self):
        """El mensaje de checkout para libros debe incluir título y usuario"""
        libro = Libro("El Principito", 10, "Saint-Exupéry", 96)
        mensaje = libro.checkout("Ana")
        self.assertEqual(mensaje, "libro:El Principito prestado a Ana")

    def test_mensaje_checkout_revista(self):
        """El mensaje de checkout para revistas debe incluir título y usuario"""
        revista = Revista("Muy Interesante", 20, 150)
        mensaje = revista.checkout("Carlos")
        self.assertEqual(mensaje, "revista:Muy Interesante prestada a Carlos")

    # 3. Pruebas de Carga desde CSV
    def test_carga_csv_correcta(self):
        """Debería cargar libros y revistas válidos desde CSV"""
        csv_data = """libro,Don Quijote,1,Cervantes,1025
revista,Science Today,2,500
libro,1984,3,Orwell,328"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write(csv_data)
            temp_path = f.name
        
        items = cargar_librery(temp_path)
        os.unlink(temp_path)
        
        self.assertEqual(len(items), 3)
        self.assertIsInstance(items[0], Libro)
        self.assertIsInstance(items[1], Revista)
        self.assertEqual(items[2].title, "1984")

    def test_carga_csv_con_errores(self):
        """Debería ignorar líneas corruptas en el CSV"""
        csv_data = """libro,,5,Autor,100
revista,Revista Válida,10,30
libro,Título Inválido,no_es_numero,Autor,200"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write(csv_data)
            temp_path = f.name
        
        items = cargar_librery(temp_path)
        os.unlink(temp_path)
        
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].item_id, 10)

    # 4. Pruebas de Funciones de Reporte
    def test_checkout_multiple(self):
        """Debería generar mensajes para todos los ítems"""
        items = [
            Libro("Ficciones", 1, "Borges", 200),
            Revista("Literatura Hoy", 2, 42)
        ]
        mensajes = checkout_librery(items, "Luisa")
        
        self.assertEqual(len(mensajes), 2)
        self.assertIn("Ficciones", mensajes[0])
        self.assertIn("Luisa", mensajes[1])

    def test_contador_objetos(self):
        """Debería contar correctamente libros y revistas"""
        items = [
            Libro("L1", 1, "A1", 100),
            Revista("R1", 2, 1),
            Libro("L2", 3, "A2", 200),
            Revista("R2", 4, 2)
        ]
        conteo = contador_objetos(items)
        
        self.assertEqual(conteo, {"libro": 2, "revista": 2})

    def test_busqueda_titulo(self):
        """Debería encontrar títulos sin importar mayúsculas"""
        items = [
            Libro("EL HOBBIT", 1, "Tolkien", 310),
            Revista("el País Semanal", 2, 1000),
            Libro("Cien años de soledad", 3, "García Márquez", 432)
        ]
        resultados = encontrar_titulo(items, "el")
        
        self.assertEqual(len(resultados), 2)
        self.assertEqual(resultados[0].title, "EL HOBBIT")
        self.assertEqual(resultados[1].title, "el País Semanal")

    def test_guardar_csv(self):
        """Debería guardar libros específicos en CSV sin errores"""
        items = [
            Libro("48 Leyes del Poder", 1, "Robert Greene", 480),
            Libro("El Arte de la Guerra", 2, "Sun Tzu", 272),
            Libro("El Camino del Hombre Superior", 3, "David Deida", 256)
        ]
        guardar_en_csv(items, "Librery.csv") 
        self.assertTrue(os.path.exists("Librery.csv"))
        
        with open("Librery.csv", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 3)
        
        print("\n Libros guardados en Librery.csv:")
        for line in lines:
            print(line.strip())

if __name__ == "__main__":
    unittest.main(verbosity=2)