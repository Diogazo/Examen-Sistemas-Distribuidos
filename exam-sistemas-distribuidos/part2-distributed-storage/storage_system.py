from pymongo import MongoClient
import random

class DistributedStorage:
    def __init__(self):
        self.nodes = {
            "mongo1": MongoClient("mongodb://admin:admin@mongo1:27017/"),
            "mongo2": MongoClient("mongodb://admin:admin@mongo2:27017/")
        }
        self.collections = {node: self.nodes[node]["test"]["tasks"] for node in self.nodes}

    def insert_document(self, doc):
        """Distribuye documentos aleatoriamente entre nodos"""
        node = random.choice(list(self.collections.keys()))
        self.collections[node].insert_one(doc)

    def find_document(self, document_id):
        """Busca documento en todos los nodos"""
        for node, collection in self.collections.items():
            result = collection.find_one({"_id": document_id})
            if result:
                return result
        return None

    def get_stats(self):
        """Cuenta documentos en cada nodo"""
        stats = {node: collection.count_documents({}) for node, collection in self.collections.items()}
        return stats

if __name__ == "__main__":
    storage = DistributedStorage()
    # Insertar 100 documentos de prueba
    for i in range(100):
        storage.insert_document({"task": f"Tarea {i}", "value": random.randint(1,100)})

    # Mostrar estadísticas
    stats = storage.get_stats()
    print("Estadísticas de distribución:", stats)

    # Probar búsqueda
    print("Buscando documento 10:", storage.collections["mongo1"].find_one({"task": "Tarea 10"}) or
          storage.collections["mongo2"].find_one({"task": "Tarea 10"}))
