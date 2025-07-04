from abc import ABC, abstractmethod
import csv

class Librery(ABC):
    def __init__(self, title: str, item_id: int):
        if not title.strip():
            raise ValueError("el titulo no puede estar vacío")
        if item_id <= 0:
            raise ValueError("el id debe ser un número entero positivo")   
        self.title = title
        self.item_id = item_id

    @abstractmethod
    def checkout(self, usuario: str) -> str:
        pass

class Libro(Librery):
    def __init__(self, title: str, item_id: int, author: str, paginas: int):
        super().__init__(title, item_id)
        if not author.strip():
            raise ValueError("el autor no puede estar vacío")
        if paginas <= 0:
            raise ValueError("la cantidad páginas debe ser un número entero positivo")
        self.author = author
        self.paginas = paginas

    def checkout(self, usuario: str) -> str:
        return f"libro:{self.title} prestado a {usuario}"
    
class Revista(Librery):
    def __init__(self, title: str, item_id: int, numero_emision: int):
        super().__init__(title, item_id)
        if numero_emision <= 0:
            raise ValueError("el número de emision debe ser un número entero positivo")
        self.numero_emision = numero_emision

    def checkout(self, usuario: str) -> str:
        return f"revista:{self.title} prestada a {usuario}"  # Corregido: {usuario} en minúscula

def cargar_librery(path: str) -> list[Librery]:
    objetos_Librery = []
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                if not row:
                    continue
                tipo = row[0].strip().lower()
                title = row[1].strip()
                item_id = int(row[2])

                if tipo == 'libro':
                    if len(row) < 5:
                        raise ValueError("Faltan datos para el libro")
                    author = row[3].strip()
                    paginas = int(row[4])
                    objetos_Librery.append(Libro(title, item_id, author, paginas))

                elif tipo == "revista":
                    if len(row) < 4:
                        raise ValueError("Faltan datos para la revista")
                    numero_emision = int(row[3])
                    objetos_Librery.append(Revista(title, item_id, numero_emision))
            except (ValueError, IndexError, TypeError) as e:
                print(f"Error al cargar el objeto: {e}")
    return objetos_Librery

def checkout_librery(objetos_Librery: list, usuario: str) -> list[str]:
    return [objeto.checkout(usuario) for objeto in objetos_Librery]

def contador_objetos(objetos_Librery: list[Librery]) -> dict:
    contador = {"libro": 0, "revista": 0}
    for objeto in objetos_Librery:
        if isinstance(objeto, Libro):
            contador["libro"] += 1
        elif isinstance(objeto, Revista):
            contador["revista"] += 1
    return contador

def encontrar_titulo(objetos_Librery: list[Librery], palabra: str) -> list[Librery]:
    palabra = palabra.lower()
    return [objeto for objeto in objetos_Librery if palabra in objeto.title.lower()]


  #esta parte del codigo es por gusto personal, no es necesario para el funcionamiento del programa
    # 5. Pruebas de Guardado en CSV
    
def guardar_en_csv(items: list[Librery], path: str = "Librery.csv"):
    
    with open(path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for item in items:
            if isinstance(item, Libro):
                writer.writerow([
                    "libro",
                    item.title,
                    item.item_id,
                    item.author,
                    item.paginas
                ])
            elif isinstance(item, Revista):
                writer.writerow([
                    "revista",
                    item.title,
                    item.item_id,
                    item.numero_emision
                ])
        print(f"Datos guardados en {path}")