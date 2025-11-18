from pymongo import MongoClient
import random
import time
import sys

class DistributedStorage:
    def __init__(self):
        # Conectar a los dos contenedores de mongo
        print("Conectando a los servidores...")
        self.nodes = {
            "mongo1": MongoClient("mongodb://admin:admin@mongo1:27017/"),
            "mongo2": MongoClient("mongodb://admin:admin@mongo2:27017/")
        }
        # Guardamos la referencia a las colecciones
        self.collections = {node: self.nodes[node]["test"]["tasks"] for node in self.nodes}

    def clear_databases(self):
        # Borrar todo para que la prueba empiece limpia
        print("Limpiando datos viejos...")
        for name, col in self.collections.items():
            col.delete_many({})

    def insert_document(self, doc):
        # Elegir un nodo al azar (balanceo de carga simple)
        node = random.choice(list(self.collections.keys()))
        self.collections[node].insert_one(doc)
        return node

    def find_document(self, task_name):
        print(f"\nBuscando '{task_name}' en los nodos...")
        
        # Buscar en cada nodo uno por uno
        for node_name, collection in self.collections.items():
            print(f" -> Revisando en {node_name}...", end=" ")
            sys.stdout.flush()
            time.sleep(0.1) # Simular un poco de delay de red
            
            result = collection.find_one({"task": task_name})
            
            if result:
                print("ENCONTRADO!")
                return result, node_name
            else:
                print("No esta aqui.")
                
        return None, None

    def get_stats(self):
        # Contar cuantos docs tiene cada uno para ver si se repartieron bien
        stats = {node: collection.count_documents({}) for node, collection in self.collections.items()}
        return stats

if __name__ == "__main__":
    print("--- INICIO DEL SISTEMA DE ALMACENAMIENTO ---")
    
    storage = DistributedStorage()
    storage.clear_databases()

    # Variables para recordar un ejemplo de cada nodo
    tarea_en_mongo1 = None
    tarea_en_mongo2 = None

    # Insertar 100 datos
    print("\nInsertando 100 documentos aleatoriamente...")
    
    for i in range(100):
        doc = {"task": f"Tarea {i}", "value": random.randint(1,100)}
        node_used = storage.insert_document(doc)
        
        # Guardamos una tarea de ejemplo para cada nodo
        if node_used == "mongo1" and tarea_en_mongo1 is None:
            tarea_en_mongo1 = f"Tarea {i}"
        elif node_used == "mongo2" and tarea_en_mongo2 is None:
            tarea_en_mongo2 = f"Tarea {i}"

        # Imprimir solo algunos para no llenar la consola
        if i < 3 or i > 96:
            print(f"Guardado Tarea {i} en {node_used}")
        elif i == 3:
            print("... insertando los demas ...")

    # Ver como quedaron repartidos
    print("\n--- ESTADISTICAS ---")
    stats = storage.get_stats()
    print("Distribucion final:", stats)

    nombre_buscado = "Tarea 7" 
    
    print(f"\n--- PRUEBA MANUAL: Buscando {nombre_buscado} ---")

    doc, node = storage.find_document(nombre_buscado) 
    
    if doc:
        print(f"Resultado: Encontrado en {node}")
        print(f"Datos completos: {doc}") 
    else:
        print("No se encontró esa tarea específica.")

    print("\n--- FIN DE LA PRUEBA ---")